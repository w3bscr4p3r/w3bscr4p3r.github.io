import { useState, useEffect } from 'react'
import PedidoForm from './components/PedidoForm'
import Dashboard from './components/Dashboard'
import Filtros from './components/Filtros'

function App() {
  const [pedidos, setPedidos] = useState([])
  const [totais, setTotais] = useState({})
  const [filtros, setFiltros] = useState({ status: 'todos', cliente: '' })
  const [loading, setLoading] = useState(false)
  const [activeView, setActiveView] = useState('dashboard')

  const fetchData = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (filtros.status !== 'todos') params.append('status', filtros.status)
      if (filtros.cliente) params.append('cliente_nome', filtros.cliente)

      const [pedidosRes, totaisRes] = await Promise.all([
        fetch(`/api/pedidos?${params}`).then(r => r.json()),
        fetch('/api/pedidos/totais').then(r => r.json())
      ])
      
      setPedidos(pedidosRes)
      setTotais(totaisRes)
    } catch (error) {
      console.error('Erro:', error)
    }
    setLoading(false)
  }

  useEffect(() => {
    fetchData()
  }, [filtros])

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100">
      <header className="bg-white/80 backdrop-blur-md shadow-sm border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
              🥚 Ovos Páscoa Léia
            </h1>
            <nav className="flex space-x-1">
              <button
                onClick={() => setActiveView('dashboard')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  activeView === 'dashboard'
                    ? 'bg-purple-600 text-white shadow-lg'
                    : 'text-gray-600 hover:text-purple-600 hover:bg-purple-50'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => setActiveView('novo')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  activeView === 'novo'
                    ? 'bg-green-600 text-white shadow-lg'
                    : 'text-gray-600 hover:text-green-600 hover:bg-green-50'
                }`}
              >
                Novo Pedido
              </button>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeView === 'dashboard' && (
          <>
            <Filtros filtros={filtros} setFiltros={setFiltros} />
            <Dashboard pedidos={pedidos} totais={totais} loading={loading} refresh={fetchData} />
          </>
        )}
        
        {activeView === 'novo' && (
          <PedidoForm onSuccess={fetchData} />
        )}
      </main>
    </div>
  )
}

export default App
