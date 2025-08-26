from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
def validate(self, data):
    if not data.get("maneja_iva"):
        data["iva_porcentaje"] = None
    elif data.get("iva_porcentaje") is None:
        raise serializers.ValidationError({"iva_porcentaje": "Debe indicar un % IVA si maneja IVA"})
    return data
