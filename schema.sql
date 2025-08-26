-- Esquema PostgreSQL para el sistema de ventas

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Secuencia de ventas consecutivas
CREATE SEQUENCE IF NOT EXISTS sales_seq START 2025000000 INCREMENT 1;

CREATE TABLE IF NOT EXISTS customers (
  id              BIGSERIAL PRIMARY KEY,
  cedula          VARCHAR(20) NOT NULL UNIQUE,
  nombre          VARCHAR(120) NOT NULL,
  direccion       VARCHAR(200) NOT NULL,
  telefono        VARCHAR(30)  NOT NULL,
  email           VARCHAR(150),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS products (
  id              BIGSERIAL PRIMARY KEY,
  codigo          VARCHAR(40) NOT NULL UNIQUE,
  nombre          VARCHAR(160) NOT NULL,
  valor_venta     NUMERIC(12,2) NOT NULL CHECK (valor_venta >= 0),
  maneja_iva      BOOLEAN NOT NULL DEFAULT FALSE,
  iva_porcentaje  NUMERIC(5,2) CHECK (iva_porcentaje >= 0 AND iva_porcentaje <= 100),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT iva_required CHECK ( (maneja_iva = FALSE AND iva_porcentaje IS NULL) OR (maneja_iva = TRUE AND iva_porcentaje IS NOT NULL) )
);

CREATE TABLE IF NOT EXISTS sales (
  id              BIGSERIAL PRIMARY KEY,
  consecutivo     BIGINT NOT NULL UNIQUE DEFAULT nextval('sales_seq'),
  fecha           DATE NOT NULL DEFAULT CURRENT_DATE,
  cliente_id      BIGINT NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
  total_venta     NUMERIC(14,2) NOT NULL DEFAULT 0,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sale_items (
  id                          BIGSERIAL PRIMARY KEY,
  sale_id                     BIGINT NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
  producto_id                 BIGINT NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  cantidad                    INTEGER NOT NULL CHECK (cantidad >= 1),
  valor_unitario_capturado    NUMERIC(12,2) NOT NULL CHECK (valor_unitario_capturado >= 0),
  iva_calculado               NUMERIC(12,2) NOT NULL DEFAULT 0,
  subtotal_linea              NUMERIC(12,2) NOT NULL DEFAULT 0,
  total_linea                 NUMERIC(12,2) NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_sales_fecha ON sales(fecha);
CREATE INDEX IF NOT EXISTS idx_sales_cliente ON sales(cliente_id);
CREATE INDEX IF NOT EXISTS idx_items_sale ON sale_items(sale_id);
CREATE INDEX IF NOT EXISTS idx_items_producto ON sale_items(producto_id);

-- El disparador para mantener sales.total_venta sincronizado se implementaría a nivel de aplicación en una transacción.