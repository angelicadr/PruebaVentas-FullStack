import { Link, Outlet } from 'react-router-dom'

export default function App() {
  return (
    <div style={{ padding: 16, fontFamily: 'system-ui, Arial' }}>
      <h1>Sistema de Ventas</h1>
      <nav style={{ display:'flex', gap: 12 }}>
        <Link to="/customers">Clientes</Link>
        <Link to="/products">Productos</Link>
        <Link to="/sales">Ventas</Link>
      </nav>
      <hr />
      <Outlet />
    </div>
  )
}
