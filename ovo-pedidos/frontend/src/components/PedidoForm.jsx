import { useState } from 'react'
import api from '../services/api'

export default function PedidoForm({ onSuccess }) {
  const [formData, setFormData] = useState({
    cliente_nome: '',
    cliente_telefone: '',
    cliente_whatsapp: '',
    cliente_endereco: '',
    data_entrega: '',
    observacoes_geral: '',
    itens: [{ tipo_item: 'ovo', tamanho: 'M', quantidade: 1, preco_unitario: 50 }]
  })
  const [loading, setLoading] = useState(false)

  const addItem = () => {
    setFormData({
      ...formData,
      itens: [...formData.itens, { tipo_item: 'ovo', tamanho: 'M', quantidade: 1, preco_unitario: 50 }]
    })
  }

  const updateItem = (index, field, value) => {
    const newItens = [...formData.itens]
    newItens[index] = { ...newItens[index], [field]: value }
    setFormData({ ...formData, itens: newItens })
  }

  const removeItem = (index) => {
    setFormData({
      ...formData,
      itens: formData.itens.filter((_, i) => i !== index)
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      await api.post('/pedidos', formData)
      onSuccess()
      setFormData({
        cliente_nome: '',
        cliente_telefone: '',
        cliente_whatsapp: '',
        cliente_endereco: '',
        data_entrega: '',
        observacoes_geral: '',
        itens: [{ tipo_item: 'ovo', tamanho: 'M', quantidade: 1, preco_unitario: 50 }]
      })
      alert('Pedido criado com sucesso!')
    } catch (error) {
      alert('Erro ao criar pedido: ' + error.message)
    }
    setLoading(false)
  }

  const total = formData.itens.reduce((sum, item) => sum + (item.quantidade * item.preco_unitario), 0)
  const entrada = total * 0.5

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-2xl shadow-xl p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-8">Novo Pedido</h2>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Cliente */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Nome do Cliente *</label>
              <input
                required
                type="text"
                value={formData.cliente_nome}
                onChange={(e) => setFormData({ ...formData, cliente_nome: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Telefone *</label>
              <input
                required
                type="tel"
                value={formData.cliente_telefone}
                onChange={(e) => setFormData({ ...formData, cliente_telefone: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Data Entrega e Endereço */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Data Entrega</label>
              <input
                type="date"
                value={formData.data_entrega}
                onChange={(e) => setFormData({ ...formData, data_entrega: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Endereço</label>
              <input
                type="text"
                value={formData.cliente_endereco}
                onChange={(e) => setFormData({ ...formData, cliente_endereco: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Itens */}
          <div>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-800">Itens do Pedido</h3>
              <button
                type="button"
                onClick={addItem}
                className="px-4 py-2 bg-green-600 text-white rounded-xl hover:bg-green-700 transition-colors"
              >
                + Adicionar Item
              </button>
            </div>
            
            <div className="space-y-3">
              {formData.itens.map((item, index) => (
                <div key={index} className="bg-gray-50 p-6 rounded-xl border border-gray-200">
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
                      <select
                        value={item.tipo_item}
                        onChange={(e) => updateItem(index, 'tipo_item', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="ovo">Ovo</option>
                        <option value="casca">Casca</option>
                        <option value="recheio">Recheio</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Tamanho</label>
                      <select
                        value={item.tamanho}
                        onChange={(e) => updateItem(index, 'tamanho', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="P">Pequeno</option>
                        <option value="M">Médio</option>
                        <option value="G">Grande</option>
                        <option value="GG">G.Gigante</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Qtd</label>
                      <input
                        type="number"
                        min="1"
                        value={item.quantidade}
                        onChange={(e) => updateItem(index, 'quantidade', parseInt(e.target.value))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div className="space-y-2">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Preço Unit.</label>
                        <input
                          type="number"
                          step="0.01"
                          min="0"
                          value={item.preco_unitario}
                          onChange={(e) => updateItem(index, 'preco_unitario', parseFloat(e.target.value))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                      <button
                        type="button"
                        onClick={() => removeItem(index)}
                        className="w-full px-3 py-2 text-red-600 border border-red-300 rounded-lg hover:bg-red-50 transition-colors text-sm"
                      >
                        Remover
                      </button>
                    </div>
                  </div>
                  <div className="mt-3">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Observações</label>
                    <input
                      type="text"
                      value={item.observacoes}
                      onChange={(e) => updateItem(index, 'observacoes', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                      placeholder="Recheio especial, sem amendoim, etc..."
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Totais e Observações */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-gradient-to-r from-purple-50 to-indigo-50 p-6 rounded-xl">
              <h4 className="font-semibold text-gray-800 mb-3">Totais</h4>
              <div className="space-y-2 text-lg">
                <div className="flex justify-between">
                  <span>Total:</span>
                  <span>R$ {total.toFixed(2)}</span>
                </div>
                <div className="flex justify-between font-semibold text-purple-600 text-xl border-t pt-2">
                  <span>Entrada 50%:</span>
                  <span>R$ {entrada.toFixed(2)}</span>
                </div>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Observações Gerais</label>
              <textarea
                value={formData.observacoes_geral}
                onChange={(e) => setFormData({ ...formData, observacoes_geral: e.target.value })}
                rows="3"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-vertical"
                placeholder="Informações importantes do pedido..."
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || formData.itens.length === 0}
            className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 text-white py-4 px-8 rounded-xl text-lg font-semibold hover:from-purple-700 hover:to-indigo-700 focus:ring-4 focus:ring-purple-500 focus:outline-none transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-xl"
          >
            {loading ? 'Salvando...' : `Criar Pedido (R$ ${total.toFixed(2)})`}
          </button>
        </form>
      </div>
    </div>
  )
}
