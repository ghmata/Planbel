import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Copy, Share2, FileDown, Clock, BookOpen, ChevronDown, Printer, Loader2, Gamepad2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { usePlans } from '@/contexts/PlansContext';
import { toast } from '@/hooks/use-toast';
import { useState } from 'react';
import { cn } from '@/lib/utils';
import { generatePrintableMaterial, generateGame, openHtmlForPrint } from '@/services/api';
import { generateProfessionalPDF } from '@/services/pdfGenerator';

export default function Resultado() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { getPlan } = usePlans();
  const plan = getPlan(id || '');
  const [openSections, setOpenSections] = useState<string[]>(['introducao', 'desenvolvimento', 'fechamento']);
  const [isGeneratingMaterial, setIsGeneratingMaterial] = useState(false);
  const [isGeneratingGame, setIsGeneratingGame] = useState(false);

  const handleGenerateMaterial = async () => {
    if (!plan) return;
    
    setIsGeneratingMaterial(true);
    try {
      const result = await generatePrintableMaterial(plan as any);
      if (result.html) {
        openHtmlForPrint(result.html, result.titulo || 'Material Impresso');
        toast({
          title: 'Material gerado!',
          description: 'Uma nova aba foi aberta. Use Ctrl+P para imprimir ou salvar como PDF.',
        });
      }
    } catch (error) {
      toast({
        title: 'Erro ao gerar material',
        description: error instanceof Error ? error.message : 'Tente novamente',
        variant: 'destructive',
      });
    } finally {
      setIsGeneratingMaterial(false);
    }
  };

  const handleGenerateGame = async () => {
    if (!plan) return;
    
    setIsGeneratingGame(true);
    try {
      const result = await generateGame(plan as any);
      if (result.html) {
        openHtmlForPrint(result.html, result.titulo || 'Jogo Educativo');
        toast({
          title: 'Jogo gerado!',
          description: 'Uma nova aba foi aberta. Recorte e monte seu jogo!',
        });
      }
    } catch (error) {
      toast({
        title: 'Erro ao gerar jogo',
        description: error instanceof Error ? error.message : 'Tente novamente',
        variant: 'destructive',
      });
    } finally {
      setIsGeneratingGame(false);
    }
  };

  if (!plan) {
    return (
      <div className="p-6 text-center">
        <p>Plano não encontrado</p>
        <Button onClick={() => navigate('/')} className="mt-4">
          Voltar ao início
        </Button>
      </div>
    );
  }

  const toggleSection = (section: string) => {
    setOpenSections(prev =>
      prev.includes(section)
        ? prev.filter(s => s !== section)
        : [...prev, section]
    );
  };

  const copyToClipboard = () => {
    const text = `
${plan.titulo}

INTRODUÇÃO
${plan.introducao}

DESENVOLVIMENTO
${plan.desenvolvimento}

FECHAMENTO
${plan.fechamento}

CRONOGRAMA
${plan.cronograma.map(c => `• ${c.etapa} (${c.tempo}): ${c.descricao}`).join('\n')}

COMPETÊNCIAS BNCC
${plan.competenciasBNCC.join(', ')}

MATERIAIS
${plan.materiaisNecessarios.join(', ')}
    `.trim();

    navigator.clipboard.writeText(text);
    toast({ title: 'Copiado!', description: 'Plano copiado para a área de transferência.' });
  };

  const sharePlan = async () => {
    if (navigator.share) {
      await navigator.share({
        title: plan.titulo,
        text: `Confira este plano de aula: ${plan.titulo}`,
      });
    } else {
      copyToClipboard();
    }
  };

  const exportPDF = async () => {
    toast({ title: 'Gerando PDF...', description: 'Baixando fontes e preparando arquivo...' });
    try {
      await generateProfessionalPDF(plan as any);
      toast({ title: 'PDF baixado!', description: 'Arquivo salvo com sucesso.' });
    } catch (error) {
      console.error(error);
      toast({ 
        title: 'Erro ao gerar PDF', 
        description: 'Não foi possível gerar o arquivo.', 
        variant: 'destructive' 
      });
    }
  };

  const sections = [
    { id: 'introducao', title: 'Introdução', content: plan.introducao },
    { id: 'desenvolvimento', title: 'Desenvolvimento', content: plan.desenvolvimento },
    { id: 'fechamento', title: 'Fechamento', content: plan.fechamento },
  ];

  return (
    <div className="p-6 max-w-3xl mx-auto pb-24 md:pb-6">
      <Button
        variant="ghost"
        className="mb-4"
        onClick={() => navigate('/')}
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Voltar
      </Button>

      <div id="plan-content">
        <header className="mb-6">
          <h1 className="text-2xl font-bold text-foreground mb-3">
            {plan.titulo}
          </h1>
          <div className="flex flex-wrap gap-2">
            <Badge variant="secondary">
              <BookOpen className="h-3 w-3 mr-1" />
              {plan.serie}
            </Badge>
            <Badge variant="outline">
              <Clock className="h-3 w-3 mr-1" />
              {plan.duracao} min
            </Badge>
            {plan.disciplinas.map(d => (
              <Badge key={d} variant="outline">{d}</Badge>
            ))}
          </div>
        </header>

        <div className="flex flex-wrap gap-2 mb-6">
          <Button variant="outline" size="sm" onClick={copyToClipboard}>
            <Copy className="h-4 w-4 mr-2" />
            Copiar
          </Button>
          <Button variant="outline" size="sm" onClick={sharePlan}>
            <Share2 className="h-4 w-4 mr-2" />
            Compartilhar
          </Button>
          <Button variant="outline" size="sm" onClick={exportPDF}>
            <FileDown className="h-4 w-4 mr-2" />
            Exportar PDF
          </Button>

          {(plan.detalhesGamificacao || plan.metodologia?.toLowerCase().includes('gamifica')) && (
            <Button 
              onClick={handleGenerateGame}
              disabled={isGeneratingGame}
              className="bg-purple-600 hover:bg-purple-700 text-white disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              size="sm"
            >
              {isGeneratingGame ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Gamepad2 className="h-4 w-4 mr-2" />
              )}
              {isGeneratingGame ? 'Gerando Jogo...' : 'Imprimir Jogo'}
            </Button>
          )}

          {plan.gerarMaterialImpresso && (
            <Button 
              variant="outline" 
              size="sm" 
              onClick={handleGenerateMaterial}
              disabled={isGeneratingMaterial}
              className="border-amber-500 text-amber-600 hover:bg-amber-50"
            >
              {isGeneratingMaterial ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Printer className="h-4 w-4 mr-2" />
              )}
              {isGeneratingMaterial ? 'Gerando...' : 'Gerar Material Impresso'}
            </Button>
          )}
        </div>

        <div className="space-y-4">
          {sections.map(section => (
            <Collapsible
              key={section.id}
              open={openSections.includes(section.id)}
              onOpenChange={() => toggleSection(section.id)}
            >
              <div className="rounded-2xl border bg-card overflow-hidden">
                <CollapsibleTrigger className="w-full flex items-center justify-between p-4 hover:bg-muted/50 transition-colors">
                  <h2 className="font-semibold">{section.title}</h2>
                  <ChevronDown className={cn(
                    'h-5 w-5 text-muted-foreground transition-transform',
                    openSections.includes(section.id) && 'rotate-180'
                  )} />
                </CollapsibleTrigger>
                <CollapsibleContent>
                  <div className="px-4 pb-4 text-muted-foreground leading-relaxed whitespace-pre-wrap">
                    {section.content}
                  </div>
                </CollapsibleContent>
              </div>
            </Collapsible>
          ))}
        </div>

        <div className="rounded-2xl border bg-card p-4 mt-4">
          <h2 className="font-semibold mb-4">Cronograma</h2>
          {/* Visualização Mobile (Cards) */}
          <div className="space-y-3 md:hidden">
            {plan.cronograma.map((item, index) => (
              <div key={index} className="bg-muted/30 p-3 rounded-lg border">
                <div className="flex justify-between items-start mb-2 pb-2 border-b border-border/50">
                  <span className="font-semibold text-sm text-foreground pr-2">{item.etapa}</span>
                  <Badge variant="secondary" className="text-xs whitespace-nowrap shrink-0 h-6">
                    {item.tempo}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
                  {item.descricao}
                </p>
              </div>
            ))}
          </div>

          {/* Visualização Desktop (Tabela) */}
          <div className="hidden md:block overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2 font-medium">Etapa</th>
                  <th className="text-left py-2 font-medium">Tempo</th>
                  <th className="text-left py-2 font-medium">Descrição</th>
                </tr>
              </thead>
              <tbody>
                {plan.cronograma.map((item, index) => (
                  <tr key={index} className="border-b last:border-0 hover:bg-muted/30 transition-colors">
                    <td className="py-3 font-medium w-[25%]">{item.etapa}</td>
                    <td className="py-3 text-muted-foreground w-[15%]">{item.tempo}</td>
                    <td className="py-3 text-muted-foreground whitespace-pre-wrap">{item.descricao}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="rounded-2xl border bg-card p-4 mt-4">
          <h2 className="font-semibold mb-3">Competências BNCC</h2>
          <div className="flex flex-wrap gap-2">
            {plan.competenciasBNCC.map(comp => (
              <Badge key={comp} variant="secondary">{comp}</Badge>
            ))}
          </div>
        </div>

        {plan.materiaisNecessarios.length > 0 && (
          <div className="rounded-2xl border bg-card p-4 mt-4">
            <h2 className="font-semibold mb-3">Materiais Necessários</h2>
            <ul className="list-disc list-inside text-muted-foreground space-y-1">
              {plan.materiaisNecessarios.map((material, index) => (
                <li key={index}>{material}</li>
              ))}
            </ul>
          </div>
        )}

        {plan.materialImpresso && (
          <div className="rounded-2xl border border-amber-500/50 bg-amber-500/5 p-4 mt-4">
            <div className="flex items-center gap-2 mb-3">
              <h2 className="font-semibold">📄 Sugestão de Material Impresso</h2>
              <Badge variant="outline" className="text-amber-600 border-amber-500">
                Revisar antes de usar
              </Badge>
            </div>
            <div className="text-muted-foreground leading-relaxed whitespace-pre-wrap">
              {plan.materialImpresso}
            </div>
            <p className="mt-4 text-sm text-amber-600 bg-amber-500/10 p-2 rounded">
              ⚠️ <strong>Atenção:</strong> Este material foi gerado por IA e pode conter erros. 
              Por favor, revise, edite e adapte conforme necessário antes de imprimir e entregar aos alunos.
            </p>
          </div>
        )}
      </div>
      <div className="mt-8 text-xs text-muted-foreground text-center opacity-50">
        ID do Plano: {plan.id}
      </div>
    </div>
  );
}
