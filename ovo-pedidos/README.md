# 🥚 Gestão Pedidos Ovos Páscoa

## 🚀 Como Rodar Localmente

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

Frontend
bash
cd frontend
npm install
npm run dev
🌐 Acessar
Backend API: http://localhost:8000/docs

Frontend: http://localhost:3000

📱 Funcionalidades
✅ Cadastro completo de pedidos com 50% entrada automática
✅ Dashboard com totais por tamanho (P/M/G/GG)
✅ Filtros por status e cliente
✅ Controle de fluxo (Pendente → Produção → Pronto → Entregue)
✅ Design mobile-first responsivo
✅ SQLite zero-config (migra fácil para PostgreSQL)
