import { useState, useEffect } from 'react';
import { useWizard } from '@/contexts/WizardContext';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { METODOLOGIAS, RECURSOS, MATERIAIS, GAMIFICACAO_OPCOES } from '@/types/plan';
import { cn } from '@/lib/utils';
import { Gamepad2, Lightbulb, RotateCcw, Atom, AlertTriangle, Users, Brain, RefreshCw, FileText } from 'lucide-react';

const metodologiaIcons: Record<string, React.ElementType> = {
  gamificacao: Gamepad2,
  pbl: Lightbulb,
  invertida: RotateCcw,
  steam: Atom,
  peer_instruction: Users,
  design_thinking: Brain,
  rotacao: RefreshCw,
  estudo_caso: FileText,
};

const STORAGE_KEY_MATERIAL_CONSENT = 'planbel-material-impresso-consent';

export function Step3Refinamento() {
  const { data, setData } = useWizard();
  const [showConsentDialog, setShowConsentDialog] = useState(false);
  const [rememberConsent, setRememberConsent] = useState(false);
  const [consentGiven, setConsentGiven] = useState(() => {
    return localStorage.getItem(STORAGE_KEY_MATERIAL_CONSENT) === 'true';
  });

  const toggleMetodologia = (id: string) => {
    setData(prev => ({
      ...prev,
      metodologias: prev.metodologias.includes(id)
        ? prev.metodologias.filter(m => m !== id)
        : [...prev.metodologias, id],
    }));
  };

  const toggleRecurso = (recurso: string) => {
    setData(prev => ({
      ...prev,
      recursos: prev.recursos.includes(recurso)
        ? prev.recursos.filter(r => r !== recurso)
        : [...prev.recursos, recurso],
    }));
  };

  const toggleMaterial = (material: string) => {
    setData(prev => ({
      ...prev,
      materiaisDisponiveis: prev.materiaisDisponiveis.includes(material)
        ? prev.materiaisDisponiveis.filter(m => m !== material)
        : [...prev.materiaisDisponiveis, material],
    }));
  };

  const handleMaterialImpressoChange = (checked: boolean) => {
    if (checked && !consentGiven) {
      // Mostrar modal de aviso
      setShowConsentDialog(true);
    } else {
      // Se já deu consentimento ou está desmarcando, atualiza diretamente
      setData(prev => ({ ...prev, gerarMaterialImpresso: checked }));
    }
  };

  const handleConsentAccept = () => {
    if (rememberConsent) {
      localStorage.setItem(STORAGE_KEY_MATERIAL_CONSENT, 'true');
      setConsentGiven(true);
    }
    setData(prev => ({ ...prev, gerarMaterialImpresso: true }));
    setShowConsentDialog(false);
    setRememberConsent(false);
  };

  const handleConsentDecline = () => {
    setShowConsentDialog(false);
    setRememberConsent(false);
  };

  return (
    <>
      <div className="space-y-6 sm:space-y-8">
        <div>
          <h2 className="text-lg sm:text-xl font-semibold mb-2 select-none">Metodologias Ativas</h2>
          <p className="text-muted-foreground text-xs sm:text-sm mb-4 select-none">
            Selecione abordagens pedagógicas inovadoras (opcional)
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
            {METODOLOGIAS.map(({ id, label, desc }) => {
              const Icon = metodologiaIcons[id];
              const isSelected = data.metodologias.includes(id);
              return (
                <button
                  key={id}
                  onClick={() => toggleMetodologia(id)}
                  className={cn(
                    'rounded-2xl p-3 sm:p-4 border-2 transition-all text-left min-h-[80px]',
                    isSelected
                      ? 'border-accent bg-accent/10'
                      : 'border-border hover:border-accent/50'
                  )}
                >
                  <Icon className={cn(
                    'h-5 w-5 sm:h-6 sm:w-6 mb-2',
                    isSelected ? 'text-accent' : 'text-muted-foreground'
                  )} />
                  <p className={cn('text-xs sm:text-sm font-medium', isSelected && 'text-accent-foreground')}>
                    {label}
                  </p>
                  <p className="text-[10px] sm:text-xs text-muted-foreground mt-1">{desc}</p>
                </button>
              );
            })}
          </div>

          {data.metodologias.includes('gamificacao') && (
            <div className="mt-4 animate-in fade-in slide-in-from-top-2">
              <label className="text-sm font-medium mb-1.5 block">
                Detalhes da Gamificação (Opcional)
              </label>
              <Select
                value={data.detalhesGamificacao || ''}
                onValueChange={(value) => setData(prev => ({ ...prev, detalhesGamificacao: value }))}
              >
                <SelectTrigger className="bg-accent/5 border-accent/20 focus:ring-accent w-full">
                  <SelectValue placeholder="Selecione um jogo ou mecânica..." />
                </SelectTrigger>
                <SelectContent>
                  {GAMIFICACAO_OPCOES.map((ocpcao) => (
                    <SelectItem key={ocpcao} value={ocpcao}>
                      {ocpcao}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground mt-1">
                Escolha uma das dinâmicas sugeridas para guiar o planejamento da aula.
              </p>
            </div>
          )}
        </div>

        <div>
          <h2 className="text-lg sm:text-xl font-semibold mb-2 select-none">Recursos Didáticos</h2>
          <p className="text-muted-foreground text-xs sm:text-sm mb-4 select-none">
            Tipos de recursos que você pretende usar
          </p>
          <div className="flex flex-wrap gap-2">
            {RECURSOS.map(recurso => (
              <Badge
                key={recurso}
                variant={data.recursos.includes(recurso) ? 'default' : 'outline'}
                className={cn(
                  'cursor-pointer transition-all py-2 px-3 sm:px-4 text-xs sm:text-sm min-h-[44px] flex items-center',
                  data.recursos.includes(recurso) && 'bg-accent text-accent-foreground'
                )}
                onClick={() => toggleRecurso(recurso)}
              >
                {recurso}
              </Badge>
            ))}
          </div>
        </div>

        <div>
          <h2 className="text-lg sm:text-xl font-semibold mb-2 select-none">Materiais Disponíveis</h2>
          <p className="text-muted-foreground text-xs sm:text-sm mb-4 select-none">
            Marque os materiais que você tem acesso na escola
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {MATERIAIS.map(material => (
              <div key={material} className="flex items-center space-x-3">
                <Checkbox
                  id={material}
                  checked={data.materiaisDisponiveis.includes(material)}
                  onCheckedChange={() => toggleMaterial(material)}
                />
                <label
                  htmlFor={material}
                  className="text-xs sm:text-sm font-medium cursor-pointer select-none"
                >
                  {material}
                </label>
              </div>
            ))}
          </div>

          <div className="mt-4">
            <Input
              placeholder="Outros materiais disponíveis..."
              className="text-sm"
              value={data.materiaisCustom}
              onChange={(e) => setData(prev => ({ ...prev, materiaisCustom: e.target.value }))}
            />
          </div>
        </div>

        <div className="flex items-center justify-between rounded-2xl border p-3 sm:p-4 gap-3">
          <div className="flex-1 min-w-0">
            <p className="font-medium text-sm sm:text-base">Permitir materiais extras</p>
            <p className="text-xs sm:text-sm text-muted-foreground">
              A IA pode sugerir materiais além dos selecionados
            </p>
          </div>
          <Switch
            checked={data.permitirExtras}
            onCheckedChange={(checked) => setData(prev => ({ ...prev, permitirExtras: checked }))}
          />
        </div>

        {/* Checkbox para Material Impresso */}
        <div className={cn(
          "rounded-2xl border p-3 sm:p-4 transition-all",
          data.gerarMaterialImpresso ? "border-amber-500/50 bg-amber-500/5" : ""
        )}>
          <div className="flex items-start space-x-3">
            <Checkbox
              id="gerarMaterialImpresso"
              checked={data.gerarMaterialImpresso}
              onCheckedChange={(checked) => handleMaterialImpressoChange(checked as boolean)}
            />
            <div className="flex-1">
              <label
                htmlFor="gerarMaterialImpresso"
                className="text-sm sm:text-base font-medium cursor-pointer flex items-center gap-2 select-none"
              >
                📄 Gerar sugestão de material impresso?
              </label>
              <p className="text-sm text-muted-foreground mt-1">
                A IA criará uma sugestão de atividade que pode ser impressa e entregue aos alunos
              </p>
              {data.gerarMaterialImpresso && (
                <p className="text-xs text-amber-600 mt-2 flex items-center gap-1">
                  <AlertTriangle className="h-3 w-3" />
                  Lembre-se de revisar o material antes de usar
                </p>
              )}
            </div>
          </div>
        </div>

        <div>
          <h2 className="text-lg sm:text-xl font-semibold mb-2 select-none">Observações sobre a Turma</h2>
          <p className="text-muted-foreground text-xs sm:text-sm mb-4 select-none">
            Informações adicionais sobre necessidades especiais, nível da turma, etc.
          </p>
          <Textarea
            placeholder="Ex: Turma com 30 alunos, nível heterogêneo, 2 alunos com TDAH..."
            value={data.observacoes}
            onChange={(e) => setData(prev => ({ ...prev, observacoes: e.target.value }))}
            className="min-h-[80px] sm:min-h-[100px] resize-none text-sm"
          />
        </div>
      </div>

      {/* Modal de Consentimento */}
      <Dialog open={showConsentDialog} onOpenChange={setShowConsentDialog}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-500" />
              Aviso Importante
            </DialogTitle>
            <DialogDescription asChild>
              <div className="space-y-4 text-left">
                <p>
                  O <strong>Material Impresso Sugerido</strong> é gerado por Inteligência Artificial 
                  e pode conter erros, imprecisões ou conteúdo inadequado.
                </p>
                <p>
                  Ao ativar esta opção, você concorda que:
                </p>
                <ul className="list-disc list-inside space-y-1 text-sm">
                  <li>O material é apenas uma <strong>sugestão</strong> e deve ser revisado</li>
                  <li>Você se responsabiliza por revisar, editar e adaptar o conteúdo</li>
                  <li>Você se responsabiliza por qualquer erro presente no material final</li>
                  <li>O material não deve ser usado sem verificação prévia</li>
                </ul>
              </div>
            </DialogDescription>
          </DialogHeader>
          <div className="flex items-center space-x-2 pt-2">
            <Checkbox
              id="rememberConsent"
              checked={rememberConsent}
              onCheckedChange={(checked) => setRememberConsent(checked as boolean)}
            />
            <label htmlFor="rememberConsent" className="text-sm cursor-pointer">
              Memorizar essa decisão (não perguntar novamente)
            </label>
          </div>
          <DialogFooter className="gap-2">
            <Button variant="outline" onClick={handleConsentDecline}>
              Cancelar
            </Button>
            <Button onClick={handleConsentAccept} className="bg-amber-500 hover:bg-amber-600">
              Li e concordo
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
