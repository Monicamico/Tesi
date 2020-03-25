/**
 * Radio-dashboard
 * @author Monica Amico 
 */

import { write } from "fs";

/*-------------------------------- VASE CLASS ----------------------------------*/
class Vase {
    serial_number: number;    // serial number of the vase
    temp: number;             // temperature value of the vase
    hum: number;              // humidity value of the vase
    light: number;
    ping: number;             // ping
    dying: boolean;

    constructor(id: number, ping: number) {
        if (id) {
            this.serial_number = id;
            this.temp = 0;
            this.light = 0;
            this.hum = 0;
            this.ping = ping
            this.dying = false;
        }
    }

    /**
     * @summary changes the temperature value of the vase
     * @param temp_vase (number) rappresenting the temperature of the vase
     */
    setTemperature(temp_vase: number) {
        this.temp = temp_vase
        this.ping = input.runningTime()
    }

    /**
     * @summary changes the humidity value of the vase
     * @param hum_vase (number) rappresenting the humidity of the vase
     */
    setHumidity(hum_vase: number) {
        this.hum = hum_vase
        this.ping = input.runningTime()
    }

    /**
     * @summary changes the light value of the vase
     * @param light_vase (number) rappresenting the light of the vase
     */
    setLight(light_vase: number) {
        this.light = light_vase
        this.ping = input.runningTime()
    }

    /**
     * @summary to get the serial number of the vase
     * @returns the serial number
     */
    getSerial() {
        return this.serial_number
    }

    getPing(){
        return this.ping
    }

    setPing(ping:number){
        this.ping = ping;
    }
}

class Request {
    serial_number: number
    ping: number

    constructor(s:number, ping:number){
        this.serial_number = s
        this.ping = ping;
    }
}
/*--------------------------------- VARIABLE STATEMENTS --------------------------------*/

const vase_list: Vase[] = [];           // list of vases
const conn_request: Request[] = [];      // list of connection requests
let dim_list: number = 0;               // size of vase_map
let pause_time = 80000
let current_time;
let diedping = 300000;

/*------------------------------------- FUNCTIONS ---------------------------------------*/

/**
 * @summary the function getVase returns the vase with serial number equal to id. 
 *           if the vase does not exist returns undefined
 * @param id (number) the serial number of the vase.
 * @return the vase with serial number equal to id.
*/
function getVase(id: number): Vase {
    if (!id) return undefined;
    for (const vase of vase_list){
        if (vase.getSerial() == id)
            return vase;
    }
    return undefined;
}

/**
 * @summary the function insert the vase with serial number equal to id into the list.
 * @param id (number) the serial number of the vase.
 * @return the vase with serial number equal to id or undefined.
*/
function insertVase(id: number, p:number): Vase {
    if (!id) return undefined;
    let v = getVase(id)
    if (v!= undefined) return v
    dim_list = vase_list.length
    if (dim_list == 24)
        return undefined;
    const vase: Vase = new Vase(id, p)
    if (!vase) return undefined;
    //add a new plot that rappresents the new vase
    led.plot(dim_list % 5, dim_list / 5)
    //insert the new vase in the list
    vase_list.push(vase)
    dim_list = vase_list.length
    return vase;
}

/**
 * @summary the function delete the vase with serial number equal to id into the list.
 * @param id (number) the serial number of the vase.
*/
function deleteVase(id:number){
    if (!id) return;
    let i = 0
    while (i < dim_list){
        let vase = vase_list.shift()
        if (vase.getSerial() != id)
            vase_list.push(vase)
        else {
            led.unplot(dim_list % 5, dim_list / 5)
            dim_list = vase_list.length
            return;
        }
        i++;
    }
    
}

/**
 * @summary the function check if the connection request has already been received
 * @param id the serial number of the vase.
 * @return true if the list contains the request, false otherwise
*/
function containRequest(id: number):boolean {
    for (const r of conn_request){
        if (r.serial_number == id) return true;
    }
    return false;
}


function deleteRequest(id:number): number {
    if (!id) return;
    let i = 0
    while (i < conn_request.length){
        let conn = conn_request.shift()
        if (conn.serial_number != id)
            conn_request.push(conn)
        else {
            return conn.ping;
        }
        i++;
    }
    return -1;
}
/**
 * @summary to plot points that rappresents the vases contained in the vaselist
 */
