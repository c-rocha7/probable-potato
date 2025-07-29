import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Documento } from '../types/documento';

@Injectable({
  providedIn: 'root',
})
export class Api {
  // Usa variável de ambiente se disponível, senão usa localhost
  baseUrl = (window as any)?.env?.API_URL || 'http://localhost:8001/api';
  http = inject(HttpClient);

  getDocumentos() {
    return this.http.get<Documento[]>(this.baseUrl + '/documento');
  }

  createDocumento(documento: Documento) {
    console.log(documento);
    return this.http.post<Documento>(
      this.baseUrl + '/documento/create',
      documento
    );
  }

  updateDocumento(documento: Documento) {
    return this.http.put(
      this.baseUrl + '/documento/update/' + documento.id,
      documento
    );
  }

  deleteDocumento(documento: Documento) {
    return this.http.delete(this.baseUrl + '/documento/delete/' + documento.id);
  }
}
