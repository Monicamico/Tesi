/**
 * Radio-dashboard
 * classes.ts
 * @author Monica Amico 
 */

/*-------------------------------- VASE CLASS ----------------------------------*/
class Vase {

    serial_number: number;    // serial number of the vase
    temp: number;             // temperature value of the vase
    hum: number;              // humidity value of the vase
    light: number;
    ping: number;             // ping
    dying: boolean;

    constructor(id: number, ping: number) {
        if (id) {
            this.serial_number = id;
            this.temp = 0;
            this.light = 0;
            this.hum = 0;
            this.ping = ping
            this.dying = false;
        }
    }

    /**
     * @summary changes the temperature value of the vase
     * @param temp_vase (number) rappresenting the temperature of the vase
     */
    setTemperature(temp_vase: number) {
        this.temp = temp_vase
        this.ping = input.runningTime()
    }

    /**
     * @summary changes the humidity value of the vase
     * @param hum_vase (number) rappresenting the humidity of the vase
     */
    setHumidity(hum_vase: number) {
        this.hum = hum_vase
        this.ping = input.runningTime()
    }

    /**
     * @summary changes the light value of the vase
     * @param light_vase (number) rappresenting the light of the vase
     */
    setLight(light_vase: number) {
        this.light = light_vase
        this.ping = input.runningTime()
    }

    /**
     * @summary to get the serial number of the vase
     * @returns the serial number
     */
    getSerial() {
        return this.serial_number
    }

    getPing(){
        return this.ping
    }

    setPing(ping:number){
        this.ping = ping;
    }
}

class Request {
    serial_number: number
    ping: number

    constructor(s:number, ping:number){
        this.serial_number = s
        this.ping = ping;
    }
}

