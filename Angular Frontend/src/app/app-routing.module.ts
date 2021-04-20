import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { Step1Component } from './step1/step1.component'
import { Step2Component } from './step2/step2.component'

const routes: Routes = [
  { path: '', component: Step1Component },
  { path: 'Assumptions', component: Step2Component }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
