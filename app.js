const year = document.querySelector('#year');
if (year) year.textContent = new Date().getFullYear();

const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');
menuToggle?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(open));
});
nav?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  nav.classList.remove('open');
  menuToggle?.setAttribute('aria-expanded', 'false');
}));

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const delay = entry.target.dataset.delay || 0;
      setTimeout(() => entry.target.classList.add('visible'), Number(delay));
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

const cursorGlow = document.querySelector('.cursor-glow');
window.addEventListener('pointermove', (e) => {
  if (!cursorGlow) return;
  cursorGlow.style.left = `${e.clientX}px`;
  cursorGlow.style.top = `${e.clientY}px`;
}, { passive: true });

const filters = document.querySelectorAll('.filter');
const cards = document.querySelectorAll('.project-card');
filters.forEach(btn => btn.addEventListener('click', () => {
  filters.forEach(f => f.classList.remove('active'));
  btn.classList.add('active');
  const filter = btn.dataset.filter;
  cards.forEach(card => {
    const categories = card.dataset.category?.split(' ') || [];
    card.classList.toggle('hidden', filter !== 'all' && !categories.includes(filter));
  });
}));

const modal = document.querySelector('#project-modal');
const modalContent = document.querySelector('#modal-content');
const modalClose = document.querySelector('.modal-close');

const projectData = {
  'wolf-grc': {
    kicker: 'FLAGSHIP // GRC PLATFORM',
    title: 'WOLF GRC',
    text: 'Plataforma orientada à entrega de GRCaaS e vCISO, conectando risco, controles, evidências, métricas e contexto técnico em uma experiência executiva.',
    items: ['Risk Register', 'Controles & Evidências', 'vCISO Dashboard', 'ISO 27001 / NIST CSF', 'Integração SIEM/ITSM', 'AI Copilot / RAG']
  },
  'wolf-ucp': {
    kicker: 'UNIFIED CYBER PLATFORM',
    title: 'WOLF UCP',
    text: 'Camada de integração para consolidar sinais de segurança e observabilidade, reduzindo silos entre ferramentas e entregando contexto operacional em tempo quase real.',
    items: ['SIEM / SOAR', 'Firewall / IDS', 'CTI', 'ITSM', 'Observabilidade', 'Contextualização de risco']
  },
  'cyber-agent': {
    kicker: 'CYBER REASONING ENGINE',
    title: 'WOLF Cyber Agent',
    text: 'Agente de IA focado em raciocínio de segurança, enriquecimento contextual e apoio à resposta. Projetado para trabalhar com modelos locais e integração controlada com fontes externas.',
    items: ['FastAPI', 'RAG', 'Ollama', 'Local LLM', 'Wazuh', 'pfSense / Suricata']
  },
  'wolf-cti': {
    kicker: 'THREAT INTELLIGENCE',
    title: 'WOLF CTI',
    text: 'Plataforma para agregar e enriquecer indicadores, vulnerabilidades e inteligência de ameaças a partir de múltiplas fontes abertas e comerciais.',
    items: ['OTX', 'NVD', 'CISA KEV', 'ThreatFox', 'URLhaus', 'MITRE ATT&CK']
  },
  'ot-sentinel': {
    kicker: 'OT / XIOT SECURITY',
    title: 'OT Sentinel',
    text: 'Visibilidade e gestão de risco para ambientes industriais e infraestrutura crítica, priorizando continuidade operacional e segurança defensiva.',
    items: ['Asset Discovery', 'Risk Scoring', 'OT Monitoring', 'Exposure Management', 'Threat Detection', 'Operational Resilience']
  },
  'wjp': {
    kicker: 'INTEROPERABILITY LAYER',
    title: 'WJP Protocol',
    text: 'Padrão de comunicação estruturada em JSON para integrações previsíveis entre serviços, APIs e agentes de IA dentro do ecossistema WOLF.',
    items: ['JSON-first', 'Schema Validation', 'API Contracts', 'Agent Messages', 'Auditability', 'Loose Coupling']
  }
};

document.querySelectorAll('[data-modal]').forEach(btn => btn.addEventListener('click', () => {
  const data = projectData[btn.dataset.modal];
  if (!data || !modalContent || !modal) return;
  modalContent.innerHTML = `
    <span class="modal-kicker">${data.kicker}</span>
    <h3 class="modal-title">${data.title}</h3>
    <p class="modal-text">${data.text}</p>
    <ul class="modal-list">${data.items.map(item => `<li>${item}</li>`).join('')}</ul>
  `;
  modal.showModal();
}));
modalClose?.addEventListener('click', () => modal?.close());
modal?.addEventListener('click', (e) => {
  if (e.target === modal) modal.close();
});
