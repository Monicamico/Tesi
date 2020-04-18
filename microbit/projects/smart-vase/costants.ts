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
    JOINED = "j",
    REFUSED = "r",
    PING = "p",
    HUMIDITY = "h",
    TEMPERATURE = "t",
    LIGHT = "l",
    WATER = "w",
    SET_HUMIDITY_MIN = "hm",
    SET_HUMIDITY_MAX = "hM",
    SET_TEMPERATURE_MIN = "tm",
    SET_TEMPERATURE_MAX = "tM",
    SET_LIGHT_MAX = "lM",
    SET_LIGHT_MIN = "lm",
    SET_VASE_PAUSE_TIME = "pt",
    SET_VASE_SEND_TIME = "st",
};

let currentState = State.Happy;
let serial_number = control.deviceSerialNumber()  // serial number of the vase
let DEBUG = true;
