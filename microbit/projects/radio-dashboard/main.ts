/**
 * Radio-dashboard
 * main.ts
 * @author Monica Amico 
 */

/*--------------------------------- VARIABLE STATEMENTS --------------------------------*/

const vase_list: Vase[] = [];           // list of vases
const conn_request: Request[] = [];      // list of connection requests
let dim_vase_list: number = 0;               // size of vase_map
let pause_time = 80000
let current_time;
let diedping = 300000;


/*------------------------------------ INITIAL CODE -------------------------------------*/

led.setBrightness(50)
radio.setTransmitSerialNumber(true)
radio.setGroup(18)
radio.setTransmitPower(7)
dim_vase_list = vase_list.length
diedping = 300000;

/*--------------------------------------- RADIO CODE -------------------------------------*/
basic.forever(function () {

    current_time = input.runningTime()

    for (const vase of vase_list){

        if ((current_time - vase.getPing()) > diedping){
            if (vase.dying) {
                dim_vase_list = deleteVase(vase.serial_number, vase_list)
                if (dim_vase_list!= undefined){
                    basic.showString("del")
                    drawNumberOfVases(dim_vase_list)
                }
                
            }
            else {
                vase.dying = true;
                sendRequest("ping",vase.serial_number)
            }
        }
    }
    basic.pause(pause_time)
})

/*--------------------------------------- EVENTS CODE ------------------------------------*/


//to accept the request connection from the vase
input.onButtonPressed(Button.A, function () {

    let req = conn_request.shift()
    dim_vase_list = insertVase(req.serial_number, req.ping, vase_list)
    setJoined(req.serial_number)//send the joined notification to smart-vase
    sendResponse(`joined;${req.serial_number};${req.ping}`) //send joined notification to raspberry

})

//to refuse the request connection from the vase
input.onButtonPressed(Button.B, function () {
    let req = conn_request.shift()
    sendResponse(`refused;${req.serial_number}`)
})


/* code to be executed when a connection request or ping is received from the smartvase */
radio.onReceivedString(function (receivedString: string) {

    const serialNumber = radio.receivedPacket(RadioPacketProperty.SerialNumber)

    if (receivedString == "join"){
        if (containRequest(serialNumber, conn_request)) return;
        conn_request.push(new Request(serialNumber, input.runningTime()))
        sendResponse(`conn_req;${serialNumber}`) //send connection request to raspberry

    } else if (receivedString == "ping"){
        /* I don't check if it is on the list, 
           I only receive ping from vases that have been requested*/
        let ping = input.runningTime();
        getVase(serialNumber).setPing(ping)
        sendResponse(`ping;${serialNumber};${ping}`)
    }
})


//code to be executed when a value is received from a smart-vase
radio.onReceivedValue(function (request: string, param: number) {

    const serialNumber = radio.receivedPacket(RadioPacketProperty.SerialNumber)
    const vase = getVase(serialNumber)
    if (!vase) return;
    let ping = input.runningTime()
    //send the received value to raspberry as a string
    sendResponse(`${request};${serialNumber};${param};${ping}`) 

    switch (request){
        case ("getHum"): { 
            basic.showNumber(param)
            basic.clearScreen()
            vase.setHumidity(param)
            break;
        }
        case ("getTemp"):{
            basic.showNumber(param)
            basic.clearScreen()
            vase.setTemperature(param)
            break;
        }
        case ("getLight"):{
            basic.showNumber(param)
            basic.clearScreen()
            vase.setLight(param)
            break;
        }
    }
    drawNumberOfVases(dim_vase_list)
})


/* request received from RaspBerry */
serial.onDataReceived(";", function(){

    let received = serial.readUntil(serial.delimiters(Delimiters.Fullstop))
    let r_list= received.split(";")
    let request = r_list[0]
    let serialNumber = parseInt(r_list[1])

    switch(request){

        case ("join"): {
            let ping =deleteRequest(serialNumber,conn_request)
            if (ping!= -1){
                dim_vase_list = insertVase(serialNumber,ping,vase_list)
                setJoined(serialNumber) //send the joined notification to smart-vase
                sendResponse(`joined;${serialNumber};${ping}`) //send joined notification to raspberry
            }
            break;
        }

        case ("refuse"): {
            let ping =deleteRequest(serialNumber,conn_request)
            if (ping!= -1){
                sendResponse(`refused;${serialNumber}`)
            }
            break;
        }

        case ("ping"): {
            if (getVase(serialNumber)){
                sendRequest("ping",serialNumber)
            }
            break;
        }

        case ("getHum"): {
            getHum(serialNumber)
            break;
        }

        case ("getTemp"): {
            getTemp(serialNumber)
            break;
        }
        
        case ("getLight"): {
            getLight(serialNumber)
            break;
        }

        case ("water"): {
            putWater(serialNumber)
            break;
        }

        case ("setTempMin"): {
            let param = parseInt(r_list[2])
            setTempMin(serialNumber,param)
            break;
        }

        case ("setTempMax"): {
            let param = parseInt(r_list[2])
            setTempMax(serialNumber,param)
            break;
        }

        case ("setLightMax"): {
            let param = parseInt(r_list[2])
            setLightMax(serialNumber,param)
            break;
        }
        
        case ("setLightMin"): {
            let param = parseInt(r_list[2])
            setLightMin(serialNumber,param)
            break;
        }

        case ("setHumMin"): {
            let param = parseInt(r_list[2])
            setHumMin(serialNumber,param)
            break;
        }

        case ("setHumMax"): {
            let param = parseInt(r_list[2])
            setHumMin(serialNumber,param)
            break;
        }

        case ("setPtime"): {
            let param = parseInt(r_list[2])
            setPTime(serialNumber,param)
            break;
        }

        case ("setStime"): {
            let param = parseInt(r_list[2])
            setSTime(serialNumber,param)
            break;
        }

        case ("setDiedping"): {
            let param = parseInt(r_list[1])
            setDiedping(param)
            break;
        }

        case ("setRadioPause"): {
            let param = parseInt(r_list[1])
            setRadioPauseTime(param)
            break;
        }
    
    }
})