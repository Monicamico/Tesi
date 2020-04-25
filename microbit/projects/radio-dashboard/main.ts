/**
 * Radio-dashboard
 * main.ts
 * @author Monica Amico 
 */

/*--------------------------------- VARIABLE STATEMENTS --------------------------------*/

const vase_list: Vase[] = [];            // list of vases
const conn_request: Request[] = [];      // list of connection requests
let dim_vase_list: number = 0;           // size of vase_list
let pause_time = 200000                  //(
let current_time;
let deadping = 1200000;                  // (20 min)

/*------------------------------------ INITIAL CODE -------------------------------------*/

led.setBrightness(120)
radio.setTransmitSerialNumber(true)
radio.setGroup(18)
radio.setTransmitPower(7)
serial.redirectToUSB()
serial.writeLine('') //utile per bytes b'\x00 che scrive il microbit all'avvio
dim_vase_list = vase_list.length
DEBUG = true

if (DEBUG) {
    deadping = 300000
}

/*------------------------------------------ MAIN CODE ------------------------------------------- */

basic.forever(function () {
   
   current_time = input.runningTime()
    for (const vase of vase_list){
        if ((current_time - vase.getPing()) > deadping){
            if (vase.dying) 
            {
                dim_vase_list = deleteVase(vase.serial_number, vase_list)
                if (dim_vase_list!= undefined){
                    basic.showString("del")
                    sendToRB(`${OPERATION.DELETED};${vase.serial_number};0;0`)
                    drawNumberOfVases(dim_vase_list)
                }    
            } else {
                vase.dying = true;
                sendToVase(OPERATION.PING,vase.serial_number)
            }
        }
    }
    basic.pause(pause_time)
})


/* --------------------------------------- EVENTS CODE -------------------------------------------- */

//to accept the request connection from the vase
input.onButtonPressed(Button.A, function () {

    let n = dim_vase_list
    let req = conn_request.shift()
    if (req){ 
        dim_vase_list = insertVase(req.serial_number, req.ping, vase_list)
        if (n == dim_vase_list - 1){
            //send the joined notification to smart-vase
            sendToVase(OPERATION.JOINED,req.serial_number)
            //send joined notification to raspberry
            sendToRB(`${OPERATION.JOINED};${req.serial_number};${req.ping};0`) 
            
        } 
    }
    
})

//to refuse the request connection from the vase
input.onButtonPressed(Button.B, function () {

    let req = conn_request.shift()
    if (req)
        sendToRB(`${OPERATION.REFUSED};${req.serial_number};0;0`)
})

/* ----------------------------------- RECEIVED FROM SMART-VASE ------------------------------------- */

/* code to be executed when:
 *  - CONNECTION REQUEST is received from the SMARTVASE
 *  - PING is received from the SMARTVASE 
*/
radio.onReceivedNumber(function (received: number) {

    const serialNumber = radio.receivedPacket(RadioPacketProperty.SerialNumber)

    if (received == OPERATION.CONNECTION) {
        if (getVase(serialNumber, vase_list)){
            sendToVase(OPERATION.JOINED,serialNumber) 
            return
        }
        if (containRequest(serialNumber, conn_request)) 
            return
        let ping_req = input.runningTime();
        conn_request.push(new Request(serialNumber,ping_req))
        //send connection request to raspberry
        sendToRB(`${OPERATION.CONNECTION};${serialNumber};${ping_req};0`) 

    } else if (received == OPERATION.PING) {
        
        let ping = input.runningTime();
        let vase = getVase(serialNumber, vase_list)
        if (vase) {
            vase.setPing(ping)
            sendToRB(`${OPERATION.PING};${serialNumber};${ping};0`)
        }
    }
})


