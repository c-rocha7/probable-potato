import { Component, inject, Output, EventEmitter } from '@angular/core';
import { DatePipe } from '@angular/common';
import { DocumentoStore } from '../../store/documento-store';
import { Documento } from '../../types/documento';

@Component({
  selector: 'app-documento-table',
  standalone: true,
  imports: [DatePipe],
  templateUrl: './documento-table.component.html',
  styleUrl: './documento-table.component.css',
})
export class DocumentoTableComponent {
  @Output() editDocumento = new EventEmitter<Documento>();
  @Output() deleteDocumento = new EventEmitter<Documento>();

  documentoStore = inject(DocumentoStore);

  onEditDocumento(documento: Documento) {
    this.editDocumento.emit(documento);
  }

  onDeleteDocumento(documento: Documento) {
    this.deleteDocumento.emit(documento);
  }

  onRefresh() {
    this.documentoStore.reloadDocumentos();
  }
}
