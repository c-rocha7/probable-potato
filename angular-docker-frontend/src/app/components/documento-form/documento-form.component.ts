import { Component, inject, Input, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { DocumentoStore } from '../../store/documento-store';
import { Documento } from '../../types/documento';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-documento-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './documento-form.component.html',
  styleUrl: './documento-form.component.css',
})
export class DocumentoFormComponent implements OnChanges {
  @Input() selectedDocumento: Documento | null = null;
  @Output() documentoSaved = new EventEmitter<void>();
  @Output() formCleared = new EventEmitter<void>();

  formBuilder = inject(FormBuilder);
  documentoForm!: FormGroup;
  documentoStore = inject(DocumentoStore);
  toaster = inject(ToastrService);

  constructor() {
    this.documentoForm = this.formBuilder.group({
      name: ['', Validators.required],
      url_documento: ['', Validators.required],
      nome_signatario: ['', Validators.required],
      email_signatario: ['', [Validators.required, Validators.email]],
    });
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['selectedDocumento'] && this.selectedDocumento) {
      // Para edição, vamos pegar o primeiro signatário se existir
      const firstSigner = this.selectedDocumento.signers?.[0];

      this.documentoForm.patchValue({
        name: this.selectedDocumento.name,
        url_documento: '', // Este campo não existe no novo JSON, manter vazio
        nome_signatario: firstSigner?.name || '',
        email_signatario: firstSigner?.email || ''
      });
    }
  }

  save() {
    if (this.documentoForm.invalid) {
      this.toaster.error('Preencha os campos.');
      return;
    }

    let formValues = this.documentoForm.value;
    if (this.selectedDocumento) {
      formValues.id = this.selectedDocumento.id;
      this.documentoStore.updateDocumento(formValues);
    } else {
      this.documentoStore.addDocumento(formValues);
    }

    this.clearForm();
    this.documentoSaved.emit();
  }

  clearForm() {
    this.documentoForm.reset();
    this.formCleared.emit();
  }
}
