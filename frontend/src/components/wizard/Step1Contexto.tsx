import { useWizard } from '@/contexts/WizardContext';
import { Plus, X, BookOpen } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { DISCIPLINAS_OPCOES, SERIES, Disciplina } from '@/types/plan';
import { useState } from 'react';
import { cn } from '@/lib/utils';

export function Step1Contexto() {
  const { data, setData } = useWizard();
  const [novoConteudo, setNovoConteudo] = useState<Record<string, string>>({});

  const addDisciplina = (nome: string) => {
    if (data.disciplinas.find(d => d.nome === nome)) return;
    const novaDisciplina: Disciplina = {
      id: Date.now().toString(36) + Math.random().toString(36).substr(2),
      nome,
      conteudos: [],
    };
    setData(prev => ({
      ...prev,
      disciplinas: [...prev.disciplinas, novaDisciplina],
    }));
  };

  const removeDisciplina = (id: string) => {
    setData(prev => ({
      ...prev,
      disciplinas: prev.disciplinas.filter(d => d.id !== id),
    }));
  };

  const addConteudo = (disciplinaId: string) => {
    const conteudo = novoConteudo[disciplinaId]?.trim();
    if (!conteudo) return;
    
    setData(prev => ({
      ...prev,
      disciplinas: prev.disciplinas.map(d =>
        d.id === disciplinaId
          ? { ...d, conteudos: [...d.conteudos, conteudo] }
          : d
      ),
    }));
    setNovoConteudo(prev => ({ ...prev, [disciplinaId]: '' }));
  };

  const removeConteudo = (disciplinaId: string, index: number) => {
    setData(prev => ({
      ...prev,
      disciplinas: prev.disciplinas.map(d =>
        d.id === disciplinaId
          ? { ...d, conteudos: d.conteudos.filter((_, i) => i !== index) }
          : d
      ),
    }));
  };

  const selectSerie = (serie: string, segmento: 'fundamental1' | 'fundamental2' | 'medio') => {
    setData(prev => ({ ...prev, serie, segmento }));
  };

  return (
    <div className="space-y-6 sm:space-y-8">
      <div>
        <h2 className="text-lg sm:text-xl font-semibold mb-2 select-none">Disciplinas e Conteúdos</h2>
        <p className="text-muted-foreground text-xs sm:text-sm mb-4 select-none">
          Selecione as disciplinas e adicione os conteúdos específicos da aula
        </p>

        <div className="flex flex-wrap gap-2">
          {DISCIPLINAS_OPCOES.map(nome => {
            const isSelected = data.disciplinas.some(d => d.nome === nome);
            return (
              <Badge
                key={nome}
                variant={isSelected ? 'default' : 'outline'}
                className={cn(
                  'cursor-pointer transition-all py-2 px-3 text-xs sm:text-sm min-h-[44px] flex items-center select-none',
                  isSelected && 'bg-primary text-primary-foreground',
                  !isSelected && 'hover:bg-muted'
                )}
                onClick={() => {
                  if (isSelected) {
                    removeDisciplina(data.disciplinas.find(d => d.nome === nome)!.id);
                  } else {
                    addDisciplina(nome);
                  }
                }}
              >
                {nome}
                {isSelected && (
                  <X
                    className="h-3 w-3 ml-1 cursor-pointer"
                    onClick={(e) => {
                      e.stopPropagation();
                      removeDisciplina(data.disciplinas.find(d => d.nome === nome)!.id);
                    }}
                  />
                )}
              </Badge>
            );
          })}
        </div>

        {data.disciplinas.length > 0 && (
          <div className="space-y-4 mt-4 sm:mt-6">
            {data.disciplinas.map(disciplina => (
              <div key={disciplina.id} className="rounded-2xl border p-3 sm:p-4">
                <div className="flex items-center gap-2 mb-3">
                  <BookOpen className="h-4 w-4 text-primary flex-shrink-0" />
                  <span className="font-medium text-sm sm:text-base">{disciplina.nome}</span>
                </div>
                
                <div className="flex flex-wrap gap-2 mb-3">
                  {disciplina.conteudos.map((conteudo, index) => (
                    <Badge key={index} variant="secondary" className="py-1.5 text-xs">
                      {conteudo}
                      <X
                        className="h-3 w-3 ml-1.5 cursor-pointer hover:text-destructive"
                        onClick={() => removeConteudo(disciplina.id, index)}
                      />
                    </Badge>
                  ))}
                </div>
                
                <div className="flex gap-2">
                  <Input
                    placeholder="Adicionar conteúdo..."
                    className="text-sm"
                    value={novoConteudo[disciplina.id] || ''}
                    onChange={(e) => setNovoConteudo(prev => ({ ...prev, [disciplina.id]: e.target.value }))}
                    onKeyPress={(e) => e.key === 'Enter' && addConteudo(disciplina.id)}
                  />
                  <Button type="button" size="icon" className="h-10 w-10 flex-shrink-0" onClick={() => addConteudo(disciplina.id)}>
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <h2 className="text-lg sm:text-xl font-semibold mb-2 select-none">Série Escolar</h2>
        <p className="text-muted-foreground text-xs sm:text-sm mb-4 select-none">
          Selecione a série ou ano de ensino
        </p>

        <Tabs
          value={data.segmento}
          onValueChange={(v) => setData(prev => ({ ...prev, segmento: v as typeof data.segmento, serie: '' }))}
        >
          <TabsList className="w-full grid grid-cols-3 mb-4 h-11">
            <TabsTrigger value="fundamental1" className="text-xs sm:text-sm">Fund. I</TabsTrigger>
            <TabsTrigger value="fundamental2" className="text-xs sm:text-sm">Fund. II</TabsTrigger>
            <TabsTrigger value="medio" className="text-xs sm:text-sm">Médio</TabsTrigger>
          </TabsList>

          {Object.entries(SERIES).map(([segmento, series]) => (
            <TabsContent key={segmento} value={segmento} className="mt-0">
              <div className="flex flex-wrap gap-2">
                {series.map(serie => (
                  <Badge
                    key={serie}
                    variant={data.serie === serie ? 'default' : 'outline'}
                    className={cn(
                      'cursor-pointer transition-all py-2 px-3 sm:px-4 text-xs sm:text-sm min-h-[44px] flex items-center select-none',
                      data.serie === serie && 'bg-primary text-primary-foreground'
                    )}
                    onClick={() => selectSerie(serie, segmento as typeof data.segmento)}
                  >
                    {serie}
                  </Badge>
                ))}
              </div>
            </TabsContent>
          ))}
        </Tabs>
      </div>

    </div>
  );
}
