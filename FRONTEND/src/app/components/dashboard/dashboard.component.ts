import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-dashboard',
  imports: [],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {

  http = inject(HttpClient)
  router = inject(Router)
  userService = inject(UserService)
  name: string = ""

  onLogout(): void {
    this.userService.logout().subscribe((res:any)=>{
      if(res.success){
        alert(res.message)
        this.router.navigate(['/login'])
      }
      else{
        alert(res.message)
      }
    })
  }
  
  // ngOnDestroy() {
  //   this.http.get("http://127.0.0.1:5001/get_user").subscribe((res:any)=>{
  //     if(res.success){
  //       this.name = res.message.name
  //     }
  //     else{
  //       alert(res.message)
  //     }

  //   })
   
  //}

}
