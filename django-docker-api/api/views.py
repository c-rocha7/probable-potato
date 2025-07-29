from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Documento, Signatario
from .serializers import DocumentoSerializer, DocumentoWithSignersSerializer, DocumentoUpdateSerializer, SignatarioSerializer
from decouple import config

import json
import requests

# Configurações da API ZapSign
ZAPSIGN_API_TOKEN = config('ZAPSIGN_API_TOKEN')
ZAPSIGN_API_BASE_URL = config('ZAPSIGN_API_BASE_URL')

def get_zapsign_headers():
    """Retorna os headers necessários para autenticação na API ZapSign"""
    return {
        'Authorization': f'Bearer {ZAPSIGN_API_TOKEN}'
    }


@api_view(['GET'])
def get_documentos(request):
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        documentos = Documento.objects.all()
        serializer = DocumentoWithSignersSerializer(documentos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print("Error fetching documentos:", str(e))
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_documento(request, pk):
    if request.method != 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        documento = Documento.objects.get(pk=pk)
    except Documento.DoesNotExist:
        return Response({'error': 'Documento não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    try:
        serializer = DocumentoWithSignersSerializer(documento)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print("Error fetching documento:", str(e))
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_documento(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        data = request.data

        headers = get_zapsign_headers()

        response = requests.post(
            f'{ZAPSIGN_API_BASE_URL}/docs/',
            json={
                "name": data.get("name"),
                "url_pdf": data.get("url_documento"),
                "signers": [
                    {
                        "name": data.get("nome_signatario"),
                        "email": data.get("email_signatario"),
                    }
                ],
            },
            headers=headers
        )
        if response.status_code != 200:
            print("Erro na API externa:", response.status_code, response.text)
            return Response({'error': 'Erro na API externa'}, status=status.HTTP_400_BAD_REQUEST)

        api_result = response.json()

        data['openID'] = api_result.get('open_id', None)
        data['token'] = api_result.get('token', None)
        data['status'] = api_result.get('status', 'pending')
        data['created_by'] = api_result['created_by'].get('email', 'system')
        data['company_id'] = data.get('company_id', 1)
        data['external_id'] = api_result.get('external_id', 'vazio')

        serializer = DocumentoSerializer(data=data)

        if serializer.is_valid():
            documento_criado = serializer.save()

            try:
                # headers = {
                #     'Authorization': 'Bearer eb3905e2-0fe4-429d-b4fb-266964f52ee55b401a88-b6ef-47f5-8d66-27a4a8678a2b'
                # }

                # response = requests.post(
                #     f'https://sandbox.api.zapsign.com.br/api/v1/docs/{data['token']}/add-signer/',
                #     json={
                #         "name": data.get("name_signatario"),
                #         "email": data.get("email_signatario"),
                #     },
                #     headers=headers
                # )

                # if response.status_code != 200:
                #     print("Erro ao adicionar signatário:", response.status_code, response.text)
                #     return Response({'error': 'Erro ao adicionar signatário'}, status=status.HTTP_400_BAD_REQUEST)

                signatario_data = response.json()

                signatario_data['token'] = data['token']
                signatario_data['status'] = data['status']
                signatario_data['name'] = data.get("nome_signatario")
                signatario_data['email'] = data.get("email_signatario")
                # Use the correct field name and ensure it's not blank
                signatario_data['external_id'] = api_result.get(
                    'external_id', 'vazio')
                signatario_data['documentID'] = documento_criado.id

                signatario_serializer = SignatarioSerializer(
                    data=signatario_data)

                if signatario_serializer.is_valid():
                    signatario_serializer.save()
                    print(
                        f"Signatário cadastrado com sucesso: {data.get('nome_signatario')}")
                else:
                    print("Erro ao cadastrar signatário:",
                          signatario_serializer.errors)

            except Exception as e:
                print("Erro ao processar signatário:", str(e))

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("Erro de validação:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("Error fetching documentos:", str(e))
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_documento(request, pk):
    if request.method != 'PUT':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        documento = Documento.objects.get(pk=pk)
    except Documento.DoesNotExist:
        return Response({'error': 'Documento não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    try:
        data = request.data

        if 'name' not in data:
            return Response({'error': 'Campo name é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

        headers = get_zapsign_headers()

        response = requests.put(
            f'{ZAPSIGN_API_BASE_URL}/docs/{documento.token}/',
            json={
                "name": data.get("name"),
            },
            headers=headers
        )
        if response.status_code != 200:
            print("Erro na API externa:", response.status_code, response.text)
            return Response({'error': 'Erro na API externa'}, status=status.HTTP_400_BAD_REQUEST)

        documento.name = data.get("name")
        documento.save()

        serializer = DocumentoUpdateSerializer(documento)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        print("Error updating documento:", str(e))
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_documento(request, pk):
    if request.method != 'DELETE':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        documento = Documento.objects.get(pk=pk)
    except Documento.DoesNotExist:
        return Response({'error': 'Documento não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    try:

        data = request.data

        headers = get_zapsign_headers()

        response = requests.delete(
            f'{ZAPSIGN_API_BASE_URL}/docs/{documento.token}/',
            headers=headers
        )
        if response.status_code != 200:
            print("Erro na API externa:", response.status_code, response.text)
            return Response({'error': 'Erro na API externa'}, status=status.HTTP_400_BAD_REQUEST)

        documento.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        print("Error deleting documento:", str(e))
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
