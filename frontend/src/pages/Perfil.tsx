import { Moon, Sun, Bell, BellOff, FileText, Award, Clock } from 'lucide-react';
import { Switch } from '@/components/ui/switch';
import { useTheme } from '@/contexts/ThemeContext';
import { usePlans } from '@/contexts/PlansContext';
import { useState } from 'react';

export default function Perfil() {
  const { theme, toggleTheme } = useTheme();
  const { plans } = usePlans();
  const [notifications, setNotifications] = useState(true);

  const stats = [
    { label: 'Planos Criados', value: plans.length, icon: FileText },
    { label: 'Disciplinas', value: new Set(plans.flatMap(p => p.disciplinas)).size, icon: Award },
    { label: 'Horas Planejadas', value: Math.round(plans.reduce((acc, p) => acc + Number(p.duracao), 0) / 60), icon: Clock },
  ];

  return (
    <div className="p-6 max-w-2xl mx-auto pb-24 md:pb-6">
      <header className="mb-8 text-center">
        <div className="h-20 w-20 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-2xl font-bold mx-auto mb-4">
          PR
        </div>
        <h1 className="text-2xl font-bold text-foreground">Professor</h1>
        <p className="text-muted-foreground">professor@escola.edu.br</p>
      </header>

      <div className="grid grid-cols-3 gap-4 mb-8">
        {stats.map(({ label, value, icon: Icon }) => (
          <div key={label} className="rounded-2xl bg-card p-4 text-center">
            <Icon className="h-6 w-6 text-primary mx-auto mb-2" />
            <p className="text-2xl font-bold">{value}</p>
            <p className="text-xs text-muted-foreground">{label}</p>
          </div>
        ))}
      </div>

      <div className="space-y-4">
        <div className="rounded-2xl border bg-card p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            {theme === 'dark' ? (
              <Moon className="h-5 w-5 text-primary" />
            ) : (
              <Sun className="h-5 w-5 text-primary" />
            )}
            <div>
              <p className="font-medium">Modo Escuro</p>
              <p className="text-sm text-muted-foreground">
                {theme === 'dark' ? 'Ativado' : 'Desativado'}
              </p>
            </div>
          </div>
          <Switch
            checked={theme === 'dark'}
            onCheckedChange={toggleTheme}
          />
        </div>

        <div className="rounded-2xl border bg-card p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            {notifications ? (
              <Bell className="h-5 w-5 text-primary" />
            ) : (
              <BellOff className="h-5 w-5 text-muted-foreground" />
            )}
            <div>
              <p className="font-medium">Notificações</p>
              <p className="text-sm text-muted-foreground">
                {notifications ? 'Ativadas' : 'Desativadas'}
              </p>
            </div>
          </div>
          <Switch
            checked={notifications}
            onCheckedChange={setNotifications}
          />
        </div>
      </div>

      <div className="mt-8 rounded-2xl bg-accent/20 p-6 text-center">
        <p className="text-sm text-muted-foreground">
          PLANBEL 2.0 - Gerador de Planos de Aula
        </p>
        <p className="text-xs text-muted-foreground mt-1">
          Planos alinhados à BNCC em minutos
        </p>
      </div>
    </div>
  );
}
