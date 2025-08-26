import json
from decimal import Decimal
from django.test import Client
from customers.models import Customer
from products.models import Product

def test_crear_venta_calcula_iva(db):
    c = Customer.objects.create(cedula="999", nombre="Test", direccion="X", telefono="1")
    p = Product.objects.create(codigo="IVA-1", nombre="Con IVA", valor_venta=Decimal("1000.00"), maneja_iva=True, iva_porcentaje=Decimal("19.00"))
    client = Client()
    payload = {"cliente": c.id, "items":[{"producto": p.id, "cantidad": 2, "valor_unitario_capturado": "1000.00"}]}
    r = client.post("/api/v1/sales", data=json.dumps(payload), content_type="application/json")
    assert r.status_code == 201, r.content
    data = r.json()
    # subtotal 2000, iva 380, total 2380
    assert Decimal(str(data["total_venta"])) == Decimal("2380.00")
    item = data["items"][0]
    assert Decimal(str(item["iva_calculado"])) == Decimal("380.00")
