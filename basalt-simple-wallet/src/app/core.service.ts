import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AccountResponse, AuthResponse, CreateAccountResponse } from './interfaces';

@Injectable({
  providedIn: 'root'
})
export class CoreService {

  private apiUrl = 'http://localhost/api';

  constructor(private httpClient: HttpClient) { }

  getAccountData(): Observable<AccountResponse> {
    const url = `${this.apiUrl}/dashboard/`;
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    });
    return this.httpClient.get<AccountResponse>(url,{headers});
  }

  onLogin(email: string, password: string): Observable<AuthResponse> {
    const url = `${this.apiUrl}/login/`;
    return this.httpClient.post<AuthResponse>(url, {email:email, password:password});
  }

  onCreateAccount(email: string, password: string, firstName: string, lastName: string): Observable<CreateAccountResponse> {
    const url = `${this.apiUrl}/create-account/`;
    return this.httpClient.post<CreateAccountResponse>(url, {email:email, password:password, first_name: firstName,last_name: lastName});
  }

  onCreditAccount(): Observable<CreateAccountResponse> {
    const url = `${this.apiUrl}/pay/credit/`;
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    });
    return this.httpClient.post<CreateAccountResponse>(url,{headers});
  }

  onDebitAccount(address: string, transactionNote: string, amount: string ) {
    const url = `${this.apiUrl}/pay/debit/`;
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    });
    return this.httpClient.post<CreateAccountResponse>(url, 
      {address: address, transaction_note: transactionNote, amount: Number(amount)}, {headers});
  }

}
