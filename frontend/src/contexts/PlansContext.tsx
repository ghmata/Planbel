import React, { createContext, useContext, useState, useEffect } from 'react';
import { PlanoGerado } from '@/types/plan';

interface PlansContextType {
  plans: PlanoGerado[];
  addPlan: (plan: PlanoGerado) => void;
  deletePlan: (id: string) => void;
  getPlan: (id: string) => PlanoGerado | undefined;
}

const PlansContext = createContext<PlansContextType | undefined>(undefined);

const STORAGE_KEY = 'planbel-plans';

export function PlansProvider({ children }: { children: React.ReactNode }) {
  const [plans, setPlans] = useState<PlanoGerado[]>(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      return parsed.map((p: PlanoGerado) => ({
        ...p,
        createdAt: new Date(p.createdAt),
      }));
    }
    return [];
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(plans));
  }, [plans]);

  const addPlan = (plan: PlanoGerado) => {
    setPlans(prev => [plan, ...prev]);
  };

  const deletePlan = (id: string) => {
    setPlans(prev => prev.filter(p => p.id !== id));
  };

  const getPlan = (id: string) => {
    return plans.find(p => p.id === id);
  };

  return (
    <PlansContext.Provider value={{ plans, addPlan, deletePlan, getPlan }}>
      {children}
    </PlansContext.Provider>
  );
}

export function usePlans() {
  const context = useContext(PlansContext);
  if (!context) {
    throw new Error('usePlans must be used within a PlansProvider');
  }
  return context;
}
