import { jsPDF } from 'jspdf';
import { GeneratedPlan } from './api';

export const generateProfessionalPDF = async (plan: GeneratedPlan) => {
  const doc = new jsPDF();
  
  // --- CARREGAMENTO DE FONTE UTF-8 (Roboto) ---
  // Isso resolve o problema de caracteres ilegíveis/quadrados
  try {
    const fontUrl = 'https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.66/fonts/Roboto/Roboto-Regular.ttf';
    const fontResponse = await fetch(fontUrl);
    const fontBuffer = await fontResponse.arrayBuffer();
    
    // Converter ArrayBuffer para Base64 (sem usar libs externas pesadas)
    const base64Font = btoa(
      new Uint8Array(fontBuffer)
        .reduce((data, byte) => data + String.fromCharCode(byte), '')
    );

    // Adicionar ao VFS do jsPDF
    doc.addFileToVFS('Roboto-Regular.ttf', base64Font);
    doc.addFont('Roboto-Regular.ttf', 'Roboto', 'normal');
    doc.setFont('Roboto'); // Define como padrão global
  } catch (e) {
    console.error("Erro ao carregar fonte, usando fallback (pode ter erros de acentuação):", e);
    // Fallback para Helvetica (padrão) se der erro de rede
    doc.setFont('helvetica'); 
  }

  // Configurações Iniciais
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  const margin = 20;
  const contentWidth = pageWidth - (margin * 2);
  let y = 20;

  // Função auxiliar para verificar quebras de página
  const checkPageBreak = (heightNeeded: number) => {
    if (y + heightNeeded > pageHeight - margin) {
      doc.addPage();
      y = 20;
      // Reaplicar fonte na nova página
      try { doc.setFont('Roboto'); } catch {}
    }
  };

  // Função auxiliar para adicionar texto com quebra de linha inteligente
  const addWrappedText = (text: string, fontSize: number = 11, fontStyle: string = 'normal', color: string = '#333333') => {
    if (fontStyle === 'bold') {
       doc.setFont('Roboto', 'normal'); 
    } else {
       doc.setFont('Roboto', 'normal');
    }
    
    doc.setFontSize(fontSize);
    doc.setTextColor(color);

    const safeText = text || ''; 
    const lines = doc.splitTextToSize(safeText, contentWidth);
    
    // Altura da linha em pontos (aproximação segura para espaçamento 1.5)
    // fontSize * 0.5 (como estava antes) era muito apertado/estranho para jsPDF units. 
    // Geralmente jsPDF usa mm ou pt. Se unit for mm (padrão do jsPDF() construtor sem args),
    // fontSize 11 é ~3.88mm. 
    // Vamos usar um fator multiplicativo mais seguro.
    const lineHeight = fontSize * 0.45; 

    // Renderizar linha a linha para permitir quebra de página no meio do parágrafo
    lines.forEach((line: string) => {
      // Verifica se a linha cabe na página atual
      if (y + lineHeight > pageHeight - margin) {
        doc.addPage();
        y = margin; // Reinicia no topo (margem)
        
        // Reaplicar configurações de fonte na nova página
        try { 
          doc.setFont('Roboto', 'normal'); 
          doc.setFontSize(fontSize);
          doc.setTextColor(color);
        } catch {}
      }
      
      doc.text(line, margin, y);
      y += lineHeight;
    });

    // Adiciona um pequeno espaçamento após o bloco de texto
    y += 3;
  };

  // Função para adicionar títulos de seção
  const addSectionTitle = (title: string) => {
    checkPageBreak(15);
    y += 5;
    doc.setFontSize(14);
    doc.setTextColor('#2563eb'); 
    doc.text((title || '').toUpperCase(), margin, y);
    doc.setDrawColor(37, 99, 235);
    doc.setLineWidth(0.5);
    doc.line(margin, y + 2, margin + 40, y + 2);
    y += 10;
  };

  // ==================== CONTEÚDO DO PDF ====================

  // CABEÇALHO
  doc.setFontSize(22);
  doc.setTextColor('#1e3a8a');
  
  const titleLines = doc.splitTextToSize(plan.titulo || 'Sem Título', contentWidth);
  doc.text(titleLines, margin, y);
  y += (titleLines.length * 10) + 5;

  // Metadados
  const metaText = `Disciplina: ${(plan.disciplinas || []).join(', ')}  |  Série: ${plan.serie || ''}  |  Duração: ${plan.duracao || ''} min`;
  doc.setFontSize(10);
  doc.setTextColor('#64748b');
  doc.text(metaText, margin, y);
  y += 15;

  doc.setDrawColor(200, 200, 200);
  doc.setLineWidth(0.5);
  doc.line(margin, y, pageWidth - margin, y);
  y += 15;

  // 1. SEÇÕES
  addSectionTitle('Introdução');
  addWrappedText(plan.introducao);

  addSectionTitle('Desenvolvimento');
  addWrappedText(plan.desenvolvimento);

  addSectionTitle('Fechamento');
  addWrappedText(plan.fechamento);

  addSectionTitle('Cronograma');
  (plan.cronograma || []).forEach(item => {
    checkPageBreak(10);
    doc.setFontSize(11);
    doc.setTextColor('#333333');
    // Usamos traço simples para garantir
    doc.text(`- ${item.etapa || ''} (${item.tempo || ''})`, margin + 2, y);
    y += 6;
    
    doc.setFontSize(10);
    doc.setTextColor('#555555');
    const descLines = doc.splitTextToSize(item.descricao || '', contentWidth - 5);
    doc.text(descLines, margin + 5, y);
    y += (descLines.length * 5) + 6;
  });

  if (plan.materiaisNecessarios?.length > 0) {
    addSectionTitle('Materiais Necessários');
    doc.setFontSize(11);
    doc.setTextColor('#333333');
    const matText = plan.materiaisNecessarios.join('\n- ');
    addWrappedText('- ' + matText);
  }

  if (plan.competenciasBNCC?.length > 0) {
    addSectionTitle('Competências BNCC');
    doc.setFontSize(10);
    doc.setTextColor('#059669'); 
    const bnccText = plan.competenciasBNCC.join('\n');
    addWrappedText(bnccText, 10, 'normal', '#059669');
  }

  // RODAPÉ
  const pageCount = doc.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFontSize(8);
    doc.setTextColor('#94a3b8');
    doc.text(
      `Gerado por PlanBel 2.0 - Página ${i} de ${pageCount}`,
      pageWidth / 2,
      pageHeight - 10,
      { align: 'center' }
    );
  }

  // Nome do Arquivo Seguro
  const safeFilename = (plan.titulo || 'plano')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, "") 
    .replace(/[^a-zA-Z0-9 ]/g, "")   
    .replace(/\s+/g, "_")            
    .substring(0, 40);

  doc.save(`PlanBel_${safeFilename}.pdf`);
};
