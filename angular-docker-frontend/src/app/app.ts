import { Component, inject } from '@angular/core';
import { DocumentoStore } from './store/documento-store';
import { Documento } from './types/documento';
import { DocumentoFormComponent } from './components/documento-form/documento-form.component';
import { DocumentoTableComponent } from './components/documento-table/documento-table.component';

@Component({
  selector: 'app-root',
  imports: [DocumentoFormComponent, DocumentoTableComponent],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  selectedDocumento: Documento | null = null;
  documentoStore = inject(DocumentoStore);

  onEditDocumento(documento: Documento) {
    this.selectedDocumento = documento;
  }

  onDeleteDocumento(documento: Documento) {
    this.documentoStore.deleteDocumento(documento);
  }

  onFormCleared() {
    this.selectedDocumento = null;
  }

  onDocumentoSaved() {
    this.selectedDocumento = null;
  }
}
