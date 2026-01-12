import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Sparkles, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ProgressBar } from '@/components/wizard/ProgressBar';
import { Step1Contexto } from '@/components/wizard/Step1Contexto';
import { Step2Pedagogia } from '@/components/wizard/Step2Pedagogia';
import { Step3Refinamento } from '@/components/wizard/Step3Refinamento';
import { useWizard } from '@/contexts/WizardContext';
import { usePlans } from '@/contexts/PlansContext';
import { PlanoGerado } from '@/types/plan';
import { toast } from '@/hooks/use-toast';
import { generatePlan as apiGeneratePlan } from '@/services/api';

const STEPS = ['Contexto', 'Pedagogia', 'Refinamento'];

export default function NovoPlano() {
  const navigate = useNavigate();
  const { data, currentStep, setCurrentStep, resetWizard } = useWizard();
  const { addPlan } = usePlans();
  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [statusMessage, setStatusMessage] = useState('');

  // Scroll to top whenever step changes
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [currentStep]);

  const canProceed = () => {
    if (currentStep === 1) {
      return data.disciplinas.length > 0 && data.serie !== '';
    }
    if (currentStep === 2) {
      return data.objetivos.trim() !== '';
    }
    return true;
  };

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    } else {
      navigate('/');
    }
  };

  const generatePlan = async () => {
    setIsGenerating(true);
    setProgress(0);

    const progressSteps = [
      { p: 15, msg: 'Analisando objetivos de aprendizagem...' },
      { p: 35, msg: 'Consultando Base Nacional Comum Curricular...' },
      { p: 55, msg: 'Estruturando atividades pedagógicas...' },
      { p: 75, msg: 'Elaborando cronograma detalhado...' },
      { p: 90, msg: 'Finalizando plano de aula...' },
    ];

    // Start progress animation
    let currentStepIndex = 0;
    const progressInterval = setInterval(() => {
      if (currentStepIndex < progressSteps.length) {
        setProgress(progressSteps[currentStepIndex].p);
        setStatusMessage(progressSteps[currentStepIndex].msg);
        currentStepIndex++;
      }
    }, 1500);

    try {
      const responseData = await apiGeneratePlan(data);

      clearInterval(progressInterval);

      setProgress(100);
      setStatusMessage('Plano gerado com sucesso!');

      const plano: PlanoGerado = {
        ...responseData,
        createdAt: new Date(responseData.createdAt),
      };

      addPlan(plano);
      resetWizard();
      
      toast({
        title: "Plano gerado com sucesso!",
        description: "Seu plano de aula está pronto e foi criado pela IA.",
      });

      navigate(`/resultado/${plano.id}`);
    } catch (error) {
      clearInterval(progressInterval);
      console.error('Error generating plan:', error);
      
      toast({
        title: "Erro ao gerar plano",
        description: error instanceof Error ? error.message : "Tente novamente em alguns instantes.",
        variant: "destructive",
      });
      
      setIsGenerating(false);
      setProgress(0);
      setStatusMessage('');
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="sticky top-0 z-10 bg-background/95 backdrop-blur border-b px-6 py-4">
        <div className="max-w-2xl mx-auto">
          <ProgressBar currentStep={currentStep} steps={STEPS} />
        </div>
      </header>

      <main className="flex-1 p-6 max-w-2xl mx-auto w-full">
        {currentStep === 1 && <Step1Contexto />}
        {currentStep === 2 && <Step2Pedagogia />}
        {currentStep === 3 && <Step3Refinamento />}
      </main>

      <footer className="sticky bottom-0 bg-background/95 backdrop-blur border-t px-6 py-4 mb-16 md:mb-0">
        <div className="max-w-2xl mx-auto flex gap-3">
          <Button
            variant="outline"
            className="flex-1"
            onClick={handleBack}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            {currentStep === 1 ? 'Cancelar' : 'Voltar'}
          </Button>

          {currentStep < 3 ? (
            <Button
              className="flex-1"
              onClick={handleNext}
              disabled={!canProceed()}
            >
              Próximo
              <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          ) : (
            <Button
              className="flex-1"
              onClick={generatePlan}
              disabled={isGenerating || !canProceed()}
            >
            {isGenerating ? (
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm">{statusMessage || `Gerando... ${progress}%`}</span>
                </div>
              ) : (
                <>
                  <Sparkles className="h-4 w-4 mr-2" />
                  Gerar Plano de Aula
                </>
              )}
            </Button>
          )}
        </div>
      </footer>
    </div>
  );
}
