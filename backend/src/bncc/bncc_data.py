"""
PlanBel 2.0 - Dados BNCC Estruturados
Carrega habilidades do JSON extraído do PDF oficial
"""

import json
from pathlib import Path
from functools import lru_cache


# Competências Gerais da BNCC (resumo compacto para contexto)
COMPETENCIAS_GERAIS = """
As 10 Competências Gerais da BNCC:
1. Conhecimento: valorizar e utilizar conhecimentos sobre o mundo
2. Pensamento científico: investigar, elaborar hipóteses, propor soluções
3. Repertório cultural: valorizar manifestações artísticas e culturais
4. Comunicação: utilizar diferentes linguagens
5. Cultura digital: compreender e criar tecnologias digitais
6. Trabalho e projeto de vida: valorizar o trabalho e fazer escolhas
7. Argumentação: argumentar com base em fatos e dados
8. Autoconhecimento: conhecer-se e cuidar de sua saúde
9. Empatia e cooperação: exercitar empatia e diálogo
10. Responsabilidade e cidadania: agir com responsabilidade
"""


@lru_cache(maxsize=1)
def load_habilidades() -> dict:
    """
    Carrega habilidades do arquivo JSON extraído da BNCC.
    Usa cache para evitar leitura repetida do arquivo.
    """
    json_path = Path(__file__).parent.parent.parent / "bncc_habilidades.json"
    
    if not json_path.exists():
        print(f"⚠️ Arquivo não encontrado: {json_path}")
        return {}
    
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


# Alias para compatibilidade
HABILIDADES = load_habilidades()


def get_bncc_context(disciplina: str, ano: str) -> str:
    """
    Retorna contexto BNCC formatado para o prompt.
    
    Args:
        disciplina: Nome da disciplina (ex: "Matemática")
        ano: Ano escolar (ex: "7º ano")
        
    Returns:
        Texto formatado com competências e habilidades relevantes
    """
    context_parts = [COMPETENCIAS_GERAIS.strip()]
    habilidades = load_habilidades()
    
    # Normalizar ano para busca
    ano_normalizado = ano.replace("º", "").replace("°", "")
    ano_num = int(''.join(filter(str.isdigit, ano_normalizado)) or "0")
    
    # Determinar segmento
    if "Médio" in ano:
        segmento = "Ensino Médio"
    elif ano_num <= 5:
        segmento = "Anos Iniciais"
    else:
        segmento = "Anos Finais"
    
    # Buscar habilidades na disciplina
    if disciplina in habilidades:
        disc_data = habilidades[disciplina]
        
        if segmento in disc_data:
            seg_data = disc_data[segmento]
            
            # Buscar ano específico ou similar
            for ano_key, hab_dict in seg_data.items():
                # Match flexível: "7º ano" casa com "7º ano", "7° ano", etc.
                if str(ano_num) in ano_key:
                    context_parts.append(f"\n\nHabilidades BNCC - {disciplina} - {ano_key}:")
                    
                    # Limitar a 10 habilidades mais relevantes para economizar tokens
                    count = 0
                    for codigo, descricao in hab_dict.items():
                        if count >= 10:
                            context_parts.append(f"  ... e mais {len(hab_dict) - 10} habilidades")
                            break
                        # Truncar descrições longas
                        desc_curta = descricao[:150] + "..." if len(descricao) > 150 else descricao
                        context_parts.append(f"- {codigo}: {desc_curta}")
                        count += 1
                    break
    
    return "\n".join(context_parts)


def list_available_habilidades(disciplina: str | None = None) -> list[str]:
    """Lista todas as habilidades disponíveis, opcionalmente filtradas por disciplina."""
    result = []
    habilidades = load_habilidades()
    
    for disc_nome, disc_data in habilidades.items():
        if disciplina and disc_nome != disciplina:
            continue
            
        for segmento, seg_data in disc_data.items():
            for ano, hab_dict in seg_data.items():
                for codigo, descricao in hab_dict.items():
                    desc_curta = descricao[:100] + "..." if len(descricao) > 100 else descricao
                    result.append(f"{codigo} | {disc_nome} | {ano} | {desc_curta}")
    
    return result


def get_habilidade_por_codigo(codigo: str) -> dict | None:
    """
    Busca uma habilidade específica pelo código.
    
    Args:
        codigo: Código da habilidade (ex: "EF07MA12")
        
    Returns:
        Dict com informações da habilidade ou None se não encontrada
    """
    habilidades = load_habilidades()
    
    for disc_nome, disc_data in habilidades.items():
        for segmento, seg_data in disc_data.items():
            for ano, hab_dict in seg_data.items():
                if codigo in hab_dict:
                    return {
                        "codigo": codigo,
                        "descricao": hab_dict[codigo],
                        "disciplina": disc_nome,
                        "segmento": segmento,
                        "ano": ano
                    }
    
    return None


def get_disciplinas_disponiveis() -> list[str]:
    """Retorna lista de disciplinas disponíveis no banco."""
    return list(load_habilidades().keys())


def count_habilidades() -> dict:
    """Retorna contagem de habilidades por disciplina."""
    habilidades = load_habilidades()
    contagem = {}
    
    for disc_nome, disc_data in habilidades.items():
        total = sum(
            len(hab_dict) 
            for seg_data in disc_data.values() 
            for hab_dict in seg_data.values()
        )
        contagem[disc_nome] = total
    
    return contagem


if __name__ == "__main__":
    # Teste rápido
    print("📊 Contagem de habilidades:")
    for disc, count in count_habilidades().items():
        print(f"  - {disc}: {count}")
    
    print("\n📝 Exemplo de contexto para Matemática 7º ano:")
    print(get_bncc_context("Matemática", "7º ano"))
