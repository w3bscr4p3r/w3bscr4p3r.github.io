import PedidoCard from './PedidoCard'
import Totais from './Totais'

export default function Dashboard({ pedidos, totais, loading, refresh }) {
  return (
    <div className="space-y-8">
      {/* Totais */}
      <Totais totais={totais} />
      
      {/* Lista de Pedidos */}
      <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
        <div className="p-8 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-800">Pedidos</h2>
          <p className="text-gray-600 mt-1">{pedidos.length} pedidos encontrados</p>
        </div>
        
        <div className="p-0">
          {loading ? (
            <div className="p-12 text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
              <p className="mt-4 text-gray-600">Carregando pedidos...</p>
            </div>
          ) : pedidos.length === 0 ? (
            <div className="p-12 text-center">
              <div className="w-24 h-24 mx-auto bg-gray-100 rounded-2xl flex items-center justify-center mb-4">
                📋
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Nenhum pedido encontrado</h3>
              <p className="text-gray-600 mb-6">Tente ajustar os filtros ou crie o primeiro pedido!</p>
              <button
                onClick={() => window.location.href = '#novo'}
                className="bg-green-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-green-700 transition-colors"
              >
                Criar Primeiro Pedido
              </button>
            </div>
          ) : (
            <div className="divide-y divide-gray-100">
              {pedidos.map((pedido) => (
                <PedidoCard key={pedido.id} pedido={pedido} onUpdate={refresh} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
