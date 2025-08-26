# Sistema Administrativo de Ventas — Prueba Técnica

Solución propuesta **Full Stack** con _Back-end_ **Django + DRF + Python** (REST, JWT) y _Front-end_ **React + Vite + TypeScript**. Base de datos **PostgreSQL**. Incluye esquema SQL, especificación OpenAPI y colección de Postman para pruebas rápidas.

> La prueba solicita: CRUD de Cliente y Producto, registro de **Cabecera** y **Detalle** de Ventas, **listado por fecha**, separación Front/Back y servicios **REST o SOAP** (optativo implementar ambos). También permite frameworks como **Django**/**SpringBoot** y **React**/**Angular**/**Vue**. 



## Arquitectura

- **DB**: PostgreSQL 15
- **API**: Python 3.12, Django 5, Django REST Framework, JWT (simplejwt), drf-spectacular (OpenAPI), django-filter.
- **Front**: React 18 + Vite + TypeScript, React Router, React Hook Form + Zod, React Query, Axios, TailwindCSS.
- **Contenedores**: Docker Compose (db, api, web).
- **Estándares**: 12-Factor, .env, migrations, CI fácil de integrar (GitHub Actions).

docs\Prueba-Ventas.jpg

### Módulos
- `customers`: Clientes (cédula, nombre, dirección, teléfono, email).
- `products`: Productos (código, nombre, valor_venta, maneja_iva, iva_porcentaje).
- `sales`: Ventas
  - **Cabecera**: consecutivo (seq), fecha, cliente, total_venta.
  - **Detalle**: producto, cantidad, valor_unitario_capturado, iva_calculado, subtotal_línea, total_línea.

> El **consecutivo** se genera desde la base mediante `sales_seq` para evitar colisiones en concurrencia. El **total_venta** se calcula en servidor a partir de los detalles para proteger integridad. 


## Modelo de Datos (ER)
- **customers**(id, cedula[unique], nombre, direccion, telefono, email[unique nullable], created_at)
- **products**(id, codigo[unique], nombre, valor_venta, maneja_iva, iva_porcentaje, created_at)
- **sales**(id, consecutivo[unique], fecha, cliente_id FK, total_venta, created_at)
- **sale_items**(id, sale_id FK, producto_id FK, cantidad, valor_unitario_capturado, iva_calculado, subtotal_linea, total_linea)

docs\Diagrama BD pruebaVentas.png

**Reglas de IVA**:
```
iva_linea = (valor_unitario_capturado * cantidad) * (iva_porcentaje/100) si maneja_iva
subtotal_linea = valor_unitario_capturado * cantidad
total_linea = subtotal_linea + iva_linea
total_venta = SUM(total_linea) por venta
```

## API (REST, JWT)
- `POST   /api/v1/auth/login` → token
- `POST   /api/v1/customers` | `GET /customers` | `GET /customers/:id` | `PUT/PATCH /customers/:id` | `DELETE`
- `POST   /api/v1/products`  | `GET /products`  | `GET /products/:id`  | `PUT/PATCH /products/:id` | `DELETE`
- `POST   /api/v1/sales`     → crea cabecera + items (transacción)
- `GET    /api/v1/sales`     → filtro por `from=YYYY-MM-DD&to=YYYY-MM-DD`
- `GET    /api/v1/sales/:id` → detalle con items

### Validaciones clave
- `cedula`, `codigo` únicos.
- `valor_venta >= 0`, `iva_porcentaje ∈ [0, 100]` si `maneja_iva=true`.
- `cantidad >= 1`.
- Email formato correcto si provisto.
- La fecha de venta por defecto es la del servidor (UTC) pero se puede enviar.
- El total se recalcula server-side, se ignora cualquier total enviado por el cliente.

## Seguridad
- JWT (acceso/refresh), rate limit básico (throttling DRF), CORS restringido por ambiente, headers `X-Request-Id`, logs estructurados, validación y sanitización de entrada, políticas de rol **admin** .

## Testing
- **Back**: pytest + coverage (unit, api, integración DB). Factories y tests de IVA.
- **Front**: Vitest + React Testing Library (componentes y formularios).
- Datos `seed` reproducibles con `manage.py loaddata`.

## Puesta en marcha - Instalación (Docker)

```bash
# 1) Clonar el repositorio: 
https://github.com/angelicadr/prueba-ventas.git

# 2) en una terminal CMD ubicarse en la raíz donde se encuentre docker-compose.yml o segun se ubique las variables de entorno
cp .env.example .env

# 3) Construye y levanta todos los servicios que se definieron en el docker-compose.yml:
docker compose up -d --build

# 4) Crear superusuario (primera vez) si se ve alguna falla 
docker compose exec api python manage.py createsuperuser

# 5) Apaga contenedores anteriores y elimina volúmenes si es necesario:
docker-compose down -v

```
## URLs locales

- **Frontend (React):**
- http://localhost:5173

- **Backend API (Django):**
- http://localhost:8000/admin/

- **Swagger / Docs API:**
- http://localhost:8000/api/schema/swagger-ui/


## Estructura  de repositorio

```
/app
  /backend
    manage.py
    /config          # settings, urls, asgi, wsgi
    /customers
    /products
    /sales
    /tests
    requirements.txt
  /frontend
    index.html
    package.json
    src/
docker-compose.yml
schema.sql
openapi.yaml
.postman/ventas.postman_collection.json
README.md
```

## Ejemplos de payload

**Crear producto**
```json
POST /api/v1/products
{
  "codigo": "JAB-100",
  "nombre": "Jabón Neutro 200g",
  "valor_venta": 3500,
  "maneja_iva": true,
  "iva_porcentaje": 19
}
```

**Crear venta (1 cabecera + n items)**
```json
POST /api/v1/sales
{
  "cliente_id": 1,
  "fecha": "2025-08-21",
  "items": [
    {"producto_id": 10, "cantidad": 2, "valor_unitario_capturado": 3500},
    {"producto_id": 11, "cantidad": 1, "valor_unitario_capturado": 12000}
  ]
}
```
Respuesta:
```json
{
  "id": 99,
  "consecutivo": 2025000099,
  "fecha": "2025-08-21",
  "cliente": {"id":1,"cedula":"123","nombre":"Cliente Demo"},
  "total_venta": 22610,
  "items": [
    {"producto_id":10,"cantidad":2,"valor_unitario_capturado":3500,"iva_calculado":1330,"total_linea": 8330},
    {"producto_id":11,"cantidad":1,"valor_unitario_capturado":12000,"iva_calculado":2280,"total_linea": 14280}
  ]
}
```

## SOAP (opcional)
Servicio `VentasWS` con métodos:
- `crearVenta(clienteId, fecha, items[])` → retorna `consecutivo` y `totalVenta`.
- `listarVentasPorFecha(desde, hasta)` → retorna arreglo de ventas con totales.

## Extras de valor
- Paginación y ordenación en listados.
- Búsqueda por `cedula`, `nombre`, `codigo`.
- Auditoría simple (`created_at`, `updated_at`).
- Exportación CSV del listado por fecha.

---

> Revisa `schema.sql`, `openapi.yaml` y la colección Postman para probar de inmediato.

## Tests
- Backend: `docker compose exec api pytest -q`
