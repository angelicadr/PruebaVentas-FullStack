from django.db import models
from customers.models import Customer
from products.models import Product

class Sale(models.Model):
    id = models.BigAutoField(primary_key=True)
    consecutivo = models.BigIntegerField(unique=True)
    fecha = models.DateField()
    cliente = models.ForeignKey(Customer, on_delete=models.RESTRICT, db_column="cliente_id", related_name="ventas")
    total_venta = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sales"

    def __str__(self):
        return f"Venta {self.consecutivo}"

class SaleItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, db_column="sale_id", related_name="items")
    producto = models.ForeignKey(Product, on_delete=models.RESTRICT, db_column="producto_id")
    cantidad = models.PositiveIntegerField()
    valor_unitario_capturado = models.DecimalField(max_digits=12, decimal_places=2)
    iva_calculado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal_linea = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_linea = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = "sale_items"

    def __str__(self):
        return f"{self.producto_id} x {self.cantidad}"
