export interface Signer {
  id: number;
  token: string;
  status: string;
  name: string;
  email: string;
  externalID: string;
  documentID: number;
}

export interface Documento {
  id: number;
  openID: number;
  token: string;
  name: string;
  status: string;
  created_at: string;
  signers: Signer[];
}
