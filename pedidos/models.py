from django.db import models
from vendedores.models import Fornecedor

class Produtos(models.Model):
    id_produto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Pedidos(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    data_pedido = models.DateField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calcula_valor_total(self):
        total = sum(item.quantidade * item.valor_unitario for item in self.produtos.all())
        self.valor_total = total
        self.save()

class PedidoPorProduto(models.Model):
    pedido = models.ForeignKey(Pedidos, related_name='produtos', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(default=1)



