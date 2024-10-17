import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, catchError } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class ChatService {

    private is_local: boolean = false;

    private localUrl: string = "http://localhost:5000/api";

    private apiUrl: string = "https://radiant.rarepath.ai/api";


    constructor(private http: HttpClient){}

    sendMessage(messagePayload: { userQuery: string, modelSelection: string, currentSummary: string }): Observable<any> {

      if (this.is_local) {
        this.apiUrl = this.localUrl;
      }
        const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
        return this.http.post<any>(this.apiUrl + '/get_response', messagePayload, { headers });
      }
}
