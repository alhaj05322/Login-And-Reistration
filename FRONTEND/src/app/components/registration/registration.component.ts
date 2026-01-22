import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import {Router, RouterModule } from "@angular/router";

@Component({
  selector: 'app-registration',
  imports: [RouterModule, ReactiveFormsModule, CommonModule],
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.css'
})
export class RegistrationComponent {


  userData: FormGroup = new FormGroup({
    name: new FormControl("", [Validators.required, Validators.minLength(3)]),
    email: new FormControl("", [Validators.required, Validators.email]),
    password: new FormControl("", [Validators.required, Validators.minLength(8)]),
    confirm: new FormControl("", [Validators.required, Validators.minLength(8)])
  })

  http = inject(HttpClient)
  router = inject(Router)

  onSave() {
    const data = this.userData.value
    this.http.post("http://127.0.0.1:5001/register", data).subscribe((res: any)=>{
      if(res.success){
        alert(res.message)
        this.router.navigate(['/login'])
      }
      else{
        alert(res.message)
      }
    })
  }

}
