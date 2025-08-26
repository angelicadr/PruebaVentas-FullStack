from rest_framework import serializers
from .models import Sale, SaleItem

class SaleItemInputSerializer(serializers.Serializer):
    producto = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1)
    valor_unitario_capturado = serializers.DecimalField(max_digits=12, decimal_places=2)

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ("id","producto_id","cantidad","valor_unitario_capturado","iva_calculado","subtotal_linea","total_linea")

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    cliente_nombre = serializers.CharField(source="cliente.nombre", read_only=True)
    class Meta:
        model = Sale
        fields = ("id","consecutivo","fecha","cliente_id","cliente_nombre","total_venta","items")

class SaleCreateSerializer(serializers.Serializer):
    cliente = serializers.IntegerField()
    fecha = serializers.DateField(required=False)
    items = SaleItemInputSerializer(many=True)
