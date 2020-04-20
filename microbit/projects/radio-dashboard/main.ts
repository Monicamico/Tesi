/**
 * Radio-dashboard
 * main.ts
 * @author Monica Amico 
 */

/*--------------------------------- VARIABLE STATEMENTS --------------------------------*/

const vase_list: Vase[] = [];            // list of vases
const conn_request: Request[] = [];      // list of connection requests
let dim_vase_list: number = 0;           // size of vase_list
let pause_time = 600000                  //(10 min)
let current_time;
let diedping = 1200000;                  // (20 min)

/*------------------------------------ INITIAL CODE -------------------------------------*/

led.setBrightness(120)
radio.setTransmitSerialNumber(true)
radio.setGroup(18)
radio.setTransmitPower(7)
serial.redirectToUSB()

dim_vase_list = vase_list.length

if (DEBUG) {
    diedping = 500000   // 8 min
}
/*--------------------------------------- RADIO CODE -------------------------------------*/
basic.forever(function () {
   
   current_time = input.runningTime()
    
    for (const vase of vase_list){

        if ((current_time - vase.getPing()) > diedping){
            if (vase.dying) {
                dim_vase_list = deleteVase(vase.serial_number, vase_list)
                if (dim_vase_list!= undefined){
                    basic.showString("del")
                    sendResponse("deleted;"+vase.serial_number+";0;0")
                    drawNumberOfVases(dim_vase_list)
                }    
            }
            else {
                vase.dying = true;
                ping(vase.serial_number)
            }
        }
    }
    basic.pause(pause_time)

})

/*--------------------------------------- EVENTS CODE --------------------------------------*/

//to accept the request connection from the vase
input.onButtonPressed(Button.A, function () {
    let n = dim_vase_list
    let req = conn_request.shift()
    if (req){ 
        dim_vase_list = insertVase(req.serial_number, req.ping, vase_list)
        if (n == dim_vase_list - 1){
            setJoined(req.serial_number)//send the joined notification to smart-vase
            sendResponse(`joined;${req.serial_number};${req.ping};0`) //send joined notification to raspberry
        } 
    }
    
})

//to refuse the request connection from the vase
input.onButtonPressed(Button.B, function () {
    let req = conn_request.shift()
    if (req)
        sendResponse(`refused;${req.serial_number};0;0`)
})


/* code to be executed when a CONNECTION REQUEST or PING is received from the SMARTVASE */
radio.onReceivedString(function (receivedString: string) {

    const serialNumber = radio.receivedPacket(RadioPacketProperty.SerialNumber)

    if (receivedString == "join") {

        if (containRequest(serialNumber, conn_request)) return;
        let ping_req = input.runningTime();
        conn_request.push(new Request(serialNumber,ping_req ))
        sendResponse(`conn_req;${serialNumber};${ping_req};0`) //send connection request to raspberry

    } else if (receivedString == "ping") {
        
        let ping = input.runningTime();
        let vase = getVase(serialNumber, vase_list)
        if (vase!= undefined) {
            vase.setPing(ping)
            sendResponse(`ping;${serialNumber};${ping};0`)
        }
    }
})


//code to be executed when a VALUE is received from a SMART-VASE
radio.onReceivedValue(function (request: string, param: number) {

    const serialNumber = radio.receivedPacket(RadioPacketProperty.SerialNumber)
    const vase = getVase(serialNumber, vase_list)
    if (!vase) return;
    let ping = input.runningTime()
    //send the received value to raspberry as a string
    sendResponse(`${request};${serialNumber};${ping};${param}`) 

    switch (request){
        case ("getHum"): { 
            basic.showString("H")
            basic.clearScreen()
            break;
        }
        case ("getTemp"):{
            basic.showString("T")
            basic.clearScreen()
            break;
        }
        case ("getLight"):{
            basic.showString("L")
            basic.clearScreen()
            break;
        }
    }
    drawNumberOfVases(dim_vase_list)
})


/* REQUEST received from RASPBERRY */
serial.onDataReceived(serial.delimiters(Delimiters.Fullstop), function(){
    
    let received = serial.readUntil(serial.delimiters(Delimiters.Fullstop))
    let r_list= received.split(";")

    let param = 0;
    let request = parseInt(r_list[0])
    let serialNumber = parseInt(r_list[1]) 

    if (r_list.length == 3)
        param = parseInt(r_list[2])

    console.log(request.toString())

    let vase_exist = getVase(serialNumber, vase_list)

    if (vase_exist) {

        if (request == OPERATION.PING) 
            ping(serialNumber)
            
        else if (request == OPERATION.HUMIDITY)
            getHum(serialNumber)

        else if (request == OPERATION.TEMPERATURE)
            getTemp(serialNumber)
            
        else if (request == OPERATION.LIGHT)
            getLight(serialNumber)

        else if (request == OPERATION.WATER)
            putWater(serialNumber)

        else if (request == OPERATION.SET_TEMPERATURE_MIN)
            setTempMin(serialNumber,param)
    
        else if(request == OPERATION.SET_TEMPERATURE_MAX)
            setTempMax(serialNumber,param)

        else if (request == OPERATION.SET_LIGHT_MAX)
            setLightMax(serialNumber,param)

        else if (request == OPERATION.SET_LIGHT_MIN)
            setLightMin(serialNumber,param)

        else if (request == OPERATION.SET_HUMIDITY_MIN)
            setHumMin(serialNumber,param)
  
        else if (request == OPERATION.SET_HUMIDITY_MAX)
            setHumMax(serialNumber,param)
  
        else if (request == OPERATION.SET_VASE_PAUSE_TIME)
            setPTime(serialNumber,param)

        else if (request == OPERATION.SET_VASE_SEND_TIME)
            setSTime(serialNumber,param)

    } else {

        if (request == OPERATION.JOINED) {   
            //get and remove from the conn_list the ping of the vase
            let ping = deleteRequest(serialNumber,conn_request)
            let n = dim_vase_list
            if (ping!= -1){
                dim_vase_list = insertVase(serialNumber,ping,vase_list)
                if (n == dim_vase_list - 1){
                    //send the joined notification to smart-vase
                    //and send the request to get the values (hum, light, temp)
                    setJoined(serialNumber)
                    //send joined notification to raspberry
                    sendResponse(`joined;${serialNumber};${ping};0`) 
                } else {
                    conn_request.push(new Request(serialNumber,ping))
                }
            }
        }
        else if (request == OPERATION.REFUSED){
            let ping = deleteRequest(serialNumber,conn_request)
            if (ping!= -1){
                sendResponse(`refused;${serialNumber};0;0`)
            }
        }
    }

    if (request == OPERATION.SET_RADIO_DIEDPING_TIME){
        param = parseInt(r_list[1])
        setDiedping(param)
    }
    
    else if ( request == OPERATION.SET_RADIO_PAUSE_TIME){            
        param = parseInt(r_list[1])
        setRadioPauseTime(param)
    }

})
