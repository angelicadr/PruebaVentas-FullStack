from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction, connection
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from customers.models import Customer
from products.models import Product
from .serializers import SaleSerializer, SaleCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFilter
from .models import Customer, Product, Sale , SaleItem

class SaleFilter(FilterSet):
    fecha_inicio = DateFilter(field_name="fecha", lookup_expr="gte")
    fecha_fin = DateFilter(field_name="fecha", lookup_expr="lte")

    class Meta:
        model = Sale
        fields = ["fecha"]

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.prefetch_related("items","items__producto").select_related("cliente").order_by("-id","-fecha")
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get","post","head","options"]

    def get_serializer_class(self):
        if self.action in ["create"]:
            return SaleCreateSerializer
        return SaleSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        f = request.query_params.get("from")
        t = request.query_params.get("to")
        if f and t:
            qs = qs.filter(fecha__range=[f,t])
        return Response(SaleSerializer(qs, many=True).data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        ser = SaleCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        cliente = Customer.objects.get(pk=data["cliente"])
        fecha = data.get("fecha") or timezone.now().date()

        # Obtener consecutivo desde secuencia PostgreSQL
        with connection.cursor() as cur:
            cur.execute("SELECT nextval('sales_seq')")
            consecutivo = cur.fetchone()[0]

        sale = Sale.objects.create(cliente=cliente, fecha=fecha, consecutivo=consecutivo)

        total = Decimal("0")
        for item in data["items"]:
            prod = Product.objects.get(pk=item["producto"].id if hasattr(item["producto"],"id") else item["producto"])
            cantidad = int(item["cantidad"])
            unit = Decimal(item["valor_unitario_capturado"]).quantize(Decimal("1.00"))
            subtotal = (unit * cantidad).quantize(Decimal("1.00"))
            iva = Decimal("0")
            if prod.maneja_iva and prod.iva_porcentaje is not None:
                iva = (subtotal * Decimal(prod.iva_porcentaje) / Decimal("100")).quantize(Decimal("1.00"), rounding=ROUND_HALF_UP)
            total_linea = (subtotal + iva).quantize(Decimal("1.00"))
            SaleItem.objects.create(
                sale=sale, producto=prod, cantidad=cantidad,
                valor_unitario_capturado=unit, iva_calculado=iva,
                subtotal_linea=subtotal, total_linea=total_linea
            )
            total += total_linea

        sale.total_venta = total.quantize(Decimal("1.00"))
        sale.save()

        return Response(SaleSerializer(sale).data, status=status.HTTP_201_CREATED)
