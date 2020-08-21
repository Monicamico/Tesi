from enum import Enum

URL_DASHBOARD = 'http://192.168.1.18:5000'
MICROBIT_PORT_MAC = '/dev/cu.usbmodem14102'   # right
MICROBIT_PORT_MAC2 = '/dev/cu.usbmodem14202'  # left
MICROBIT_PORT_LINUX = '/dev/ttyACM1'
MICROBIT_PORT_LINUX2 = '/dev/ttyACM0'
DELIMITER = '#'
PORT = 5000


class Operation(Enum):
    """

    Type of Operation Enum

    - JOINED = 0
    - REFUSED = 1
    - PING = 2
    - HUMIDITY = 3
    - TEMPERATURE = 4
    - LIGHT = 5
    - WATER = 6
    - SET_HUMIDITY_MIN = 7
    - SET_HUMIDITY_MAX = 8
    - SET_TEMPERATURE_MIN = 9
    - SET_TEMPERATURE_MAX = 10
    - SET_LIGHT_MAX = 11
    - SET_LIGHT_MIN = 12
    - SET_VASE_PAUSE_TIME = 13
    - SET_VASE_SEND_TIME = 14
    - SET_RADIO_PAUSE_TIME = 15
    - SET_RADIO_DIED_PING = 16
    - CONNECTION = 17
    - DELETED = 18
    - SET_WATERING_LIGHT = 19
    - SET_WATER_CONTAINER_SIZE = 20
    - WATER_CONTAINER_STATE = 21
    - RADIO_JOIN = 22
    - RADIO_TRANSMIT_POWER = 23
    - VASE_TRANSMIT_POWER = 24
    - ADD_EXISTING_VASE = 26

    """
    JOINED = 0
    REFUSED = 1
    PING = 2
    HUMIDITY = 3
    TEMPERATURE = 4
    LIGHT = 5
    WATER = 6
    SET_HUMIDITY_MIN = 7
    SET_HUMIDITY_MAX = 8
    SET_TEMPERATURE_MIN = 9
    SET_TEMPERATURE_MAX = 10
    SET_LIGHT_MAX = 11
    SET_LIGHT_MIN = 12
    SET_VASE_PAUSE_TIME = 13
    SET_VASE_SEND_TIME = 14
    SET_RADIO_PAUSE_TIME = 15
    SET_RADIO_DIED_PING = 16
    CONNECTION = 17
    DELETED = 18
    SET_WATERING_LIGHT = 19
    SET_WATER_CONTAINER_SIZE = 20
    WATER_CONTAINER_STATE = 21
    RADIO_JOIN = 22
    RADIO_TRANSMIT_POWER = 23
    VASE_TRANSMIT_POWER = 24
    ADD_EXISTING_VASE = 26


class WaterContainerState(Enum):
    """
    Water container state enum
    - Empty = 0
    - Full = 1
    """
    Empty = 0
    Full = 1