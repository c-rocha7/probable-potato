from django.contrib import admin
from .models import Empresa, Documento, Signatario

admin.site.register(Empresa)
admin.site.register(Documento)
admin.site.register(Signatario)
