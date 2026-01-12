import { useState } from 'react';
import { Search, FileText } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { PlanCard } from '@/components/dashboard/PlanCard';
import { usePlans } from '@/contexts/PlansContext';

export default function Historico() {
  const { plans, deletePlan } = usePlans();
  const [search, setSearch] = useState('');

  const filteredPlans = plans.filter(plan =>
    plan.titulo.toLowerCase().includes(search.toLowerCase()) ||
    plan.disciplinas.some(d => d.toLowerCase().includes(search.toLowerCase())) ||
    plan.serie.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 max-w-4xl mx-auto pb-24 md:pb-6">
      <header className="mb-6">
        <h1 className="text-2xl font-bold text-foreground">Histórico de Planos</h1>
        <p className="text-muted-foreground mt-1">
          {plans.length} {plans.length === 1 ? 'plano criado' : 'planos criados'}
        </p>
      </header>

      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
        <Input
          placeholder="Buscar por título, disciplina ou série..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="pl-10"
        />
      </div>

      {filteredPlans.length > 0 ? (
        <div className="grid gap-4 sm:grid-cols-2">
          {filteredPlans.map(plan => (
            <PlanCard
              key={plan.id}
              plan={plan}
              onDelete={() => deletePlan(plan.id)}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 rounded-2xl border-2 border-dashed">
          <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="font-semibold text-lg">
            {search ? 'Nenhum plano encontrado' : 'Nenhum plano criado ainda'}
          </h3>
          <p className="text-muted-foreground mt-1">
            {search
              ? 'Tente buscar por outros termos'
              : 'Seus planos criados aparecerão aqui'}
          </p>
        </div>
      )}
    </div>
  );
}
