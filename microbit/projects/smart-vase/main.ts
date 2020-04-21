/**
 * smart-vase
 * main.ts 
 * @author Monica Amico  
 */

/*----------------------------------------- VARIABLE STATEMENTS --------------------------------------*/

let temp_min = 15                                 // minimum temperature value
let temp_max = 30                                 // maximum temperature value
let hum_max = 1000                                // maximum humidity value
let hum_min = 300                                 // minimum humidity value
let light_min = 0
let light_max = 255
let temperature_measure = 0                       // temperature measure
let humidity_measure = 0                          // humidity measure
let light_measure = 0                             // light measure
let send_time = 1000000                           // time interval in wich the vase sends data  (16 MINUTI)
let pause_time = 600000                           // 10 MINUTI
let time = 0
let joined = false
let radio_serial_number = 0


/*------------------------------------------- INITIAL CODE ----------------------------------------*/

radio.setTransmitSerialNumber(true)
radio.setGroup(18)
led.setBrightness(20)

DEBUG = true 

if (DEBUG) {
    pause_time = 100000 
    send_time =  100000 
} 

/*-------------------------------------------- VASE CODE ------------------------------------------*/

basic.forever(function () {

    if (joined == false) {
        radio.sendNumber(OPERATION.CONNECTION)
    }
    
    measure()
    setState()

    if (currentState == State.Happy)
        basic.showIcon(IconNames.Happy)
    else 
        basic.showIcon(IconNames.Sad)

    if (humidity_measure < hum_min) {
        waters()
    }

    basic.clearScreen()
    basic.pause(pause_time)
    
    time += pause_time
    if (time == send_time) {
        if (joined){
            basic.showString("->")
            sendHumidity()
            basic.pause(2000)
            sendTemperature()
            basic.pause(2000)
            sendLight()
            basic.pause(2000)
        }
        time = 0
    } 
})

/*------------------------------------------- EVENTS CODE ------------------------------------------*/

radio.onReceivedBuffer(function () {

    const content = radio.lastPacket.bufferPayload.toString()
    const content_list: string[] = content.split(";")

    let size = content_list.length
    let request = 0
    let id = 0
    let x = 0

    if (size <= 1) return
    if (size == 2) {
        request = parseInt(content_list[0])
        id = parseInt(content_list[1])
    }
    if (size == 3) x = parseInt(content_list[2])

    if (id == serial_number || id == -1) {

        basic.showLeds(`
        # # # # #
        # # . # #
        # . # . #
        # . . . #
        # # # # #
        `)
       
        if (request == OPERATION.JOINED) {
            if(!joined) {
                joined=true
                radio_serial_number= radio.receivedPacket(RadioPacketProperty.SerialNumber) 
            }   
        } else if (request == OPERATION.PING) {
            /* if a ping request arrives
               the smart-vase is certainly present in the vaselist of the radio */
            joined = true; 
            radio.sendNumber(OPERATION.PING)

        } else if (request == OPERATION.WATER) 
            waters()

        else if (request == OPERATION.HUMIDITY)
            sendHumidity()

        else if (request == OPERATION.TEMPERATURE)
            sendTemperature()   

        else if (request == OPERATION.LIGHT)
            sendLight()

        else if (request == OPERATION.SET_VASE_PAUSE_TIME)
            setPauseTime(x)
    
        else if (request == OPERATION.SET_VASE_SEND_TIME)
            setSendTime(x)
        
        else if (request == OPERATION.SET_HUMIDITY_MIN)
            setHumMin(x)

        else if (request == OPERATION.SET_HUMIDITY_MAX)
            setHumMax(x)

        else if (request == OPERATION.SET_TEMPERATURE_MIN)
            setTempMin(x)

        else if (request == OPERATION.SET_TEMPERATURE_MAX)
            setTempMax(x)
   
        else if (request == OPERATION.SET_LIGHT_MIN)
            setLightMin(x)
       
        else if (request == OPERATION.SET_LIGHT_MAX)
            setLightMax(x)
    }

    basic.clearScreen()
       
})

input.onButtonPressed(Button.A, function(){
    sendHumidity()
    basic.pause(1000)
    sendLight()
    basic.pause(1000)
    sendTemperature()
})
