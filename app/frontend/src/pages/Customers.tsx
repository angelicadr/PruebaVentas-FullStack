import { useEffect, useState } from 'react'
import { api, login } from '../lib/api'

type Customer = {
  id: number
  cedula: string
  nombre: string
  direccion: string
  telefono: string
  email?: string | null
}

export default function Customers() {
  const [items, setItems] = useState<Customer[]>([])
  const [form, setForm] = useState<Partial<Customer>>({})
  const [editingId, setEditingId] = useState<number | null>(null)

  useEffect(() => {
    (async () => {
      await login('admin','admin')
      await loadCustomers()
    })()
  }, [])

  const loadCustomers = async () => {
    const r = await api.get('/customers/')
    setItems(r.data)
  }

  const submit = async (e:any) => {
    e.preventDefault()
    if (editingId) {
      // editar
      await api.put(`/customers/${editingId}/`, form)
    } else {
      // crear
      await api.post('/customers/', form)
    }
    setForm({})
    setEditingId(null)
    await loadCustomers()
  }

  const editCustomer = (c: Customer) => {
    setForm(c)
    setEditingId(c.id)
  }

  const deleteCustomer = async (id:number) => {
    if (window.confirm("¿Seguro de borrar este cliente?")) {
      await api.delete(`/customers/${id}/`)
      setItems(items.filter(c => c.id !== id))
    }
  }

  return (
    <div className="container">
      <h2>Clientes</h2>
      <form onSubmit={submit} style={{ display:'grid', gridTemplateColumns:'repeat(5, 1fr) auto', gap:8 }}>
        <input placeholder="Cédula" value={form.cedula||''} onChange={e=>setForm({...form, cedula:e.target.value})} required />
        <input placeholder="Nombre" value={form.nombre||''} onChange={e=>setForm({...form, nombre:e.target.value})} required />
        <input placeholder="Dirección" value={form.direccion||''} onChange={e=>setForm({...form, direccion:e.target.value})} required />
        <input placeholder="Teléfono" value={form.telefono||''} onChange={e=>setForm({...form, telefono:e.target.value})} required />
        <input placeholder="Email" value={form.email||''} onChange={e=>setForm({...form, email:e.target.value})} />
        <button>{editingId ? "Actualizar" : "Crear"}</button>
      </form>

      <h2>Lista de Clientes</h2>
      <table>
        <thead>
          <tr>
            <th>Cédula</th>
            <th>Nombre</th>
            <th>Dirección</th>
            <th>Teléfono</th>
            <th>Email</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {items.map(c => (
            <tr key={c.id}>
              <td>{c.cedula}</td>
              <td>{c.nombre}</td>
              <td>{c.direccion}</td>
              <td>{c.telefono}</td>
              <td>{c.email}</td>
              <td>
                <button type="button" onClick={()=>editCustomer(c)}>✏️ Editar</button>
                <button type="button" onClick={()=>deleteCustomer(c.id)}>🗑️ Borrar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}