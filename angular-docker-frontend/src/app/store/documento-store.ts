import { inject, signal, Injectable } from '@angular/core';
import { Documento } from '../types/documento';
import { Api } from '../services/api';
import { ToastrService } from 'ngx-toastr';

@Injectable({
  providedIn: 'root'
})
export class DocumentoStore {
  documentos = signal<Documento[]>([]);
  loading = signal<boolean>(false);
  toaster = inject(ToastrService);
  api = inject(Api);

  constructor() {
    this.loadDocumentos();
  }

  loadDocumentos() {
    this.loading.set(true);
    this.api.getDocumentos().subscribe({
      next: (documentos) => {
        this.documentos.set(documentos);
        this.loading.set(false);
      },
      error: (error) => {
        console.error('Erro ao carregar documentos:', error);
        this.toaster.error('Erro ao carregar documentos.');
        this.loading.set(false);
      }
    });
  }

  // Método público para recarregar dados
  reloadDocumentos() {
    this.loadDocumentos();
  }

  addDocumento(documento: Documento) {
    this.api.createDocumento(documento).subscribe({
      next: (result) => {
        this.toaster.success('Documento adicionado.');
        // Recarrega todos os documentos do servidor para garantir consistência
        this.loadDocumentos();
      },
      error: (error) => {
        console.error('Erro ao adicionar documento:', error);
        this.toaster.error('Erro ao adicionar documento.');
      }
    });
  }
  updateDocumento(documento: Documento) {
    this.api.updateDocumento(documento).subscribe({
      next: () => {
        this.toaster.success('Documento atualizado.');
        // Recarrega todos os documentos do servidor para garantir consistência
        this.loadDocumentos();
      },
      error: (error) => {
        console.error('Erro ao atualizar documento:', error);
        this.toaster.error('Erro ao atualizar documento.');
      }
    });
  }
  deleteDocumento(documento: Documento) {
    this.api.deleteDocumento(documento).subscribe({
      next: () => {
        this.toaster.success('Documento deletado.');
        // Recarrega todos os documentos do servidor para garantir consistência
        this.loadDocumentos();
      },
      error: (error) => {
        console.error('Erro ao deletar documento:', error);
        this.toaster.error('Erro ao deletar documento.');
      }
    });
  }
}
