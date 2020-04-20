/**
 * Smart-vase
 * functions.ts 
 * @author Monica Amico  
 */

/*-------------------------------------------------------------*/
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
    radio.sendValue(OPERATION.TEMPERATURE.toString(), temperature_measure)
    basic.pause(1000)
}

/**
 * @summary sends the humidity value to the radio-dashboard
 */
function sendHumidity() {
    radio.sendValue(OPERATION.HUMIDITY.toString(), humidity_measure)
    basic.pause(1000)
}

/**
 * @summary sends the light value
 */
function sendLight() {
    radio.sendValue((OPERATION.LIGHT).toString(), light_measure)
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