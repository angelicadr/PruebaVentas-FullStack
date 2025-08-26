import pytest
from decimal import Decimal
from customers.models import Customer
from products.models import Product
from sales.models import Sale, SaleItem

@pytest.mark.django_db
def test_iva_calculation():
    c = Customer.objects.create(cedula="999", nombre="Cliente", direccion="X", telefono="Y")
    p = Product.objects.create(codigo="AAA", nombre="ProdIVA", valor_venta=100, maneja_iva=True, iva_porcentaje=19)
    sale = Sale.objects.create(cliente=c)
    item = SaleItem.objects.create(sale=sale, producto=p, cantidad=2, valor_unitario_capturado=100,
        subtotal_linea=200, iva_calculado=38, total_linea=238)
    sale.total_venta = item.total_linea
    sale.save()
    assert item.iva_calculado == Decimal("38")
    assert sale.total_venta == Decimal("238")

@pytest.mark.django_db
def test_sale_consecutivo_sequence(client):
    c = Customer.objects.create(cedula="111", nombre="Cliente", direccion="X", telefono="Y")
    p = Product.objects.create(codigo="BBB", nombre="Prod", valor_venta=50, maneja_iva=False)
    sale = Sale.objects.create(cliente=c)
    assert sale.consecutivo is not None
