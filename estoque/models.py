from django.db import models
from pedidos.models import Produtos

class Estoque(models.Model):
    id_estoque = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    quantidade = models.IntegerField(blank=False)
    