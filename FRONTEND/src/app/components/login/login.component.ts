import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, Inject, inject } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';



@Component({
  selector: 'app-login',
  imports: [RouterModule, ReactiveFormsModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  userForm: FormGroup = new FormGroup({
    email: new FormControl("", [Validators.required, Validators.email]),
    password: new FormControl("", [Validators.required, Validators.minLength(6)])
  })

  http = inject(HttpClient)
  router = inject(Router)


  constructor(){}

  onLogin(){
    const userData = this.userForm.value
    this.http.post("http://127.0.0.1:5001/login", userData).subscribe((res:any)=>{
      if(res.success){
        alert(res.message)
        this.router.navigate(['/dashboard'])
      }else{
        alert(res.message)
      }
    })
  }

}
