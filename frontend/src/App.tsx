import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "@/contexts/ThemeContext";
import { WizardProvider } from "@/contexts/WizardContext";
import { PlansProvider } from "@/contexts/PlansContext";
import { Layout } from "@/components/layout/Layout";
import Dashboard from "@/pages/Dashboard";
import NovoPlano from "@/pages/NovoPlano";
import Resultado from "@/pages/Resultado";
import Historico from "@/pages/Historico";
import Perfil from "@/pages/Perfil";
import NotFound from "@/pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <ThemeProvider>
      <PlansProvider>
        <WizardProvider>
          <TooltipProvider>
            <Toaster />
            <Sonner />
            <BrowserRouter>
              <Routes>
                <Route element={<Layout />}>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/novo" element={<NovoPlano />} />
                  <Route path="/resultado/:id" element={<Resultado />} />
                  <Route path="/historico" element={<Historico />} />
                  <Route path="/perfil" element={<Perfil />} />
                </Route>
                <Route path="*" element={<NotFound />} />
              </Routes>
            </BrowserRouter>
          </TooltipProvider>
        </WizardProvider>
      </PlansProvider>
    </ThemeProvider>
  </QueryClientProvider>
);

export default App;
