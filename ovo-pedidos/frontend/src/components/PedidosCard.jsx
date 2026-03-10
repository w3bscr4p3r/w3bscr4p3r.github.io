import { useState } from 'react'
import api from '../services/api'

const STATUS_COLORS = {
  pendente: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  'entrada_paga': 'bg-green-100 text-green-800 border-green-200',
  em_producao: 'bg-blue-100 text-blue-800 border-blue-200',
  pronto: 'bg-purple-100 text-purple-800 border-purple-200',
  entregue: 'bg-gray-100 text-gray-800 border-gray-200',
  cancelado: 'bg-red-100 text-red-800 border-red-200'
}

export default function PedidoCard({ pedido, onUpdate }) {
  const [updating, setUpdating] = useState(false)

  const updateStatus = async (newStatus) => {
    setUpdating(true)
    try {
      await api.put(`/pedidos/${pedido.id}`, { status: newStatus })
      onUpdate()
    } catch (error) {
      alert('Erro ao atualizar status')
    }
    setUpdating(false)
  }

  const totalItens = pedido.itens.reduce((sum, item) => sum + item.quantidade, 0)

  return (
    <div className="p-8 hover:bg-gray-50 transition-colors group">
      <div className="flex flex-col lg:flex-row lg:items-start lg:space-x-6 space-y-4 lg:space-y-0">
        {/* Info Principal */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-3">
            <div className={`px-3 py-1 rounded-full text-sm font-medium border ${STATUS_COLORS[pedido.status] || 'bg-gray-100 text-gray-800 border-gray-200'}`}>
              {pedido.status.replace('_', ' ').toUpperCase()}
            </div>
            <h3 className="text-xl font-bold text-gray-900">{pedido.cliente.nome}</h3>
          </div>
          
          <div className="mt-2 flex items-center text-sm text-gray-500 space-x-4">
            <span>📞 {pedido.cliente.telefone}</span>
            {pedido.cliente.whatsapp && <span>📱 {pedido.cliente.whatsapp}</span>}
            {pedido.data_entrega && <span>📅 {new Date(pedido.data_entrega).toLocaleDateString('pt-BR')}</span>}
          </div>
          
          {totalItens > 0 && (
            <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm bg-gray-50 p-4 rounded-xl">
              {pedido.itens.reduce((acc, item) => {
                acc[item.tamanho] = (acc[item.tamanho] || 0) + item.quantidade
                return acc
              }, {}).entries().map(([tamanho, qtd]) => (
                <div key={tamanho} className="text-center">
                  <div className="font-semibold text-gray-900">{qtd}</div>
                  <div className="text-xs text-gray-500">{tamanho}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Valores */}
        <div className="text-right lg:text-left">
          <div className="bg-gradient-to-r from-gray-50 to-gray-100 p-4 rounded-xl">
            <div className="space-y-1">
              <div className="flex justify-between text-sm text-gray-500">
                <span>Total:</span>
                <span className="font-semibold">R$ {pedido.valor_total.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm text-gray-500">
                <span>Entrada:</span>
                <span className="font-semibold">R$ {pedido.valor_entrada.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-lg font-bold text-gray-900 pt-1 border-t">
                <span>Restante:</span>
                <span className={pedido.valor_restante === 0 ? 'text-green-600' : 'text-red-600'}>
                  R$ {pedido.valor_restante.toFixed(2)}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Botões de Ação */}
      <div className="flex flex-wrap items-center gap-3 mt-6 pt-6 border-t border-gray-100">
        <div className="flex flex-wrap gap-2 flex-1">
          {['pendente', 'entrada_paga', 'em_producao', 'pronto', 'entregue'].map((status) => (
            <button
              key={status}
              onClick={() => updateStatus(status)}
              disabled={updating || pedido.status === status}
              className={`px-4 py-2 text-xs font-medium rounded-lg transition-all ${
                pedido.status === status
                  ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                  : 'bg-purple-600 hover:bg-purple-700 text-white shadow-sm hover:shadow-md'
              } ${updating ? 'opacity-50' : ''}`}
            >
              {status.replace('_', ' ').toUpperCase()}
            </button>
          ))}
        </div>
        
        <button
          onClick={() => window.open(`/api/pedidos/${pedido.id}`, '_blank')}
          className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm font-medium transition-colors"
        >
          PDF
        </button>
      </div>

      {pedido.observacoes_geral && (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-xl">
          <p className="text-sm text-blue-800">{pedido.observacoes_geral}</p>
        </div>
      )}
    </div>
  )
}
