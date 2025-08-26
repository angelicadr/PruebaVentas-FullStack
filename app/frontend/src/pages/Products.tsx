import { useEffect, useState } from 'react'
import { api, login } from '../lib/api'

type Product = {
  id: number
  codigo: string
  nombre: string
  valor_venta: number
  maneja_iva: boolean
  iva_porcentaje?: number | null
}

export default function Products() {
  const [items, setItems] = useState<Product[]>([])
  const [form, setForm] = useState<Partial<Product>>({ maneja_iva: true })
  const [editingId, setEditingId] = useState<number | null>(null)

  useEffect(() => {
    (async () => {
      await login('admin','admin')
      await loadProducts()
    })()
  }, [])

  const loadProducts = async () => {
    const r = await api.get('/products/')
    setItems(r.data)
    console.log(setItems)
  }

  const submit = async (e:any) => {
  e.preventDefault()

  let payload = { ...form }

  // Normalización del IVA
  if (!payload.maneja_iva) {
    payload.iva_porcentaje = null
  } else {
    if (!payload.iva_porcentaje || payload.iva_porcentaje <= 0) {
      payload.iva_porcentaje = 19 // valor por defecto si maneja IVA pero no se ingresó
    }
  }

  if (editingId) {
    await api.put(`/products/${editingId}/`, payload)
  } else {
    await api.post('/products/', payload)
  }

  setForm({ maneja_iva: true })
  setEditingId(null)
  await loadProducts()
}

  const editProduct = (p: Product) => {
    setForm(p)
    setEditingId(p.id)
  }

  const deleteProduct = async (id:number) => {
    if (window.confirm("¿Seguro de borrar este producto?")) {
      await api.delete(`/products/${id}/`)
      setItems(items.filter(p => p.id !== id))
    }
  }

  return (
    <div className="container">
      <h2>Productos</h2>
      <form onSubmit={submit} style={{ display:'grid', gridTemplateColumns:'repeat(6, 1fr) auto', gap:8 }}>
        <input placeholder="Código" value={form.codigo||''} onChange={e=>setForm({...form, codigo:e.target.value})} required />
        <input placeholder="Nombre" value={form.nombre||''} onChange={e=>setForm({...form, nombre:e.target.value})} required />
        <input placeholder="Valor venta" type="number" value={form.valor_venta||0} onChange={e=>setForm({...form, valor_venta:Number(e.target.value)})} required />
        
        <label>
          <input type="checkbox" checked={!!form.maneja_iva} onChange={e=>setForm({...form, maneja_iva:e.target.checked})}/> Maneja IVA
        </label>
        
        <input placeholder="% IVA" type="number" value={form.iva_porcentaje||0} onChange={e=>setForm({...form, iva_porcentaje:Number(e.target.value)})} />
        <button>{editingId ? "Actualizar" : "Crear"}</button>
      </form>

      <h2>Lista de Productos</h2>
      <table>
        <thead>
          <tr>
            <th>Código</th>
            <th>Nombre</th>
            <th>Valor Venta</th>
            <th>Maneja IVA</th>
            <th>% IVA</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {items.map(p => (
            <tr key={p.id}>
              <td>{p.codigo}</td>
              <td>{p.nombre}</td>
              <td>${p.valor_venta}</td>
              <td>{p.maneja_iva ? "Sí" : "No"}</td>
              <td>{p.iva_porcentaje ?? "-"}</td>
              <td>
                <button type="button" onClick={()=>editProduct(p)}>✏️ Editar</button>
                <button type="button" onClick={()=>deleteProduct(p.id)}>🗑️ Borrar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}