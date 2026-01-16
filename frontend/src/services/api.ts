/**
 * PlanBel 2.0 - API Service
 * Centraliza todas as chamadas ao backend Flask
 */

// Detecta automaticamente o IP se estiver rodando localmente (para acesso mobile)
const getBaseUrl = () => {
  if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  // Se estiver no localhost ou IP local, assume que o backend está na porta 5000 do mesmo host
  if (window.location.hostname === 'localhost' || window.location.hostname.match(/^192\.168\./)) {
    return `http://${window.location.hostname}:5000`;
  }
  return 'http://localhost:5000';
};

const API_URL = getBaseUrl();

// Helper para headers (inclui token do Hugging Face se existir)
const getHeaders = () => {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  const hfToken = import.meta.env.VITE_HF_TOKEN;
  if (hfToken) {
    headers['Authorization'] = `Bearer ${hfToken}`;
  }
  
  return headers;
};

interface WizardData {
  disciplinas: { id: string; nome: string; conteudos: string[] }[];
  serie: string;
  segmento: 'fundamental1' | 'fundamental2' | 'medio';
  objetivos: string;
  duracao: string;
  dinamicas: string[];
  avaliacoes: string[];
  metodologias: string[];
  recursos: string[];
  materiaisDisponiveis: string[];
  materiaisCustom: string;
  permitirExtras: boolean;
  observacoes: string;
  gerarMaterialImpresso: boolean;
  detalhesGamificacao?: string;
}

interface CronogramaItem {
  etapa: string;
  tempo: string;
  descricao: string;
}

interface GeneratedPlan {
  id: string;
  titulo: string;
  serie: string;
  duracao: string;
  disciplinas: string[];
  introducao: string;
  desenvolvimento: string;
  fechamento: string;
  cronograma: CronogramaItem[];
  competenciasBNCC: string[];
  materiaisNecessarios: string[];
  status: 'gerado' | 'rascunho';
  createdAt: string;
  gerarMaterialImpresso?: boolean;
  metodologia?: string;
  detalhesGamificacao?: string;
}

interface ApiResponse {
  success: boolean;
  plan?: GeneratedPlan;
  tokens?: number;
  error?: string;
}

/**
 * Gera um plano de aula usando o backend Flask (endpoint estruturado)
 * Envia TODOS os dados coletados no wizard
 */
