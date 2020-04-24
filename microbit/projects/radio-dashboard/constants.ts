/**
 * Radio-dashboard
 * classes.ts
 * @author Monica Amico 
 */


let DEBUG = true

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
    SET_RADIO_PAUSE_TIME = 15,
    SET_RADIO_DEADPING_TIME = 16,
    CONNECTION = 17,
    DELETED = 18,
    SET_WATERING_LIGHT = 19,
    SET_WATER_CONTAIER_SIZE = 20,
    SET_WATER_CONTAINER_FULL = 21
};