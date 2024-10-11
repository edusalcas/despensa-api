import { Injectable } from '@angular/core';
@Injectable({
    providedIn: 'root'  // Proveer el servicio globalmente
})

export class LogService {
    log(msg: any) {
        console.log(new Date().toLocaleString() + ": " + JSON.stringify(msg));
    }
}