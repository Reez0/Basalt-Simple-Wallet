import { CommonModule } from '@angular/common';
import { Component, OnInit, TemplateRef, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NgbModal, ModalDismissReasons } from '@ng-bootstrap/ng-bootstrap';
import { CoreService } from './core.service';
import { AccountResponse } from './interfaces';
import { HttpClientModule } from '@angular/common/http';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule, HttpClientModule, ReactiveFormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  title: string = 'basalt-simple-wallet';
  isLoggedIn: boolean = false;
  private modalService = inject(NgbModal);
	closeResult = '';
  accountData: AccountResponse | null = null;
  loginForm: FormGroup;
  accountForm: FormGroup;
  debitAccountForm: FormGroup;

  constructor(private coreService: CoreService, private formBuilder: FormBuilder) {
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
    this.accountForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
    this.debitAccountForm = this.formBuilder.group({
      address: ['GCLC3KNRNMQB3DGRSTBYUG6QRLZNEO4QTILVDPHIR3BWYBUHBA5UBFPV', [Validators.required]],
      transactionNote: ['', [Validators.required]],
      amount: ['', [Validators.required, Validators.pattern(/^\d+(\.\d{1,2})?$/)]]
    });
  }

  openLogin(content: TemplateRef<any>) {
		this.modalService.open(content, { ariaLabelledBy: 'loginModal' })
	}

  openCreateAccount(content: TemplateRef<any>) {
		this.modalService.open(content, { ariaLabelledBy: 'createAccountModal' })
	}

  openDebitAccount(content: TemplateRef<any>) {
    this.modalService.open(content, { ariaLabelledBy: 'debitAccountModal' })
  }


  ngOnInit() {
    if (localStorage.getItem('token')) {
      this.isLoggedIn = true;
      this.coreService.getAccountData().subscribe(result => {
        if (result.success) {
          this.accountData = result;
          console.log(this.accountData)
        } else {
          alert(result.message);
        }

      })
    }
  }

  onSubmitLogin() {
    if (this.loginForm.valid) {
      const { email, password } = this.loginForm.value;
      this.coreService.onLogin(email, password).subscribe((result => {
        if (result.success) {
          alert(result.message)
          localStorage.setItem('token', result.data.token);
          this.modalService.dismissAll();
          this.ngOnInit();
        } else {
          alert(result.message)
        }
      }))
    }
  }

  onSubmitCreateAccount() {
    if (this.accountForm.valid) {
      const { email, password, firstName, lastName } = this.accountForm.value;
      this.coreService.onCreateAccount(email, password, firstName, lastName).subscribe((result => {
        if (result.success) {
          this.modalService.dismissAll();
          alert(result.message);
        } else {
          alert(result.message)
        }
      }))
    }
  }

  creditAccount() {
    let creditAccountPrompt = confirm('Your account will be credited with 100 XLM').valueOf()
    if (creditAccountPrompt) {
      this.coreService.onCreditAccount().subscribe(result => {
        console.log(result)
        if (result.success) {
          alert(result.message)
          this.ngOnInit();
        } else {
          alert(result.message)
        }
      })
    }
  }

  onDebitAccount() {
    if (this.debitAccountForm.valid) {
      const { amount, transactionNote, address } = this.debitAccountForm.value;
      this.coreService.onDebitAccount(address, transactionNote, amount).subscribe((result => {
        if (result.success) {
          this.modalService.dismissAll();
          alert(result.message);
          this.ngOnInit()
        } else {
          alert(String(result.message))
        }
      }))
    }
  }


}
