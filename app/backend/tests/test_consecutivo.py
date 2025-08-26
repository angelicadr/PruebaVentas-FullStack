import json
from django.test import Client
from customers.models import Customer
from products.models import Product
from decimal import Decimal

def test_consecutivo_por_secuencia_incrementa(db):
    c = Customer.objects.create(cedula="888", nombre="Seq", direccion="X", telefono="1")
    p = Product.objects.create(codigo="P1", nombre="Prod", valor_venta=Decimal("100.00"), maneja_iva=False)
    client = Client()
    for _ in range(2):
        payload = {"cliente": c.id, "items":[{"producto": p.id, "cantidad": 1, "valor_unitario_capturado": "100.00"}]}
        r = client.post("/api/v1/sales", data=json.dumps(payload), content_type="application/json")
        assert r.status_code == 201
    # Get both and ensure consecutivo increases
    r = client.get("/api/v1/sales")
    ventas = r.json()
    assert len(ventas) >= 2
    cons = [v["consecutivo"] for v in ventas[:2]]
    assert cons[0] != cons[1]
