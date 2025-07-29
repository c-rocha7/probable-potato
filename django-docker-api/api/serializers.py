from rest_framework import serializers
from .models import Empresa, Documento, Signatario


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class SignatarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signatario
        fields = '__all__'


class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'


class DocumentoWithSignersSerializer(serializers.ModelSerializer):
    signers = serializers.SerializerMethodField()

    class Meta:
        model = Documento
        fields = '__all__'

    def get_signers(self, obj):
        signatarios = Signatario.objects.filter(documentID=obj)
        return SignatarioSerializer(signatarios, many=True).data


class DocumentoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = ['name']
