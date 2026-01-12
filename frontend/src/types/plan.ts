export interface Disciplina {
  id: string;
  nome: string;
  conteudos: string[];
}

export interface WizardData {
  // Etapa 1 - Contexto
  disciplinas: Disciplina[];
  serie: string;
  segmento: 'fundamental1' | 'fundamental2' | 'medio';
  
  // Etapa 2 - Pedagogia
  objetivos: string;
  duracao: '50' | '100' | '150';
  dinamicas: string[];
  avaliacoes: string[];
  
  // Etapa 3 - Refinamento
  metodologias: string[];
  recursos: string[];
  materiaisDisponiveis: string[];
  materiaisCustom: string;
  detalhesGamificacao?: string;
  permitirExtras: boolean;
  observacoes: string;
  gerarMaterialImpresso: boolean;
}


export interface CronogramaItem {
  etapa: string;
  tempo: string;
  descricao: string;
}

export interface PlanoGerado {
  id: string;
  titulo: string;
  introducao: string;
  desenvolvimento: string;
  fechamento: string;
  cronograma: CronogramaItem[];
  competenciasBNCC: string[];
  materiaisNecessarios: string[];
  materialImpresso?: string;
  gerarMaterialImpresso?: boolean;
  metodologia?: string;
  detalhesGamificacao?: string;
  serie: string;
  duracao: string;
  disciplinas: string[];
  status: 'gerado' | 'rascunho';
  createdAt: Date;
}

export const DISCIPLINAS_OPCOES = [
  'Matemática',
  'Língua Portuguesa',
  'História',
  'Geografia',
  'Ciências',
  'Biologia',
  'Física',
  'Química',
  'Educação Física',
  'Arte',
  'Inglês',
  'Filosofia',
  'Sociologia',
];

export const SERIES = {
  fundamental1: ['1º Ano', '2º Ano', '3º Ano', '4º Ano', '5º Ano'],
  fundamental2: ['6º Ano', '7º Ano', '8º Ano', '9º Ano'],
  medio: ['1ª Série', '2ª Série', '3ª Série'],
};

export const DINAMICAS = [
  { id: 'individual', label: 'Individual', icon: 'User' },
  { id: 'duplas', label: 'Em Duplas', icon: 'Users' },
  { id: 'grupos', label: 'Em Grupos', icon: 'UsersRound' },
];

export const AVALIACOES = [
  'Observação',
  'Rubrica',
  'Quiz',
  'Autoavaliação',
  'Portfólio',
  'Apresentação',
  'Debate',
  'Mapa Mental',
  'Seminário',
  'Lista de Exercícios',
];

export const METODOLOGIAS = [
  { id: 'gamificacao', label: 'Gamificação', desc: 'Elementos de jogos na aprendizagem' },
  { id: 'pbl', label: 'PBL', desc: 'Aprendizagem baseada em projetos' },
  { id: 'invertida', label: 'Aula Invertida', desc: 'Estudo prévio + prática em sala' },
  { id: 'steam', label: 'STEAM', desc: 'Ciência, Tecnologia, Engenharia, Artes e Matemática' },
  { id: 'peer_instruction', label: 'Instr. por Pares', desc: 'Alunos ensinam uns aos outros' },
  { id: 'design_thinking', label: 'Design Thinking', desc: 'Solução criativa de problemas' },
  { id: 'rotacao', label: 'Rotação', desc: 'Rodízio por estações de atividades' },
  { id: 'estudo_caso', label: 'Estudo de Caso', desc: 'Análise de situações reais' },
];

export const RECURSOS = [
  'Vídeos',
  'Slides',
  'Jogos Digitais',
  'Podcasts',
  'Infográficos',
  'Mapas Mentais',
  'Simuladores',
  'Artigos/Textos',
  'Aplicativos',
];

export const MATERIAIS = [
  'Quadro/Lousa',
  'Projetor',
  'Computadores',
  'Tablets/Celulares',
  'Internet/Wi-Fi',
  'Material Impresso',
  'Materiais de Arte',
  'Jogos de Tabuleiro',
  'Espaço ao Ar Livre',
  'Biblioteca',
  'Laboratório',
  'Materiais Manipuláveis',
];

export const GAMIFICACAO_OPCOES = [
  'Sistema de pontos e recompensas',
  'Competições em equipes',
  'Jogos educativos físicos ou digitais',
  'Escape room pedagógico',
  'Quiz interativo (Kahoot, Mentimeter)',
  'Jogo das 3 pistas',
  'Show do Milhão pedagógico',
  'Gartic educativo (desenho e adivinhação)',
  'Batata quente com perguntas',
  'Bingo de conceitos/respostas',
  'Caça ao tesouro pedagógico',
  'Outro (especificar nas observações)',
];

export const initialWizardData: WizardData = {
  disciplinas: [],
  serie: '',
  segmento: 'fundamental1',
  objetivos: '',
  duracao: '50',
  dinamicas: [],
  avaliacoes: [],
  metodologias: [],
  recursos: [],
  materiaisDisponiveis: [],
  materiaisCustom: '',
  detalhesGamificacao: '',
  permitirExtras: false,
  observacoes: '',
  gerarMaterialImpresso: false,
};
