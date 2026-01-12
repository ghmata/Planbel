#!/usr/bin/env python3
"""
Script para extrair habilidades da BNCC do PDF
Usa PyMuPDF (fitz) para ler o PDF
"""

import fitz  # PyMuPDF
import re
import json
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extrai todo o texto do PDF."""
    doc = fitz.open(pdf_path)
    full_text = ""
    
    for page_num, page in enumerate(doc):
        text = page.get_text()
        full_text += f"\n--- PÁGINA {page_num + 1} ---\n{text}"
    
    doc.close()
    return full_text


def extract_habilidades(text: str) -> list[dict]:
    """
    Extrai habilidades da BNCC do texto.
    
    Formato típico:
    (EF01MA01) Utilizar números naturais como indicador de quantidade...
    (EF07LP12) Identificar narrador e ponto de vista narrativo...
    (EM13CNT201) Analisar e representar fenômenos celulares...
    """
    # Regex para capturar códigos de habilidade BNCC
    # Padrões: EF01MA01, EF07LP12, EM13CNT201, etc.
    pattern = r'\(?(EF\d{2}[A-Z]{2}\d{2}|EM\d{2}[A-Z]{2,3}\d{2,3})\)?[:\s]+([^\n(]+(?:\n(?!\(E[FM]\d)[^\n(]+)*)'
    
    matches = re.findall(pattern, text, re.MULTILINE)
    
    habilidades = []
    for codigo, descricao in matches:
        # Limpar descrição
        descricao = descricao.strip()
        descricao = re.sub(r'\s+', ' ', descricao)  # Normalizar espaços
        descricao = descricao[:500]  # Limitar tamanho
        
        # Extrair metadados do código
        info = parse_codigo_bncc(codigo)
        
        if info and len(descricao) > 10:  # Filtrar ruído
            habilidades.append({
                "codigo": codigo,
                "descricao": descricao,
                **info
            })
    
    return habilidades


def parse_codigo_bncc(codigo: str) -> dict | None:
    """
    Extrai informações do código da habilidade.
    
    Estrutura do código:
    EF = Ensino Fundamental, EM = Ensino Médio
    01-09 = Ano escolar
    MA = Matemática, LP = Língua Portuguesa, CI = Ciências, etc.
    01-99 = Número da habilidade
    """
    # Ensino Fundamental
    ef_match = re.match(r'EF(\d{2})([A-Z]{2})(\d{2})', codigo)
    if ef_match:
        ano = int(ef_match.group(1))
        componente_sigla = ef_match.group(2)
        
        componentes = {
            "LP": "Língua Portuguesa",
            "MA": "Matemática",
            "CI": "Ciências",
            "GE": "Geografia",
            "HI": "História",
            "AR": "Arte",
            "EF": "Educação Física",
            "ER": "Ensino Religioso",
            "LI": "Língua Inglesa"
        }
        
        if ano <= 5:
            segmento = "Anos Iniciais"
        else:
            segmento = "Anos Finais"
        
        return {
            "nivel": "Ensino Fundamental",
            "segmento": segmento,
            "ano": f"{ano}º ano",
            "componente": componentes.get(componente_sigla, componente_sigla)
        }
    
    # Ensino Médio
    em_match = re.match(r'EM(\d{2})([A-Z]{2,3})(\d{2,3})', codigo)
    if em_match:
        area_sigla = em_match.group(2)
        
        areas = {
            "LGG": "Linguagens e suas Tecnologias",
            "MAT": "Matemática e suas Tecnologias",
            "CNT": "Ciências da Natureza e suas Tecnologias",
            "CHS": "Ciências Humanas e Sociais Aplicadas"
        }
        
        return {
            "nivel": "Ensino Médio",
            "segmento": "Ensino Médio",
            "ano": "1º-3º ano",
            "componente": areas.get(area_sigla, area_sigla)
        }
    
    return None


def organize_habilidades(habilidades: list[dict]) -> dict:
    """Organiza habilidades em estrutura hierárquica."""
    organized = {}
    
    for hab in habilidades:
        componente = hab.get("componente", "Outros")
        segmento = hab.get("segmento", "Geral")
        ano = hab.get("ano", "Geral")
        
        if componente not in organized:
            organized[componente] = {}
        
        if segmento not in organized[componente]:
            organized[componente][segmento] = {}
        
        if ano not in organized[componente][segmento]:
            organized[componente][segmento][ano] = {}
        
        organized[componente][segmento][ano][hab["codigo"]] = hab["descricao"]
    
    return organized


def main():
    """Executa extração e salva resultados."""
    pdf_path = Path(__file__).parent / "BNCC.pdf"
    
    if not pdf_path.exists():
        print(f"❌ Arquivo não encontrado: {pdf_path}")
        return
    
    print(f"📖 Lendo PDF: {pdf_path}")
    text = extract_text_from_pdf(str(pdf_path))
    
    print(f"📝 Texto extraído: {len(text)} caracteres")
    
    # Salvar texto bruto para análise
    text_path = Path(__file__).parent / "bncc_raw_text.txt"
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"💾 Texto salvo em: {text_path}")
    
    print("🔍 Extraindo habilidades...")
    habilidades = extract_habilidades(text)
    print(f"✅ Habilidades encontradas: {len(habilidades)}")
    
    # Organizar
    organized = organize_habilidades(habilidades)
    
    # Salvar JSON
    json_path = Path(__file__).parent / "bncc_habilidades.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(organized, f, ensure_ascii=False, indent=2)
    print(f"💾 JSON salvo em: {json_path}")
    
    # Mostrar estatísticas
    print("\n📊 Estatísticas por componente:")
    for componente, data in organized.items():
        total = sum(
            len(anos) 
            for segmento in data.values() 
            for anos in segmento.values()
        )
        print(f"  - {componente}: {total} habilidades")


if __name__ == "__main__":
    main()
