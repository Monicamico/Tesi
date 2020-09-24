/**
 * Smart-vase
 * functions.ts 
 * @author Monica Amico  
 */

/*-------------------------------------------------------------*/
/**
 * @summary it feeds the vase and update the amount of water in the container
 */
function waters() {
    pins.digitalWritePin(DigitalPin.P2, 1)
    basic.pause(3000)
    pins.digitalWritePin(DigitalPin.P2, 0)
    amount_water = amount_water - single_water_amount 
}

/**
 * @summary to set the maximum humidity value
 * @param max (number) humidity value
 */
function setHumMax(max: number) {
    if (max >= 0 && max <= 1023){
        hum_max = max
        radio.sendValue(OPERATION.SET_HUMIDITY_MAX.toString(),max)
    } 
}

/**
 * @summary to set the minimum humidity value
 * @param min (number) humidity value
 */
function setHumMin(min: number) {
    if (min >= 0 && min <= 1023){
        hum_min = min
        radio.sendValue(OPERATION.SET_HUMIDITY_MIN.toString(),min)
    }
        
}

/**
 * @summary to set the maximum temperature value
 * @param max (number) temperature value
 */
function setTempMax(max: number) {
    temp_max = max 
    radio.sendValue(OPERATION.SET_TEMPERATURE_MAX.toString(),max)
}

/**
 * @summary to set the minimum temperature value
 * @param min (number) temperature value
 */
function setTempMin(min: number) {
    temp_min = min
    radio.sendValue(OPERATION.SET_TEMPERATURE_MIN.toString(),min)
}

/**
 * @summary to set the minimum light value
 * @param min (number) light value
 */
function setLightMin(min: number) {
    if (min >= 0 && min <= 255){
        light_min = min;
        radio.sendValue(OPERATION.SET_LIGHT_MIN.toString(),min)
    }
}

/**
 * @summary to set the maximum light value
 * @param max (number) light value
 */
function setLightMax(max: number) {
    if (max >= 0 && max <= 255){
        light_max = max;
        radio.sendValue(OPERATION.SET_LIGHT_MAX.toString(),max)
    }
}

/**
 * @summary to set the maximum light value to water the plant
 * @param x (number) light value
 */
function setWateringLight(x: number) {
    if (x >= 0 && x <= 255){
        watering_light = x;
        radio.sendValue(OPERATION.SET_WATERING_LIGHT.toString(),x)
    }
}


function setWaterContainerFull(b: boolean) {
    water_container_full = b
    if (b == true){
        amount_water = water_container_size - single_water_amount
        if (joined)
            radio.sendValue(OPERATION.WATER_CONTAINER_STATE.toString(), WaterContainerState.Full)
    }
    else {
        amount_water = 0
        if (joined) 
            radio.sendValue(OPERATION.WATER_CONTAINER_STATE.toString(), WaterContainerState.Empty)
    }
}

function setWaterContainerSize(l: string) {
    water_container_size = parseFloat(l)
    if (amount_water > water_container_size)
        amount_water = water_container_size
    radio.sendValue(OPERATION.SET_WATER_CONTAINER_SIZE.toString(),water_container_size)
    
}

function setTransmitPower(x: number) {
    radio.setTransmitPower(x)
    radio.sendValue(OPERATION.VASE_TRANSMIT_POWER.toString(),x)
}


/**
 * @summary set time interval in wich the vase sends data to the radio-dashboard
 * @param x (number) interval
 */
function setSendTime(x: number) {
    if (x > 0){
        send_time = x * 60* 1000
        setPauseTime()
        radio.sendValue(OPERATION.SET_VASE_SEND_TIME.toString(), x)
    }
}

/**
 * @summary set pause time interval 
 */
function setPauseTime() {
    pause_time = send_time / 2
}

/**
 * @summary read humidity using pins P1, P0
 */
function readHumidity() {
    let i=0
    let humidity = 0
    pins.analogWritePin(AnalogPin.P1, 1023)
    humidity = pins.analogReadPin(AnalogPin.P0)
    pins.analogWritePin(AnalogPin.P1, 0)
    basic.showNumber(humidity)
    humidity_measure = humidity
    return humidity
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
    setState()
}

/**
 * @summary sends the temperature value to the radio-dashboard
 */
function sendTemperature() {
    readTemperature()
    radio.sendValue(OPERATION.TEMPERATURE.toString(), temperature_measure)
    basic.pause(3000)
}

/**
 * @summary sends the humidity value to the radio-dashboard
 */
function sendHumidity() {
    radio.sendValue(OPERATION.HUMIDITY.toString(), (readHumidity())/4)
    basic.pause(3000)
}

/**
 * @summary sends the light value
 */
function sendLight() {
    readLight()
    radio.sendValue((OPERATION.LIGHT).toString(), light_measure)
    basic.pause(3000)
}

function sendWaterContainerState() {
    if (water_container_full)
        radio.sendValue(OPERATION.WATER_CONTAINER_STATE.toString(),WaterContainerState.Full)
    else 
    radio.sendValue(OPERATION.WATER_CONTAINER_STATE.toString(),WaterContainerState.Empty)
    basic.pause(2000)
}

function setState() {
    
    if ((humidity_measure <= hum_max && humidity_measure >= hum_min) && 
        (light_measure <=light_max && light_measure >= light_min) &&
        (temperature_measure <= temp_max && temperature_measure >= temp_min))
        
        currentState = State.Happy
    else 
        currentState = State.Sad

}

function getRandomIntInclusive() {
    return Math.floor(Math.random() * (400 - 100 + 1)) + 100; //Il max è incluso e il min è incluso 
  }

/*------------------------------------------ END FUNCTIONS ----------------------------------------*/