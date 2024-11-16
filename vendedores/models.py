from django.db import models

class Fornecedor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=False)
    cnpj = models.CharField(max_length=20, blank=False, unique=True)
    ie = models.CharField(max_length=20)
    endereco = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    cep = models.CharField(max_length=20)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)