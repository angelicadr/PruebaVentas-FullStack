import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'
import Customers from './pages/Customers'
import Products from './pages/Products'
import Sales from './pages/Sales'

const router = createBrowserRouter([
  { path: '/', element: <App />,
    children: [
      { path: '/customers', element: <Customers /> },
      { path: '/products', element: <Products /> },
      { path: '/sales', element: <Sales /> },
    ]
  }
])

const qc = new QueryClient()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={qc}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>
)
