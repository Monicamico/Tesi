/**
 * Radio-dashboard
 * classes.ts
 * @author Monica Amico 
 */

/*-------------------------------- VASE CLASS ----------------------------------*/
class Vase {

    serial_number: number;    // serial number of the vase
    ping: number;             // ping
    dying: boolean;

    constructor(id: number, ping: number) {
        if (id) {
            this.serial_number = id;
            this.ping = ping
            this.dying = false;
        }
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