export async function generatePlan(wizardData: WizardData): Promise<GeneratedPlan> {
  // Mapear TODOS os dados do wizard para o Flask
  const requestBody = {
    // Disciplinas (todas, não só a primeira)
    disciplinas: wizardData.disciplinas.map(d => ({
      nome: d.nome,
      conteudos: d.conteudos
    })),
    disciplina: wizardData.disciplinas[0]?.nome || 'Matemática',
    
    // Série e segmento
    ano_escolar: wizardData.serie,
    segmento: wizardData.segmento,
    
    // Tema/Conteúdos (combina todos os conteúdos selecionados)
    tema: wizardData.disciplinas
      .flatMap(d => d.conteudos)
      .join(', ') || 'Tema geral',
    
    // Objetivos de aprendizagem (campo importante que não estava sendo enviado!)
    objetivos: wizardData.objetivos,
    
    // Duração
    duracao: wizardData.duracao || '50',
    
    // Dinâmicas de interação (Individual, Duplas, Grupos)
    dinamicas: wizardData.dinamicas,
    
    // Tipos de avaliação selecionados
    avaliacoes: wizardData.avaliacoes,
    
    // TODAS as metodologias (não só a primeira)
    metodologias: wizardData.metodologias,
    metodologia: wizardData.metodologias.join(', ') || null,
    
    // Recursos digitais
    recursos: wizardData.recursos,
    
    // Materiais físicos disponíveis
    materiais_disponiveis: wizardData.materiaisDisponiveis,
    
    // Materiais customizados pelo professor
    materiais_custom: wizardData.materiaisCustom,
    detalhes_gamificacao: wizardData.detalhesGamificacao,
    
    // Permite usar materiais extras?
    permitir_extras: wizardData.permitirExtras,
    
    // Observações da turma
    observacoes: wizardData.observacoes || null,
    
    // Flag para gerar sugestão de material impresso
    gerar_material_impresso: wizardData.gerarMaterialImpresso || false,
  };

  const response = await fetch(`${API_URL}/api/gerar-plano-estruturado`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
  }

  const data: ApiResponse = await response.json();

  if (!data.success || !data.plan) {
    throw new Error(data.error || 'Erro ao gerar plano');
  }

  // Garantir que todos os campos existem
  const plan: GeneratedPlan = {
    id: data.plan.id || crypto.randomUUID(),
    titulo: data.plan.titulo || 'Plano de Aula',
    serie: data.plan.serie || wizardData.serie,
    duracao: data.plan.duracao || wizardData.duracao,
    disciplinas: data.plan.disciplinas || wizardData.disciplinas.map(d => d.nome),
    introducao: data.plan.introducao || '',
    desenvolvimento: data.plan.desenvolvimento || '',
    fechamento: data.plan.fechamento || '',
    cronograma: data.plan.cronograma || [],
    competenciasBNCC: data.plan.competenciasBNCC || [],
    materiaisNecessarios: data.plan.materiaisNecessarios || [],
    status: 'gerado',
    createdAt: data.plan.createdAt || new Date().toISOString(),
    gerarMaterialImpresso: data.plan.gerarMaterialImpresso,
    metodologia: data.plan.metodologia,
    detalhesGamificacao: data.plan.detalhesGamificacao,
  };

  return plan;
}

/**
 * Verifica se o backend está online
 */
