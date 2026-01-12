import { Clock, BookOpen, Trash2 } from 'lucide-react';
import { PlanoGerado } from '@/types/plan';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useNavigate } from 'react-router-dom';

interface PlanCardProps {
  plan: PlanoGerado;
  onDelete?: () => void;
}

export function PlanCard({ plan, onDelete }: PlanCardProps) {
  const navigate = useNavigate();
  
  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: 'short',
    }).format(date);
  };

  return (
    <div 
      className="group rounded-2xl bg-card p-5 shadow-sm transition-all hover:shadow-md cursor-pointer border border-transparent hover:border-primary/20"
      onClick={() => navigate(`/resultado/${plan.id}`)}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-card-foreground truncate">{plan.titulo}</h3>
          <p className="text-sm text-muted-foreground mt-1 truncate">
            {plan.disciplinas.join(', ')}
          </p>
        </div>
        {onDelete && (
          <Button
            variant="ghost"
            size="icon"
            className="opacity-0 group-hover:opacity-100 transition-opacity h-8 w-8 text-muted-foreground hover:text-destructive"
            onClick={(e) => {
              e.stopPropagation();
              onDelete();
            }}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        )}
      </div>
      
      <div className="flex items-center gap-2 mt-4 flex-wrap">
        <Badge variant="secondary" className="text-xs">
          <BookOpen className="h-3 w-3 mr-1" />
          {plan.serie}
        </Badge>
        <Badge variant="outline" className="text-xs">
          <Clock className="h-3 w-3 mr-1" />
          {plan.duracao}min
        </Badge>
      </div>
      
      <div className="flex items-center justify-between mt-4 pt-3 border-t">
        <span className="text-xs text-muted-foreground">
          {formatDate(plan.createdAt)}
        </span>
        <Badge 
          variant={plan.status === 'gerado' ? 'default' : 'secondary'}
          className="text-xs"
        >
          {plan.status === 'gerado' ? 'Concluído' : 'Rascunho'}
        </Badge>
      </div>
    </div>
  );
}
