/**
 * Radio-dashboard
 * functions.ts
 * @author Monica Amico 
 */

/*------------------------------------- FUNCTIONS ---------------------------------------*/

/**
 * @summary the function getVase returns the vase with serial number equal to id. 
 *           if the vase does not exist returns undefined
 * @param id (number) the serial number of the vase.
 * @return the vase with serial number equal to id.
*/
function getVase(id: number, vase_list: Vase[]): Vase {
    if (!id || !vase_list) return undefined;
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
function insertVase(id: number, p:number, vase_list: Vase[]): number {
    if (!id) return undefined;
    let dim_list = vase_list.length
    let v = getVase(id,vase_list)
    if (v!= undefined) return dim_list
    if (dim_list == 24)
        return undefined;
    const vase: Vase = new Vase(id, p)
    if (!vase) return undefined;
    //add a new plot that rappresents the new vase
    led.plot(dim_list % 5, dim_list / 5)
    //insert the new vase in the list
    vase_list.push(vase)
    dim_list = vase_list.length
    return dim_list;
}

/**
 * @summary the function delete the vase with serial number equal to id into the list.
 * @param id (number) the serial number of the vase.
 * @returns lenght of the new list or undefined
*/
function deleteVase(id:number, vase_list: Vase[]): number{
    if (!id) return undefined;
    let i = 0
    let dim_list = vase_list.length
    while (i < dim_list){
        let vase = vase_list.shift()
        if (vase.getSerial() != id)
            vase_list.push(vase)
        else {
            led.unplot(dim_list % 5, dim_list / 5)
            dim_list = vase_list.length
            return dim_list;
        }
        i++;
    }
    
}

/**
 * @summary the function check if the connection request has already been received
 * @param id the serial number of the vase.
 * @param conn_request the list of requests
 * @return true if the list contains the request, false otherwise
*/
function containRequest(id: number, conn_request: Request[]):boolean {
    for (const r of conn_request){
        if (r.serial_number == id) return true;
    }
    return false;
}


function deleteRequest(id:number, conn_request: Request[]): number {
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
function drawNumberOfVases(dim_list:number) {
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
 * @summary to send a response to raspberry
 * @param response contains a string that rappresent the response
 */
function sendResponse(response: string){
    serial.writeString(response)
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