export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/api/health`, {
      headers: getHeaders()
    });
    const data = await response.json();
    return data.status === 'ok';
  } catch {
    return false;
  }
}

interface MaterialResponse {
  success: boolean;
  html?: string;
  titulo?: string;
  error?: string;
}

/**
 * Gera material impresso em HTML baseado no plano de aula
 */
export async function generatePrintableMaterial(plan: GeneratedPlan): Promise<MaterialResponse> {
  const response = await fetch(`${API_URL}/api/gerar-material`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ plano: plan }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
  }

  const data: MaterialResponse = await response.json();

  if (!data.success || !data.html) {
    throw new Error(data.error || 'Erro ao gerar material');
  }

  return data;
}

/**
 * Gera material de JOGO educativo personalizado
 */
export async function generateGame(plan: GeneratedPlan): Promise<MaterialResponse> {
  const response = await fetch(`${API_URL}/api/gerar-jogo`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ plano: plan }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
  }

  const data: MaterialResponse = await response.json();

  if (!data.success || !data.html) {
    throw new Error(data.error || 'Erro ao gerar jogo');
  }

  return data;
}

/**
 * Abre o HTML em nova aba para impressão/download como PDF
 */
export function openHtmlForPrint(html: string, titulo: string) {
  const printWindow = window.open('', '_blank');
  if (printWindow) {
    printWindow.document.write(html);
    printWindow.document.close();
    printWindow.document.title = titulo;
  }
}

/**
 * Gera um HTML limpo e profissional para exportação de PDF do plano de aula
 */
export function generateCleanPlanHTML(plan: GeneratedPlan): string {
  const styles = `
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    body {
      font-family: 'Roboto', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      margin: 0;
      padding: 0;
      background: #fff;
    }
    
    .container {
      max-width: 800px;
      margin: 0 auto;
      padding: 40px;
    }
    
    header {
      border-bottom: 2px solid #2563eb;
      padding-bottom: 20px;
      margin-bottom: 30px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }
    
    .header-content h1 {
      margin: 0;
      color: #1e3a8a;
      font-size: 24pt;
    }
    
    .meta-tags {
      display: flex;
      gap: 10px;
      margin-top: 10px;
      font-size: 10pt;
      color: #64748b;
    }
    
    .meta-tag {
      background: #f1f5f9;
      padding: 4px 8px;
      border-radius: 4px;
      border: 1px solid #e2e8f0;
    }
    
    .section {
      margin-bottom: 30px;
      page-break-inside: avoid;
    }
    
    h2 {
      color: #2563eb;
      font-size: 16pt;
      border-left: 4px solid #fbbf24;
      padding-left: 10px;
      margin-bottom: 15px;
    }
    
    .content-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 15px;
      border-radius: 8px;
      white-space: pre-wrap;
    }
    
    .bncc-box {
      background: #ecfdf5;
      border: 1px solid #10b981;
      padding: 15px;
      border-radius: 8px;
      color: #065f46;
      font-size: 10pt;
    }
    
    .materials-box {
      background: #fffbeb;
      border: 1px solid #f59e0b;
      padding: 15px;
      border-radius: 8px;
      color: #92400e;
      font-size: 10pt;
    }
    
    .cronograma-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
    }
    
    .cronograma-table th, .cronograma-table td {
      border: 1px solid #cbd5e1;
      padding: 8px 12px;
      text-align: left;
    }
    
    .cronograma-table th {
      background: #f1f5f9;
      color: #1e293b;
    }
    
    footer {
      margin-top: 50px;
      border-top: 1px solid #e2e8f0;
      padding-top: 20px;
      text-align: center;
      font-size: 9pt;
      color: #94a3b8;
    }
    
    @media print {
      body { -webkit-print-color-adjust: exact; }
      .container { width: 100%; max-width: none; padding: 20px; }
    }
  `;

  return `
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <title>${plan.titulo}</title>
      <style>${styles}</style>
    </head>
    <body>
      <div class="container">
        <header>
          <div class="header-content">
            <h1>${plan.titulo}</h1>
            <div class="meta-tags">
              <span class="meta-tag">📚 ${plan.disciplinas.join(', ')}</span>
              <span class="meta-tag">🎓 ${plan.serie}</span>
              <span class="meta-tag">⏱️ ${plan.duracao} min</span>
            </div>
          </div>
          <div style="text-align: right; color: #94a3b8; font-size: 10pt;">
            PLANO DE AULA<br>
            <strong>PlanBel 2.0</strong>
          </div>
        </header>

        <div class="section">
          <h2>🎯 Competências BNCC</h2>
          <div class="bncc-box">
            ${plan.competenciasBNCC.map(c => `<div>✅ ${c}</div>`).join('')}
          </div>
        </div>

        <div class="section">
          <h2>📝 Introdução</h2>
          <div class="content-box">${plan.introducao}</div>
        </div>

        <div class="section">
          <h2>🚀 Desenvolvimento</h2>
          <div class="content-box">${plan.desenvolvimento}</div>
        </div>

        <div class="section">
          <h2>🏁 Fechamento e Avaliação</h2>
          <div class="content-box">${plan.fechamento}</div>
        </div>

        <div class="section">
          <h2>📅 Cronograma Detalhado</h2>
          <table class="cronograma-table">
            <thead>
              <tr>
                <th style="width: 20%">Etapa</th>
                <th style="width: 15%">Tempo</th>
                <th>Descrição</th>
              </tr>
            </thead>
            <tbody>
              ${plan.cronograma.map(item => `
                <tr>
                  <td><strong>${item.etapa}</strong></td>
                  <td>${item.tempo}</td>
                  <td>${item.descricao}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>

        <div class="section">
          <h2>✂️ Materiais Necessários</h2>
          <div class="materials-box">
            ${plan.materiaisNecessarios.join('<br>')}
          </div>
        </div>

        <footer>
          <p>Documento gerado automaticamente pelo assistente pedagógico PlanBel 2.0</p>
          <p>${new Date().toLocaleDateString('pt-BR')} • Página 1 de 1</p>
        </footer>
      </div>
    </body>
    </html>
  `;
}
