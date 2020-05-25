/**
 * smart-vase
 * main.ts 
 * @author Monica Amico  
 */


enum State {
    Sad,
    Happy
}

enum WaterContainerState {
    Full = 1,
    Empty = 0
}

enum OPERATION {
    JOINED = 0, //j
    REFUSED = 1, //r
    PING = 2,
    HUMIDITY = 3,
    TEMPERATURE = 4,
    LIGHT = 5,
    WATER = 6,
    SET_HUMIDITY_MIN = 7,
    SET_HUMIDITY_MAX = 8,
    SET_TEMPERATURE_MIN = 9,
    SET_TEMPERATURE_MAX = 10,
    SET_LIGHT_MAX = 11,
    SET_LIGHT_MIN = 12,
    SET_VASE_PAUSE_TIME = 13,
    SET_VASE_SEND_TIME = 14,
    CONNECTION = 17,
    DELETED = 18,
    SET_WATERING_LIGHT = 19,
    SET_WATER_CONTAINER_SIZE = 20,
    WATER_CONTAINER_STATE = 21,
    VASE_TRANSMIT_POWER = 24
}

let currentState = State.Happy
let serial_number = control.deviceSerialNumber()  // serial number of the vase
let DEBUG = true
let single_water_amount = 0.02
/*
 * signal strength:
 * the value ranges from -128 to -42 
 * (-128 means a weak signal and -42 means a strong one.) 
 */
let min_signal_strenght = -120