/*
 * code to be executed when:
 *   - HUMIDITY VALUE is received from a SMART-VASE
 *   - TEMPERATURE VALUE is received from a SMART-VASE
 *   - LIGHT VALUE is received from a SMART-VASE
 *   - WATER CONTAINER STATE is received from a smart-vase
*/
radio.onReceivedValue(function (request: string, param: number) {

    const serialNumber = radio.receivedPacket(RadioPacketProperty.SerialNumber)
    const vase = getVase(serialNumber, vase_list)
    let ping = input.runningTime()
    let requestInt = parseInt(request)
    if (!vase)
            return
    vase.setPing(ping) //update ping value of the vase

    if (requestInt == OPERATION.WATER_CONTAINER_STATE){
        if (param == 0) // 0 = empty, 1 = full
            sendToRB(`${OPERATION.WATER_CONTAINER_STATE};${serialNumber};${ping};${param}`) 
        return
    } else if (requestInt == OPERATION.LIGHT || requestInt == OPERATION.TEMPERATURE || requestInt == OPERATION.HUMIDITY)
        //send the received value to raspberry as a string
        sendToRB(`${request};${serialNumber};${ping};${param}`) 
    
})

/*-------------------------------------- FROM RASPBERRY -------------------------------------------*/

/* REQUEST received from RASPBERRY */

serial.onDataReceived(serial.delimiters(Delimiters.Fullstop), function(){
    
    let received = serial.readUntil(serial.delimiters(Delimiters.Fullstop))
    let r_list= received.split(";") 
    let size = r_list.length

    if (size == 0 || size == 1) return
    
    let request = parseInt(r_list[0])
    let serialNumber = parseInt(r_list[1]) 
    let param = -1;

    if (size == 3)
        param = parseInt(r_list[2])

    let vase_exist = getVase(serialNumber, vase_list)

    if (vase_exist) {

        if (request == OPERATION.PING || request == OPERATION.HUMIDITY ||
            request == OPERATION.TEMPERATURE || request == OPERATION.LIGHT || request == OPERATION.WATER) 
            sendToVase(request, serialNumber)
            
        else if (request == OPERATION.SET_TEMPERATURE_MIN || request == OPERATION.SET_TEMPERATURE_MAX ||
                 request == OPERATION.SET_LIGHT_MIN || request == OPERATION.SET_LIGHT_MAX ||
                 request == OPERATION.SET_HUMIDITY_MAX || request == OPERATION.SET_HUMIDITY_MIN ||
                 request == OPERATION.SET_VASE_PAUSE_TIME || request == OPERATION.SET_VASE_SEND_TIME ||
                 request == OPERATION.WATER_CONTAINER_STATE || request == OPERATION.SET_WATERING_LIGHT ) {
                     if (param != -1) 
                        sendToVase(request,serialNumber,param)
                 }

        else if (request == OPERATION.SET_WATER_CONTAINER_SIZE && size == 3){
            param = parseFloat(r_list[2])
            sendToVase(request,serialNumber,param)
        }
        return
    
    } else {

        if (request == OPERATION.JOINED) {   
            //get and remove from the conn_list the ping of the vase
            let ping = deleteRequest(serialNumber,conn_request)
            let n = dim_vase_list

            if (ping!= -1) {
                dim_vase_list = insertVase(serialNumber,ping,vase_list)
                if (n == dim_vase_list - 1){
                    //send the joined notification to smart-vase
                    sendToVase(OPERATION.JOINED,serialNumber)
                    //send joined notification to raspberry
                    sendToRB(`${OPERATION.JOINED};${serialNumber};${ping};0`) 
                } else {
                    conn_request.push(new Request(serialNumber,ping))
                }
            }
            return
        }
        else if (request == OPERATION.REFUSED) {
            let ping = deleteRequest(serialNumber,conn_request)
            if (ping!= -1){
                sendToRB(`${OPERATION.REFUSED};${serialNumber};0;0`)
            }
            return
        }
    }

    if (request == OPERATION.SET_RADIO_DEADPING_TIME){
        param = parseInt(r_list[1])
        setDeadping(param)
    }
    
    else if ( request == OPERATION.SET_RADIO_PAUSE_TIME){            
        param = parseInt(r_list[1])
        setRadioPauseTime(param)
    }

})
