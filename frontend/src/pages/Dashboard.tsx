import { PlusCircle, FileText, CheckCircle, Clock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { StatsCard } from '@/components/dashboard/StatsCard';
import { PlanCard } from '@/components/dashboard/PlanCard';
import { usePlans } from '@/contexts/PlansContext';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const { plans } = usePlans();
  const navigate = useNavigate();
  const recentPlans = plans.slice(0, 4);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-foreground">
          Bem-vindo ao <span className="text-primary">PLANBEL</span>
        </h1>
        <p className="text-muted-foreground mt-2">
          Crie planos de aula profissionais e alinhados à BNCC em minutos
        </p>
      </header>

      <Button
        size="lg"
        className="w-full h-auto py-6 rounded-2xl shadow-md hover:shadow-lg transition-all mb-8"
        onClick={() => navigate('/novo')}
      >
        <PlusCircle className="h-6 w-6 mr-3" />
        <div className="text-left">
          <p className="font-semibold text-lg">Criar Novo Plano de Aula</p>
          <p className="text-primary-foreground/80 text-sm font-normal">
            Comece agora com o assistente inteligente
          </p>
        </div>
      </Button>

      <div className="grid grid-cols-3 gap-4 mb-8">
        <StatsCard
          title="Total de Planos"
          value={plans.length}
          icon={FileText}
        />
        <StatsCard
          title="Alinhamento"
          value="100% BNCC"
          icon={CheckCircle}
          variant="accent"
        />
        <StatsCard
          title="Tempo Médio"
          value="5 min"
          icon={Clock}
        />
      </div>

      {recentPlans.length > 0 && (
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Planos Recentes</h2>
            <Button variant="ghost" onClick={() => navigate('/historico')}>
              Ver todos
            </Button>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {recentPlans.map(plan => (
              <PlanCard key={plan.id} plan={plan} />
            ))}
          </div>
        </section>
      )}

      {recentPlans.length === 0 && (
        <div className="text-center py-12 rounded-2xl border-2 border-dashed">
          <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="font-semibold text-lg">Nenhum plano criado ainda</h3>
          <p className="text-muted-foreground mt-1">
            Crie seu primeiro plano de aula e veja a mágica acontecer!
          </p>
        </div>
      )}
    </div>
  );
}
