import { Component, inject, Input, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Documento } from '../../types/documento';
import { DocumentoFormService } from '../../services/documento-form.service';

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
  documentoFormService = inject(DocumentoFormService);

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
    const saved = this.documentoFormService.saveDocumento(this.documentoForm, this.selectedDocumento);
    if (saved) {
      this.clearForm();
      this.documentoSaved.emit();
    }
  }

  clearForm() {
    this.documentoFormService.clearForm(this.documentoForm);
    this.formCleared.emit();
  }
}
