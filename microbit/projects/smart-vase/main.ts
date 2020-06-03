/**
 * smart-vase
 * main.ts 
 * @author Monica Amico  
 */

/* ----------------------------------------- VARIABLE STATEMENTS --------------------------------------- */

let temp_min = 15                                 // minimum temperature value
let temp_max = 30                                 // maximum temperature value
let hum_max = 1000                                // maximum humidity value
let hum_min = 300                                 // minimum humidity value
let light_min = 50
let light_max = 250
let temperature_measure = 0                       // temperature measure
let humidity_measure = 0                          // humidity measure
let light_measure = 0                             // light measure
let send_time = 900000                            // time interval in wich the vase sends data  (16 MINUTI circa)
let pause_time = send_time / 2                       
let time = 0
let joined = false
let radio_serial_number = 0
let watering_light = 70
let water_container_size = 0.5                    // in liters (default 0.5 liter)
let water_container_full = true                     
let amount_water = 0.5
let transmit_power = 5                             // range = (0...7) lower to upper


/* ------------------------------------------- INITIAL CODE ------------------------------------------- */

radio.setTransmitSerialNumber(true)
radio.setGroup(18)
led.setBrightness(20)
radio.setTransmitPower(transmit_power)
let pairing_number = getRandomIntInclusive()
amount_water = water_container_size
amount_water -=  single_water_amount
// problema: anche se e' presente ancora acqua nel contenitore non riesce a prenderla perche' troppo poca.
// considero un waters() in meno 

DEBUG = true 

/*---------------------------------------------- MAIN CODE ------------------------------------------- */

basic.forever(function () {

    if (!joined) 
        radio.sendValue(OPERATION.CONNECTION.toString(), pairing_number)
    measure()
    setState()
    if (currentState == State.Happy)
        basic.showIcon(IconNames.Happy)
    else
         basic.showIcon(IconNames.Sad)
    if (humidity_measure < hum_min && light_measure <= watering_light && water_container_full){
        if (amount_water >= single_water_amount)
            waters() //feeds the plant and update the amount_water
        if (amount_water < single_water_amount){
            setWaterContainerFull(false)
            basic.showString('!')
        }     
    }
    basic.clearScreen()
    if (time >= send_time) {
        if (joined){
            basic.showString(">")
            sendHumidity()
            sendTemperature()
            sendLight()
            basic.clearScreen()
        }
        time = 0
    } 
    basic.pause(pause_time)
    time += pause_time
})

/*------------------------------------------- EVENTS CODE ------------------------------------------*/

radio.onReceivedBuffer(function () {

    const serial_packet = radio.receivedPacket(RadioPacketProperty.SerialNumber)
    const signal_strenght = radio.receivedPacket(RadioPacketProperty.SignalStrength)
    const content = radio.lastPacket.bufferPayload.toString()
    const content_list: string[] = content.split(";")
    let size = content_list.length

    basic.showLeds(`
        # # # # #
        # # . # #
        # . # . #
        # . . . #
        # # # # #
    `)

    let request = 0
    let id = 0
    let x = 0

    if (size <= 1) return
    if (size >= 2) {
        request = parseInt(content_list[0])
        id = parseInt(content_list[1])
    }
    if (size == 3)
        x = parseInt(content_list[2])
    
    if (id == serial_number || id == -1) {

        if (request == OPERATION.JOINED) {
            /**
             * min_signal_strength = -100
             * the signal stranght value ranges from -128 to -42 
             * (-128 means a weak signal and -42 means a strong one.) 
             */
            if(!joined && signal_strenght > min_signal_strenght) {
                joined=true
                radio_serial_number = serial_packet
                setPauseTime()
                basic.showString('j')
                radio.sendValue(OPERATION.JOINED.toString(),radio_serial_number)
            } 
            
        } else if (request == OPERATION.PING) 
            radio.sendNumber(OPERATION.PING)

        //checking if the operation has been requested from the radio
        if (serial_packet == radio_serial_number) {

            //Join operation failed or the vase has been deleted from the list
            if (request == OPERATION.DELETED){
                if (joined){
                    joined = false
                    pairing_number = getRandomIntInclusive()
                    pause_time = 1200000
                }
            } 

            if (request == OPERATION.REFUSED){
                if (joined) {
                    joined = false
                    pause_time = 1200000
                }
            } 
            
            else if (request == OPERATION.WATER) {
                if ( amount_water >= single_water_amount )
                    waters()
                else if (amount_water < single_water_amount){
                    setWaterContainerFull(false)
                    basic.showString('!')
                }     
            }
            
            else if (request == OPERATION.HUMIDITY)
                sendHumidity()

            else if (request == OPERATION.TEMPERATURE)
                sendTemperature()   

            else if (request == OPERATION.LIGHT)
                sendLight()
            
            else if (request == OPERATION.WATER_CONTAINER_STATE) 
                sendWaterContainerState()
    
            else if (request == OPERATION.SET_VASE_SEND_TIME && size == 3)
                setSendTime(x)

            else if (request == OPERATION.VASE_TRANSMIT_POWER && size == 3)
                setTransmitPower(x)
            
            else if (request == OPERATION.SET_HUMIDITY_MIN && size == 3)
                setHumMin(x)

            else if (request == OPERATION.SET_HUMIDITY_MAX && size == 3)
                setHumMax(x)

            else if (request == OPERATION.SET_TEMPERATURE_MIN && size == 3)
                setTempMin(x)

            else if (request == OPERATION.SET_TEMPERATURE_MAX && size == 3)
                setTempMax(x)
    
            else if (request == OPERATION.SET_LIGHT_MIN && size == 3)
                setLightMin(x)
        
            else if (request == OPERATION.SET_LIGHT_MAX && size == 3)
                setLightMax(x)

            else if (request == OPERATION.SET_WATERING_LIGHT && size == 3)
                setWateringLight(x)

            else if (request == OPERATION.SET_WATER_CONTAINER_SIZE && size == 3)
                setWaterContainerSize(content_list[2])                
            
        }   
    }
    basic.clearScreen()
       
})

input.onButtonPressed(Button.A, function(){
    if (joined){
        basic.showString('>')
        sendHumidity()
        sendLight()
        sendTemperature()
    } else
        basic.showNumber(pairing_number)
})

input.onButtonPressed(Button.B, function(){
    setWaterContainerFull(true)
})

//to show the pairing number
input.onButtonPressed(Button.AB, function(){
    basic.showNumber(pairing_number)
})