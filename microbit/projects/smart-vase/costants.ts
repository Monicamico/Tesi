/**
 * smart-vase
 * main.ts 
 * @author Monica Amico  
 */


enum State {
    Happy,
    Sad
}


enum OPERATION {
    JOINED = 0, //j
    REFUSED = 1, //r
    PING = 2,
    HUMIDITY = 3,
    TEMPERATURE = 4,
    LIGHT = 5,
    WATER = 6,
    SET_HUMIDITY_MIN = 7, //hm
    SET_HUMIDITY_MAX = 8, //hM
    SET_TEMPERATURE_MIN = 9, //tm
    SET_TEMPERATURE_MAX = 10, //tM
    SET_LIGHT_MAX = 11, //lM
    SET_LIGHT_MIN = 12, //lm
    SET_VASE_PAUSE_TIME = 13, //pt
    SET_VASE_SEND_TIME = 14, //st
};

let currentState = State.Happy;
let serial_number = control.deviceSerialNumber()  // serial number of the vase
let DEBUG = true;
