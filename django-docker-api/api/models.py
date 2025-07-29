from django.db import models


class Empresa(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        db_column='name',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='created_at',
    )
    last_updated_at = models.DateTimeField(
        auto_now=True,
        db_column='last_updated_at'
    )
    apiToken = models.CharField(
        max_length=255,
        null=False,
        db_column='api_token'
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'company'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Documento(models.Model):
    openID = models.IntegerField(
        null=False,
        db_column='openID',
    )
    token = models.CharField(
        max_length=255,
        null=False,
        db_column='token',
    )
    name = models.CharField(
        max_length=255,
        null=False,
        db_column='name',
    )
    status = models.CharField(
        max_length=50,
        null=False,
        db_column='status',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='created_at',
    )
    last_updated_at = models.DateTimeField(
        auto_now=True,
        db_column='last_updated_at',
    )
    created_by = models.CharField(
        max_length=255,
        null=False,
        db_column='created_by',
    )
    company_id = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        db_column='company_id',
    )
    externalID = models.CharField(
        max_length=255,
        null=True,
        db_column='externalID',
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'document'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'


class Signatario(models.Model):
    token = models.CharField(
        max_length=255,
        null=False,
        db_column='token',
    )
    status = models.CharField(
        max_length=50,
        null=False,
        db_column='status',
    )
    name = models.CharField(
        max_length=255,
        null=False,
        db_column='name',
    )
    email = models.EmailField(
        max_length=255,
        null=False,
        db_column='email',
    )
    externalID = models.CharField(
        max_length=255,
        null=True,
        db_column='externalID',
    )
    documentID = models.ForeignKey(
        Documento,
        on_delete=models.CASCADE,
        db_column='documentID',
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'signers'
        verbose_name = 'Signer'
        verbose_name_plural = 'Signers'
