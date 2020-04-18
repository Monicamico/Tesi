/**
 * Radio-dashboard
 * classes.ts
 * @author Monica Amico 
 */


let DEBUG = true

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
    SET_RADIO_PAUSE_TIME = "srp",
    SET_RADIO_DIEDPING_TIME = "sdp"
};