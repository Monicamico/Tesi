/**
 * Radio-dashboard
 * @author Monica Amico  
 */

/*-------------------------------- VASE CLASS ----------------------------------*/
class Vase {
    serial_number: number;    // serial number of the vase
    temp: number;             // temperature value of the vase
    hum: number;              // humidity value of the vase
    light: number;
    ping: number;             // ping

    constructor(id: number) {
        if (id) {
            this.serial_number = id;
            this.temp = 0;
            this.light = 0;
            this.hum = 0;
            this.ping = input.runningTime()
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
/*--------------------------------- VARIABLE STATEMENTS --------------------------------*/

const vase_map: Vase[] = [];           // list of vases
const conn_request: number[] = [];      // list of connection requests
let dim_list: number = 0;               // size of vase_map
let pause_time = 8000

/*------------------------------------- FUNCTIONS ---------------------------------------*/

/**
 * @summary the function getVase returns the vase with serial number equal to id. 
 *           if the vase does not exist returns undefined
 * @param id (number) the serial number of the vase.
 * @return the vase with serial number equal to id.
*/
function getVase(id: number): Vase {
    if (!id)
        return undefined
    //to search the vase in the list
    for (const vase of vase_map) {
        if (vase.getSerial() == id)
            return vase;
    }
    return undefined;
}

/**
 * @summary the function insert the vase, with serial number equal to id, into the list.
 * @param id (number) the serial number of the vase.
 * @return the vase with serial number equal to id or undefined.
*/
function insertVase(id: number): Vase {

    if (!id) return undefined;

    for (const vase of vase_map) {
        if (vase.getSerial() == id)
            return vase;
    }

    dim_list = vase_map.length
    if (dim_list == 25)
        return undefined;

    const vase: Vase = new Vase(id)
    if (!vase) return undefined;

    //add a new plot that rappresents the new vase
    led.plot(dim_list % 5, dim_list / 5)
    //insert the new vase in the list
    vase_map.push(vase)
    dim_list += 1
    return vase;
}

function containRequest(id:number):boolean {
    for (const n of conn_request){
        if (n == id) return true;
    }
    return false;
}

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
 * @summary send temperature request to the vase with serial number equal to the parameter id.
 *          if the param is 0 the request will be send to all.
 * @param id (number) rappresents the serial number of the vase.
 */
function getTemp(id: number) {
    sendRequest("getTemp",id)
}

/**
 * @summary send humidity request to the vase with serial number equal to the parameter id.
 *          if the param is 0 the request will be send to all.
 * @param id (number) rappresents the serial number of the vase.
 */
function getHum(id: number) {
    sendRequest("getHum", id)
}

/**
 * @summary send light request to the vase with serial number equal to the parameter id.
 *          if the param is 0 the request will be send to all.
 * @param id (number) rappresents the serial number of the vase.
 */
function getLight(id: number) {
    sendRequest("getLight", id)
}

/**
 * @summary send the request to water the vase
 *          if the param is 0 the request will be send to all.
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

/*------------------------------------- INITIAL CODE -------------------------------------*/
led.setBrightness(50)
radio.setTransmitSerialNumber(true)
radio.setGroup(18)
radio.setTransmitPower(7)
dim_list = vase_map.length

/*--------------------------------------- RADIO CODE -------------------------------------*/
basic.forever(function () {
    basic.pause(pause_time)
})

/*--------------------------------------- EVENTS CODE ------------------------------------*/


//to accept the last request
input.onButtonPressed(Button.A, function () {
    let id = conn_request.pop()
    insertVase(id)
    sendRequest("joined",id)
})

//to refuse the last request
input.onButtonPressed(Button.B, function () {
    conn_request.pop()
})

input.onButtonPressed(Button.AB, function() {

})

//code to be executed when a connection request is recived
radio.onReceivedString(function (receivedString: string) {
    const serialNumber = radio.receivedPacket(RadioPacketProperty.SerialNumber)
    if (receivedString == "join"){
        if (containRequest(serialNumber)) return;
        conn_request.push(serialNumber)
    }/* else if (receivedString == "ping"){
        const v:Vase = getVase(serialNumber)
        if (v) v.setPing(input.runningTime())
    }*/
    
})


//code to be executed when a value is received
radio.onReceivedValue(function (request: string, param: number) {

    const serialNumber = radio.receivedPacket(RadioPacketProperty.SerialNumber)
    const vase = getVase(serialNumber)
    if (!vase) return;

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
