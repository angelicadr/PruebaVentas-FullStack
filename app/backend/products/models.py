from django.db import models

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.CharField(max_length=40, unique=True)
    nombre = models.CharField(max_length=160)
    valor_venta = models.DecimalField(max_digits=12, decimal_places=2)
    maneja_iva = models.BooleanField(default=False)
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.maneja_iva and self.iva_porcentaje is None:
            raise ValidationError("iva_porcentaje es obligatorio si maneja_iva=True")
        if not self.maneja_iva:
            self.iva_porcentaje = None

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
