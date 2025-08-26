import { useEffect, useState } from 'react'
import { api, login } from '../lib/api'

type Item = {
  producto: number
  cantidad: number
  valor_unitario_capturado: number
}

type Customer = {
  id: number
  nombre: string
}

type Product = {
  id: number
  nombre: string
  valor_venta: number
}

type Venta = {
  id: number
  consecutivo: string
  total_venta: number
  fecha: string
  cliente: string
}

export default function Sales() {
  const [ventas, setVentas] = useState<any[]>([])
  const [customers, setCustomers] = useState<Customer[]>([])
  const [products, setProducts] = useState<Product[]>([])

  const [fechaInicio, setFechaInicio] = useState('')
  const [fechaFin, setFechaFin] = useState('')
  const [ventasFiltradas, setVentasFiltradas] = useState<any[]>([])
  const [form, setForm] = useState<{cliente?: number, fecha?: string, items: Item[]}>({
    cliente: undefined,
    items: []
  })



   const cargarVentas = async () => {
    let url = '/sales/'
    if (fechaInicio && fechaFin) {
      url += `?fecha_inicio=${encodeURIComponent(fechaInicio)}&fecha_fin=${encodeURIComponent(fechaFin)}`
    }
  console.log("Request a:", url) 

   const r = await api.get(url)
    setVentas(r.data)
  }

  useEffect(() => {
    (async () => {
      await login('admin','admin')
      const [v, c, p] = await Promise.all([
        api.get('/sales'),
        api.get('/customers/'),
        api.get('/products/')
      ])
      setVentas(v.data)
      setCustomers(c.data)
      setProducts(p.data)
      cargarVentas()
      setVentasFiltradas(v.data) // inicialmente muestra todas
    })()
  }, [])

   const filtrar = () => {
    if (!fechaInicio && !fechaFin) {
      setVentasFiltradas(ventas)
      return
    }

    const fi = fechaInicio ? new Date(fechaInicio) : null
    const ff = fechaFin ? new Date(fechaFin) : null

    const filtradas = ventas.filter(v => {
      const fechaVenta = new Date(v.fecha)
      if (fi && fechaVenta < fi) return false
      if (ff && fechaVenta > ff) return false
      return true
    })

    setVentasFiltradas(filtradas)
   }
  const handleProductChange = (idx: number, productId: number) => {
    const producto = products.find(p => p.id === productId)
    if (!producto) return
    const n = [...form.items]
    n[idx] = {
      ...n[idx],
      producto: producto.id,
      valor_unitario_capturado: producto.valor_venta
    }
    setForm({ ...form, items: n })
  }

  const handleCantidadChange = (idx: number, cantidad: number) => {
    const n = [...form.items]
    n[idx].cantidad = cantidad
    setForm({ ...form, items: n })
  }

 const addItem = () => {
  setForm({
    ...form,
    items: [...form.items, { producto: undefined as any, cantidad: 1, valor_unitario_capturado: 0 }]
  })
}

console.log("Payload enviado:", form)
  const submit = async (e:any) => {
    e.preventDefault()
    const payload = {
      cliente: form.cliente,
      fecha: form.fecha,
      items: form.items.filter(it => it.producto) // solo productos válidos
    }

    if (!payload.cliente) {
      alert("Debes seleccionar un cliente")
      return
    }
    if (payload.items.length === 0) {
      alert("Debes agregar al menos un producto")
      return
    }
    const r = await api.post('/sales/', payload)
    setVentas([r.data, ...ventas])
    setForm({ cliente: undefined, fecha: '', items: [] })
    console.log(ventas)

    

  }

  return (
    <div >
      <h2>Registrar Ventas</h2>
      <form onSubmit={submit} style={{ display:'grid', gap:12 }}>
        
        {/* Selección de cliente */}
        <select value={form.cliente || ''} 
          onChange={e => setForm({ ...form, cliente: Number(e.target.value) })} 
          required>
          <option value="">-- Seleccionar Cliente --</option>
          {customers.map(c => (
            <option key={c.id} value={c.id}>{c.nombre}</option>
          ))}
        </select>

        {/* Fecha */}
        <input placeholder="Fecha (YYYY-MM-DD)" 
          value={form.fecha || ''} 
          onChange={e => setForm({ ...form, fecha: e.target.value })} />

        <h2>Items</h2>

        {form.items.map((it, idx) => (
          <div key={idx} style={{ display:'grid', gridTemplateColumns:'2fr 1fr 1fr', gap:8 }}>
            <select 
              value={it.producto || ''} 
              onChange={e => handleProductChange(idx, Number(e.target.value))}
              required
            >
              <option value="">-- Seleccionar Producto --</option>
              {products.map(p => (
                <option key={p.id} value={p.id}>{p.nombre} (${p.valor_venta})</option>
              ))}
            </select>

            <input type="number" placeholder="Cantidad" 
              value={it.cantidad} 
              onChange={e => handleCantidadChange(idx, Number(e.target.value))} 
              required />

            <input type="number" value={it.valor_unitario_capturado} disabled />
          </div>
        ))}
        
        <button type="button" onClick={addItem}>+ Producto</button>
        <button type="submit">Crear venta</button>
      </form>

      <h2>Lista de Ventas</h2>
<div style={{ marginBottom: '1rem' }}>
        <label>
          Fecha inicio:
          <input
            type="date"
            value={fechaInicio}
            onChange={e => setFechaInicio(e.target.value)}
          />
        </label>
        <label>
          Fecha fin:
          <input
            type="date"
            value={fechaFin}
            onChange={e => setFechaFin(e.target.value)}
          />
        </label>
        <button onClick={filtrar}>Filtrar</button>
      </div>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Consecutivo</th>
            <th>Total</th>
            <th>Fecha</th>
            <th>Cliente</th>
          </tr>
        </thead>
        <tbody>
          {ventasFiltradas.map(v => (
            <tr key={v.id}>
              <td>{v.id}</td>
              <td>{v.consecutivo}</td>
              <td>{v.total_venta}</td>
              <td>{v.fecha}</td>
              <td>{v.cliente_nombre}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
