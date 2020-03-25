/**
 * GioVase 
 * @author Monica Amico  
 */

/*----------------------------------------- VARIABLE STATEMENTS --------------------------------------*/

let serial_number = control.deviceSerialNumber()  // serial number of the vase
let temp_min = 15                                 // minimum temperature value
let temp_max = 30                                 // maximum temperature value
let hum_max = 1000                                // maximum humidity value
let hum_min = 300                                 // minimum humidity value
let light_min = 0
let light_max = 255
let temperature_measure = 0                       // temperature measure
let humidity_measure = 0                          // humidity measure
let light_measure = 0                             // light measure
let send_time = 500                               // time interval in wich the vase sends data    
let pause_time = 300000
let time = 0
let joined = false;
let radio_serial_number = 0;

enum State {
    Happy,
    Sad
}
let currentState = State.Happy;
/*------------------------------------------- FUNCTIONS -----------------------------------------------*/
/**
 * @summary it feeds the vase
 */
function waters() {
    pins.digitalWritePin(DigitalPin.P2, 1)
    basic.pause(4000)
    pins.digitalWritePin(DigitalPin.P2, 0)
}

/**
 * @summary to set the maximum humidity value
 * @param max (number) humidity value
 */
function setHumMax(max: number) {
    if (max >= 0 && max <= 1023)
        hum_max = max
}

/**
 * @summary to set the minimum humidity value
 * @param min (number) humidity value
 */
function setHumMin(min: number) {
    if (min >= 0 && min <= 1023)
        hum_min = min
}

/**
 * @summary to set the maximum temperature value
 * @param max (number) temperature value
 */
function setTempMax(max: number) {
    temp_max = max
}

/**
 * @summary to set the minimum temperature value
 * @param min (number) temperature value
 */
function setTempMin(min: number) {
    temp_min = min
}

function setLightMin(min: number) {
    if (min >= 0 && min <= 255)
        light_min = min;
}

function setLightMax(max: number) {
    if (max >= 0 && max <= 255)
        light_max = max;
}

/**
 * @summary set time interval in wich the vase sends data to the radio-dashboard
 * @param x (number) interval
 */
function setSendTime(x: number) {
    send_time = x
}

/**
 * @summary set pause time interval 
 * @param x (number) 
 */
function setPauseTime(x: number) {
    pause_time = x
}

/**
 * @summary read humidity using pins P1, P0
 */
function readHumidity() {
    pins.analogWritePin(AnalogPin.P1, 1)
    humidity_measure = pins.analogReadPin(AnalogPin.P0)
    pins.analogWritePin(AnalogPin.P1, 0)
}

/**
 * @summary read temperature
 */
function readTemperature() {
    temperature_measure = input.temperature()
}

/**
 *@summary read light 
 */
function readLight() {
    light_measure = input.lightLevel()
}

/**
 * @summary read temperature, humidity and light
 */
function measure() {
    readHumidity()
    readTemperature()
    readLight()
}

/**
 * @summary sends the temperature value to the radio-dashboard
 */
function sendTemperature() {
    radio.sendValue("getTemp", temperature_measure)
    basic.pause(1000)
}

/**
 * @summary sends the humidity value to the radio-dashboard
 */
function sendHumidity() {
    radio.sendValue("getHum", humidity_measure)
    basic.pause(1000)
}

/**
 * @summary sends the light value
 */
function sendLight() {
    radio.sendValue("getLight", light_measure)
    basic.pause(1000)
}

function setState() {
    if ((humidity_measure <= hum_max && humidity_measure >= hum_min) && 
        (light_measure <=light_max && light_measure >= light_min) &&
        (temperature_measure <= temp_max && temperature_measure >= temp_min))
        
        currentState = State.Happy;
    else 
        currentState = State.Sad
}
/*------------------------------------------ END FUNCTIONS ----------------------------------------*/

/*------------------------------------------- INITIAL CODE ----------------------------------------*/

serial_number = control.deviceSerialNumber()
radio.setTransmitSerialNumber(true)
radio.setGroup(18)
led.setBrightness(20)

/*-------------------------------------------- VASE CODE ------------------------------------------*/

basic.forever(function () {

    if (joined == false) {
        radio.sendString("join")
    }
    
    measure()
    setState()

    if (currentState == State.Happy)
        basic.showIcon(IconNames.Happy)
    else 
        basic.showIcon(IconNames.Sad)

    if (humidity_measure < hum_min) {
        basic.showLeds(`
            . . # . .
            . . # . .
            # # # # #
            . # # # .
            . . # . .
        `)
        waters()
    }
    basic.clearScreen()
    basic.pause(pause_time)
    
    time += 1
    if (time == send_time) {
        basic.showString("->")
        sendHumidity()
        basic.pause(2000)
        sendTemperature()
        basic.pause(2000)
        sendLight()
        basic.pause(2000)
        time = 0;
    }
})

/*------------------------------------------- EVENTS CODE ------------------------------------------*/

radio.onReceivedBuffer(function () {

    const content = radio.lastPacket.bufferPayload.toString()
    const content_list: string[] = content.split(";")

    let size = content_list.length
    let request;
    let id = 0;
    let x;

    if (size <= 1) return;
    if (size == 2) {
        request = content_list[0]
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
        basic.clearScreen()

        switch (request) {
            case ("joined"): {
                joined = true;
                radio_serial_number = radio.receivedPacket(RadioPacketProperty.SerialNumber)
                basic.clearScreen()
                break
            }
            case ("ping"): {
                /* if a ping request arrives
                 the smart-vase is certainly present in the vaselist of the radio */
                joined = true; 
                radio.sendString("ping") 
                break
            }
            case ("water"): {
                waters()
                break
            }
            case ("getHum"): {
                sendHumidity()
                break
            }
            case ("getTemp"): {
                sendTemperature()
                break
            }
            case ("getLight"): {
                sendLight()
                break
            }
            case ("pause_time"): {
                setPauseTime(x)
                break
            }
            case ("send_time"): {
                setSendTime(x)
                break
            }
            case ("hum_min"): {
                setHumMin(x)
                break
            }
            case ("hum_max"): {
                setHumMax(x)
                break
            }
            case ("temp_min"): {
                setTempMin(x)
                break
            }
            case ("temp_max"): {
                setTempMax(x)
                break
            }
            case ("light_min"): {
                setLightMin(x)
                break
            }
            case ("light_max"): {
                setLightMax(x)
                break
            } 
        }
    }
})

input.onButtonPressed(Button.A, function(){
    basic.showNumber(humidity_measure) //humidity
    basic.pause(1000)
    basic.showNumber(temperature_measure)
    basic.pause(1000)
    basic.showNumber(light_measure)
})
