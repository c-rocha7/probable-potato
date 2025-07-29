// Exemplo de como reutilizar o DocumentoFormService em outro componente

import { Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DocumentoFormService } from '../services/documento-form.service';
import { Documento } from '../types/documento';

@Component({
  selector: 'app-exemplo-reutilizacao',
  template: `
    <!-- Seu template aqui -->
  `
})
export class ExemploReutilizacaoComponent {
  formBuilder = inject(FormBuilder);
  documentoFormService = inject(DocumentoFormService);

  meuFormulario: FormGroup;
  documentoSelecionado: Documento | null = null;

  constructor() {
    this.meuFormulario = this.formBuilder.group({
      name: ['', Validators.required],
      url_documento: ['', Validators.required],
      nome_signatario: ['', Validators.required],
      email_signatario: ['', [Validators.required, Validators.email]],
    });
  }

  // Reutilizando o método de save
  salvarDocumento() {
    const sucesso = this.documentoFormService.saveDocumento(
      this.meuFormulario,
      this.documentoSelecionado
    );

    if (sucesso) {
      // Ações adicionais após o salvamento
      console.log('Documento salvo com sucesso!');
      this.limparFormulario();
    }
  }

  // Reutilizando o método de limpar
  limparFormulario() {
    this.documentoFormService.clearForm(this.meuFormulario);
    // Ações adicionais após limpar
    this.documentoSelecionado = null;
  }
}
