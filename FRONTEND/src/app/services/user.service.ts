import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { User } from '../models/user.model';
import { Login } from '../models/login.model';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  

  constructor(private http: HttpClient, private router: Router) { }

  auth(craidnial: Login){
    return this.http.post("http://127.0.0.1:5001/login", craidnial)
  }

  logout(): Observable<any> {
    return this.http.post("http://127.0.0.1:5001/logout", {}).pipe(
      tap(() => {
        // Clear client-side data regardless of server response success
        //localStorage.removeItem('user_token'); // Or whatever key you use
        // Redirect the user to the login page after logout
        this.router.navigate(['/login']);
      })
    );
  }
}