function drawNumberOfVases() {
    basic.clearScreen()
    let i = 0;
    while (i != dim_list) {
        led.plot(i % 5, i / 5)
        i++
    }
}

function setDiedping(x: number){
    diedping = x;
}

function setRadioPauseTime(x:number){
    pause_time = x;
}

/**
 * @summary to send a request to smart-vase
 * @param request contains a string that rappresent the type of request
 * @param serial serial number of the smart-vase
 * @param x optional parameter, it could be useful to insert an additional value
 */
function sendRequest(request: string, serial: number, x?: number) {
    let msg: Buffer
    let content: string
    if (x) 
        content = request + ";" + serial + ";" + x;
    else 
        content = request + ";" + serial;
    msg = control.createBufferFromUTF8(content)
    radio.sendBuffer(msg)
}


/**
 * @summary to send a response to raspberry
 * @param response contains a string that rappresent the response
 */
function sendResponse(response: string){
    serial.writeString(response)
}


/*-------------------------- TYPES OF REQUEST TO SEND TO VASE ----------------------------*/

/**
 * @summary send temperature request to the vase with serial number equal to the parameter id.
 *          if the param is -1 the request will be send to all.
 * @param id (number) rappresents the serial number of the vase.
 */
function getTemp(id: number) {
    sendRequest("getTemp",id)
}

/**
 * @summary send humidity request to the vase with serial number equal to the parameter id.
 *          if the param is -1 the request will be send to all.
 * @param id (number) rappresents the serial number of the vase.
 */
function getHum(id: number) {
    sendRequest("getHum", id)
}

/**
 * @summary send light request to the vase with serial number equal to the parameter id.
 *          if the param is -1 the request will be send to all.
 * @param id (number) rappresents the serial number of the vase.
 */
function getLight(id: number) {
    sendRequest("getLight", id)
}

/**
 * @summary send the request to water the vase
 *          if the param is -1 the request will be send to all.
 * @param id (number) rappresents the serial number of the vase.
 */
function putWater(id: number) {
    sendRequest("water", id)
}

function setTempMin(id: number, min: number) {
    sendRequest("temp_min", id, min)
}

function setTempMax(id: number, max: number) {
    sendRequest("temp_max", id, max)
}

function setHumMin(id: number, min: number) {
    sendRequest("hum_min", id, min)
}

function setHumMax(id: number, max: number) {
    sendRequest("hum_max", id, max)
}

function setLightMin(id: number, min: number) {
    sendRequest("light_min", id, min)
}

function setLightMax(id: number, max: number) {
    sendRequest("light_max", id, max)
}

function setPTime(id: number, p: number) {
    sendRequest("pause_time", id, p)
}

function setSTime(id: number, s: number) {
    sendRequest("send_time", id, s)
}

function setJoined(id:number){
    sendRequest("joined", id)
}

/*------------------------------------- INITIAL CODE -------------------------------------*/

led.setBrightness(50)
radio.setTransmitSerialNumber(true)
radio.setGroup(18)
radio.setTransmitPower(7)
dim_list = vase_list.length
diedping = 300000;

/*--------------------------------------- RADIO CODE -------------------------------------*/
basic.forever(function () {

    current_time = input.runningTime()

    for (const vase of vase_list){

        if ((current_time - vase.getPing()) > diedping){
            if (vase.dying) {
                deleteVase(vase.serial_number)
                basic.showString("del")
                drawNumberOfVases()
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
    insertVase(req.serial_number, req.ping)
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
        if (containRequest(serialNumber)) return;
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
    drawNumberOfVases()
})


/* request received from RaspBerry */
serial.onDataReceived(";", function(){

    let received = serial.readUntil(serial.delimiters(Delimiters.Fullstop))
    let r_list= received.split(";")
    let request = r_list[0]
    let serialNumber = parseInt(r_list[1])

    switch(request){

        case ("join"): {
            let ping =deleteRequest(serialNumber)
            if (ping!= -1){
                insertVase(serialNumber,ping)
                setJoined(serialNumber) //send the joined notification to smart-vase
                sendResponse(`joined;${serialNumber};${ping}`) //send joined notification to raspberry
            }
            break;
        }

        case ("refuse"): {
            let ping =deleteRequest(serialNumber)
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