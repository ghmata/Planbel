import React, { createContext, useContext, useState, useEffect } from 'react';
import { WizardData, initialWizardData } from '@/types/plan';

interface WizardContextType {
  data: WizardData;
  setData: React.Dispatch<React.SetStateAction<WizardData>>;
  currentStep: number;
  setCurrentStep: React.Dispatch<React.SetStateAction<number>>;
  resetWizard: () => void;
}

const WizardContext = createContext<WizardContextType | undefined>(undefined);

const STORAGE_KEY = 'planbel-wizard-data';

export function WizardProvider({ children }: { children: React.ReactNode }) {
  const [data, setData] = useState<WizardData>(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? { ...initialWizardData, ...JSON.parse(saved) } : initialWizardData;
  });
  const [currentStep, setCurrentStep] = useState(1);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  }, [data]);

  const resetWizard = () => {
    setData(initialWizardData);
    setCurrentStep(1);
    localStorage.removeItem(STORAGE_KEY);
  };

  return (
    <WizardContext.Provider value={{ data, setData, currentStep, setCurrentStep, resetWizard }}>
      {children}
    </WizardContext.Provider>
  );
}

export function useWizard() {
  const context = useContext(WizardContext);
  if (!context) {
    throw new Error('useWizard must be used within a WizardProvider');
  }
  return context;
}
