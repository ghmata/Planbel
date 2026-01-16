import { useWizard } from '@/contexts/WizardContext';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { DINAMICAS, AVALIACOES } from '@/types/plan';
import { User, Users, UsersRound, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';

const iconMap = {
  User,
  Users,
  UsersRound,
};

const duracoes = [
  { value: '50', label: '50 min', desc: '1 aula' },
  { value: '100', label: '100 min', desc: '2 aulas' },
  { value: '150', label: '150 min', desc: '3 aulas' },
];

export function Step2Pedagogia() {
  const { data, setData } = useWizard();

  const toggleDinamica = (id: string) => {
    setData(prev => ({
      ...prev,
      dinamicas: prev.dinamicas.includes(id)
        ? prev.dinamicas.filter(d => d !== id)
        : [...prev.dinamicas, id],
    }));
  };

  const toggleAvaliacao = (avaliacao: string) => {
    setData(prev => ({
      ...prev,
      avaliacoes: prev.avaliacoes.includes(avaliacao)
        ? prev.avaliacoes.filter(a => a !== avaliacao)
        : [...prev.avaliacoes, avaliacao],
    }));
  };

  return (
    <div className="space-y-6 sm:space-y-8">
      <div>
        <h2 className="text-lg sm:text-xl font-semibold mb-2 select-none">Objetivos de Aprendizagem</h2>
        <p className="text-muted-foreground text-xs sm:text-sm mb-4 select-none">
          Descreva o que os alunos devem aprender nesta aula
        </p>
        <Textarea
          placeholder="Ex: Ao final da aula, os alunos deverão ser capazes de identificar e resolver problemas envolvendo frações..."
          value={data.objetivos}
          onChange={(e) => setData(prev => ({ ...prev, objetivos: e.target.value }))}
          className="min-h-[100px] sm:min-h-[120px] resize-none text-sm"
        />
      </div>

      <div>
        <h2 className="text-lg sm:text-xl font-semibold mb-2 select-none">Duração da Aula</h2>
        <p className="text-muted-foreground text-xs sm:text-sm mb-4 select-none">
          Selecione o tempo total disponível
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {duracoes.map(({ value, label, desc }) => (
            <button
              key={value}
              onClick={() => setData(prev => ({ ...prev, duracao: value as typeof data.duracao }))}
              className={cn(
                'rounded-2xl p-3 sm:p-4 border-2 transition-all text-center min-h-[70px]',
                data.duracao === value
                  ? 'border-primary bg-primary/5'
                  : 'border-border hover:border-primary/50'
              )}
            >
              <Clock className={cn(
                'h-6 w-6 mx-auto mb-2',
                data.duracao === value ? 'text-primary' : 'text-muted-foreground'
              )} />
              <p className="font-semibold">{label}</p>
              <p className="text-xs text-muted-foreground">{desc}</p>
            </button>
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-lg sm:text-xl font-semibold mb-2 select-none">Dinâmicas de Interação</h2>
        <p className="text-muted-foreground text-xs sm:text-sm mb-4 select-none">
          Como os alunos vão trabalhar durante a aula
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {DINAMICAS.map(({ id, label, icon }) => {
            const Icon = iconMap[icon as keyof typeof iconMap];
            const isSelected = data.dinamicas.includes(id);
            return (
              <button
                key={id}
                onClick={() => toggleDinamica(id)}
                className={cn(
                  'rounded-2xl p-3 sm:p-4 border-2 transition-all text-center min-h-[70px]',
                  isSelected
                    ? 'border-primary bg-primary/5'
                    : 'border-border hover:border-primary/50'
                )}
              >
                <Icon className={cn(
                  'h-6 w-6 mx-auto mb-2',
                  isSelected ? 'text-primary' : 'text-muted-foreground'
                )} />
                <p className={cn('text-sm font-medium', isSelected && 'text-primary')}>
                  {label}
                </p>
              </button>
            );
          })}
        </div>
      </div>

      <div>
        <h2 className="text-lg sm:text-xl font-semibold mb-2 select-none">Métodos de Avaliação</h2>
        <p className="text-muted-foreground text-xs sm:text-sm mb-4 select-none">
          Como você vai avaliar o aprendizado
        </p>
        <div className="flex flex-wrap gap-2">
          {AVALIACOES.map(avaliacao => (
            <Badge
              key={avaliacao}
              variant={data.avaliacoes.includes(avaliacao) ? 'default' : 'outline'}
              className={cn(
                'cursor-pointer transition-all py-2 px-3 sm:px-4 text-xs sm:text-sm min-h-[44px] flex items-center',
                data.avaliacoes.includes(avaliacao) && 'bg-primary text-primary-foreground'
              )}
              onClick={() => toggleAvaliacao(avaliacao)}
            >
              {avaliacao}
            </Badge>
          ))}
        </div>
      </div>
    </div>
  );
}
