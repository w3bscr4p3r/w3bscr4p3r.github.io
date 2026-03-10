export default function Totais({ totais }) {
  const tamanhos = {
    'P': 'Pequeno',
    'M': 'Médio', 
    'G': 'Grande',
    'GG': 'G.Gigante'
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-gradient-to-br from-purple-600 to-indigo-600 rounded-2xl p-8 text-white shadow-2xl">
        <h3 className="text-2xl font-bold mb-6">📊 Totais por Tamanho</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          {Object.entries(totais).map(([tamanho, total]) => (
            <div key={tamanho} className="group">
              <div className="text-3xl font-bold bg-white/20 rounded-2xl p-4 mb-2 backdrop-blur-sm group-hover:bg-white/30 transition-all">
                {total}
              </div>
              <div className="text-sm opacity-90">{tamanhos[tamanho] || tamanho}</div>
            </div>
          ))}
        </div>
      </div>
      
      <div className="bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl p-8 text-white shadow-2xl">
        <h3 className="text-2xl font-bold mb-4">🎯 Status dos Pedidos</h3>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold bg-white/20 rounded-xl p-3 mb-1">0</div>
            <div className="text-sm opacity-90">Pendente</div>
          </div>
          <div>
            <div className="text-2xl font-bold bg-white/20 rounded-xl p-3 mb-1">{totais.pendente || 0}</div>
            <div className="text-sm opacity-90">Em Produção</div>
          </div>
          <div>
            <div className="text-2xl font-bold bg-white/20 rounded-xl p-3 mb-1">{totais.pronto || 0}</div>
            <div className="text-sm opacity-90">Pronto</div>
          </div>
        </div>
      </div>
    </div>
  )
}
