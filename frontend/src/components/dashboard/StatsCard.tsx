import { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  variant?: 'default' | 'accent';
}

export function StatsCard({ title, value, icon: Icon, variant = 'default' }: StatsCardProps) {
  return (
    <div className={cn(
      "rounded-2xl p-5 shadow-sm transition-all hover:shadow-md",
      variant === 'accent' 
        ? "bg-accent text-accent-foreground" 
        : "bg-card text-card-foreground"
    )}>
      <div className="flex items-center justify-between">
        <div>
          <p className={cn(
            "text-sm",
            variant === 'accent' ? "text-accent-foreground/80" : "text-muted-foreground"
          )}>{title}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
        </div>
        <div className={cn(
          "h-12 w-12 rounded-xl flex items-center justify-center",
          variant === 'accent' 
            ? "bg-accent-foreground/10" 
            : "bg-primary/10"
        )}>
          <Icon className={cn(
            "h-6 w-6",
            variant === 'accent' ? "text-accent-foreground" : "text-primary"
          )} />
        </div>
      </div>
    </div>
  );
}
