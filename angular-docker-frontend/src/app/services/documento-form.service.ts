import { inject, Injectable } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { DocumentoStore } from '../store/documento-store';
import { Documento } from '../types/documento';

@Injectable({
  providedIn: 'root'
})
export class DocumentoFormService {
  private documentoStore = inject(DocumentoStore);
  private toaster = inject(ToastrService);

  /**
   * Salva um documento (cria novo ou atualiza existente)
   * @param form - O FormGroup com os dados do formulário
   * @param selectedDocumento - O documento selecionado para edição (null para criar novo)
   * @returns boolean - true se salvou com sucesso, false se houve erro de validação
   */
  saveDocumento(form: FormGroup, selectedDocumento: Documento | null = null): boolean {
    if (form.invalid) {
      this.toaster.error('Preencha os campos.');
      return false;
    }

    const formValues = form.value;

    if (selectedDocumento) {
      // Modo edição
      formValues.id = selectedDocumento.id;
      this.documentoStore.updateDocumento(formValues);
    } else {
      // Modo criação
      this.documentoStore.addDocumento(formValues);
    }

    return true;
  }

  /**
   * Limpa o formulário
   * @param form - O FormGroup a ser limpo
   */
  clearForm(form: FormGroup): void {
    form.reset();
  }
}
