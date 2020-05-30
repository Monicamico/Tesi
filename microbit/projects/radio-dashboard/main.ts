/**
 * Radio-dashboard
 * main.ts
 * @author Monica Amico 
 */

/*--------------------------------- VARIABLE STATEMENTS --------------------------------*/

let dim_vase_list: number = 0;           // size of vase_list
let pause_time = 200000                  //
let not_registered_pause_time = 8000
let current_time;
let deadping = 60               
let registered = false

/*------------------------------------ INITIAL CODE -------------------------------------*/

led.setBrightness(120)
radio.setTransmitSerialNumber(true)
radio.setGroup(18)
radio.setTransmitPower(7)
serial.redirectToUSB()
serial.writeLine('') //utile per bytes b'\x00 che scrive il microbit all'avvio
dim_vase_list = vase_list.length
DEBUG = true


/*------------------------------------------ MAIN CODE ------------------------------------------- */

basic.forever(function () {
    
    if (!registered){
        register()
        basic.pause(not_registered_pause_time)
    }
       
    else {
        
        current_time = Math.ceil((input.runningTime())/60000)
        for (const vase of vase_list){
            if ((current_time - vase.ping) > deadping){
                if (vase.dying)  {
                    dim_vase_list = deleteVase(vase.serial_number, vase_list)
                    if (dim_vase_list!= undefined){
                        basic.showString("del")
                        deleted_vases.push(vase.serial_number)
                        sendToVase(OPERATION.DELETED,vase.serial_number)
                        sendToRB(`${OPERATION.DELETED};${vase.serial_number};0;0`)
                        drawNumberOfVases(dim_vase_list)
                    }    
                } else {
                    vase.dying = true;
                    sendToVase(OPERATION.PING,vase.serial_number)
                    basic.pause(8000)
                }
            }
        }
        basic.pause(pause_time)
    }
   
})


/* --------------------------------------- EVENTS CODE -------------------------------------------- */

//to accept the request connection from the vase
input.onButtonPressed(Button.A, function () {
    let n = dim_vase_list
    let req = conn_request.shift()
    if (req){ 
        //send the joined notification to smart-vase
        sendToVase(OPERATION.JOINED,req.serial_number)
    }
    
})

//to refuse the request connection from the vase
input.onButtonPressed(Button.B, function () {
    let req = conn_request.shift()
    if (req){
        sendToRB(`${OPERATION.REFUSED};${req.serial_number};0;0`)
    }
        
})

//to show the pairing numbers
input.onButtonPressed(Button.AB, function(){
    showCasualNumbers(conn_request)
})

/* ----------------------------------- RECEIVED FROM SMART-VASE ------------------------------------- */

/* code to be executed when:
 *  - PING is received from the SMARTVASE 
*/
radio.onReceivedNumber(function (received: number) {

    const serialNumber = radio.receivedPacket(RadioPacketProperty.SerialNumber)

    if (received == OPERATION.PING) {
        let ping = Math.ceil(input.runningTime()/60000);
        let vase = getVase(serialNumber, vase_list)
        if (vase) {
            vase.dying = false
            vase.ping = ping
            sendToRB(`${OPERATION.PING};${serialNumber};${ping};${ping}`)
        }
    }
})


/*
 * code to be executed when:
 *   - JOINED notification has been received
 *   - CONNECTION request has been received
 *   - HUMIDITY VALUE has been received from a SMART-VASE
 *   - TEMPERATURE VALUE has been received from a SMART-VASE
 *   - LIGHT VALUE has been received from a SMART-VASE
 *   - WATER CONTAINER STATE has been received from a smart-vase
*/
radio.onReceivedValue(function (request: string, param: number) {

    const serialNumber = radio.receivedPacket(RadioPacketProperty.SerialNumber)
    let ping = Math.ceil(input.runningTime()/60000);
    const requestInt = parseInt(request)
    const vase = getVase(serialNumber, vase_list)

    if (requestInt == OPERATION.CONNECTION) {
         // if the vase has already been joined to the vase list
        // the radio will send to vase a 'joined' notification
        if ( vase || isDeletedVase(serialNumber) ){
            sendToVase(OPERATION.JOINED,serialNumber) 
            return
        }
        if (containRequest(serialNumber, conn_request)){
            deleteRequest(serialNumber,conn_request)
        } 
        conn_request.push(new Request(serialNumber, ping, param))
        //send connection request to raspberry
        const signal_strenght = radio.receivedPacket(RadioPacketProperty.SignalStrength)
        sendToRB(`${OPERATION.CONNECTION};${serialNumber};${signal_strenght};${param}`) 
        return

    } else if (requestInt == OPERATION.JOINED) {
        if (vase) 
            return
        if (param == serial_number){
            let n = dim_vase_list
            dim_vase_list = insertVase(serialNumber,ping,vase_list)
            if (n == dim_vase_list - 1) {
                //send joined notification to raspberry
                sendToRB(`${OPERATION.JOINED};${serialNumber};${ping};${serial_number}`) 
            } else {
                sendToRB(`${OPERATION.REFUSED};${serialNumber};0;0`) 
                sendToVase(OPERATION.REFUSED,serialNumber)
            }
        }
        return
    }
    
    if (!vase)
        return
    vase.ping = ping //update ping value of the vase
    vase.dying = false

    if (requestInt == OPERATION.WATER_CONTAINER_STATE ||
        requestInt == OPERATION.SET_WATER_CONTAINER_SIZE ||
        requestInt == OPERATION.SET_WATERING_LIGHT ||
        requestInt == OPERATION.LIGHT ||
        requestInt == OPERATION.TEMPERATURE ||
        requestInt == OPERATION.HUMIDITY)
        sendToRB(`${request};${serialNumber};${ping};${param}`) 

    if (requestInt == OPERATION.SET_LIGHT_MIN ||
        requestInt == OPERATION.SET_LIGHT_MAX ||
        requestInt == OPERATION.SET_HUMIDITY_MIN ||
        requestInt == OPERATION.SET_HUMIDITY_MAX ||
        requestInt == OPERATION.SET_TEMPERATURE_MIN ||
        requestInt == OPERATION.SET_TEMPERATURE_MAX ||
        requestInt == OPERATION.SET_VASE_SEND_TIME ||
        requestInt == OPERATION.VASE_TRANSMIT_POWER ) {
            sendToRB(`${request};${serialNumber};${ping};${param}`) 
            //send the received value to raspberry as a string
        }
})

/*-------------------------------------- FROM RASPBERRY -------------------------------------------*/

/* REQUEST received from RASPBERRY */

serial.onDataReceived(serial.delimiters(Delimiters.Hash), function(){

    let received = serial.readUntil(serial.delimiters(Delimiters.Hash))
    let r_list= received.split(";") 
    let size = r_list.length
    let request = parseInt(r_list[0])

    if (size == 0)
        return
    if (size == 1){
        if (request == OPERATION.RADIO_JOIN)
            registered = true
        return
    }

    let serialNumber = parseInt(r_list[1]) 
    let param = -1;

    if (size == 3) {
        param = parseInt(r_list[2])
    }

    if (request == OPERATION.SET_RADIO_PAUSE_TIME) {
        setRadioPauseTime(param)
        sendToRB(`${OPERATION.SET_RADIO_PAUSE_TIME};${serial_number};0;${param}`)
        return

    } else if (request == OPERATION.RADIO_TRANSMIT_POWER) {
        setTransmitPower(param)   
        sendToRB(`${OPERATION.RADIO_TRANSMIT_POWER};${serial_number};0;${param}`)
        return

    } else if (request == OPERATION.ADD_EXISTING_VASE) {
        let n = dim_vase_list
        dim_vase_list = insertVase(serialNumber,input.runningTime(),vase_list)
        if (n == dim_vase_list - 1) {
            sendToRB(`${OPERATION.JOINED};${serialNumber};${input.runningTime()};${serial_number}`)
        }
        return
    }
    
    let vase_exist = getVase(serialNumber, vase_list)

    if (vase_exist) {

        if (request == OPERATION.DELETED) {
            dim_vase_list = deleteVase(vase_exist.serial_number, vase_list)
            if (dim_vase_list != undefined) {
                basic.showString("del")
                sendToVase(request, serialNumber)
                sendToRB(`${OPERATION.DELETED};${vase_exist.serial_number};0;0`)
                drawNumberOfVases(dim_vase_list)
            }    
            return 
        }

        if (request == OPERATION.PING || request == OPERATION.HUMIDITY ||
            request == OPERATION.TEMPERATURE || request == OPERATION.LIGHT ||
            request == OPERATION.WATER || request == OPERATION.WATER_CONTAINER_STATE) 
            sendToVase(request, serialNumber)
            
        else if (request == OPERATION.SET_TEMPERATURE_MIN || request == OPERATION.SET_TEMPERATURE_MAX ||
                 request == OPERATION.SET_LIGHT_MIN || request == OPERATION.SET_LIGHT_MAX ||
                 request == OPERATION.SET_HUMIDITY_MAX || request == OPERATION.SET_HUMIDITY_MIN ||
                 request == OPERATION.SET_VASE_SEND_TIME ||request == OPERATION.SET_WATERING_LIGHT ||
                 request == OPERATION.VASE_TRANSMIT_POWER ) {
                    if (param != -1) 
                        sendToVase(request,serialNumber,param)
        }

        else if (request == OPERATION.SET_WATER_CONTAINER_SIZE && size == 3){
            param = parseFloat(r_list[2])
            sendToVase(request,serialNumber,param)
        }

        return
    
    } else {

        if (request == OPERATION.DELETED) {
            basic.showString("del")
            sendToVase(request, serialNumber)
            sendToRB(`${OPERATION.DELETED};${vase_exist.serial_number};0;0`)
            drawNumberOfVases(dim_vase_list)
            return
        }

        else if (request == OPERATION.JOINED) {   
            //get and remove from the conn_list the ping of the vase
            let ping = deleteRequest(serialNumber,conn_request)
            if (ping!= -1) {
                sendToVase(OPERATION.JOINED,serialNumber)
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
})
