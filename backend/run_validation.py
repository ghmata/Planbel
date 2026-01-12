#!/usr/bin/env python3
"""
PlanBel 2.0 - Script de Validação de Prompts
Executa o crew de validação para testar o prompt mestre
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.prompts import SYSTEM_PROMPT, build_prompt, TEST_SCENARIOS
from src.bncc import get_bncc_context
from src.utils import get_groq_client

console = Console()


def test_single_generation(scenario: dict) -> dict:
    """
    Testa a geração de um plano de aula para um cenário específico.
    Usa apenas o Groq diretamente (sem CrewAI) para testes rápidos.
    """
    console.print(f"\n[bold blue]📝 Testando: {scenario.get('nome', 'Cenário')}[/bold blue]")
    
    # Obter contexto BNCC
    bncc_context = get_bncc_context(
        scenario["disciplina"],
        scenario["ano_escolar"]
    )
    
    # Construir prompt
    prompt = build_prompt(
        disciplina=scenario["disciplina"],
        ano_escolar=scenario["ano_escolar"],
        tema=scenario["tema"],
        duracao_aulas=scenario.get("duracao_aulas", 1),
        bncc_context=bncc_context,
        metodologia=scenario.get("metodologia"),
        recursos=scenario.get("recursos"),
        observacoes=scenario.get("observacoes")
    )
    
    # Gerar plano
    client = get_groq_client()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Gerando plano de aula...", total=None)
        result = client.generate(prompt, system_prompt=SYSTEM_PROMPT)
        progress.update(task, completed=True)
    
    if result["success"]:
        console.print(f"[green]✅ Gerado com sucesso![/green] ({result['tokens_used']} tokens)")
        
        # Salvar output
        output_dir = Path(__file__).parent / "outputs"
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"plano_{scenario.get('nome', 'teste').replace(' ', '_')}_{timestamp}.md"
        output_path = output_dir / filename
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["content"])
        
        console.print(f"[dim]📄 Salvo em: {output_path}[/dim]")
        
        return {
            "success": True,
            "content": result["content"],
            "tokens": result["tokens_used"],
            "file": str(output_path)
        }
    else:
        console.print(f"[red]❌ Erro: {result.get('error', 'Unknown')}[/red]")
        return {
            "success": False,
            "error": result.get("error")
        }


def run_quick_validation():
    """
    Executa validação rápida com todos os cenários de teste.
    Usa Groq direto sem CrewAI para debugging inicial.
    """
    console.print(Panel.fit(
        "[bold]🚀 PlanBel 2.0 - Validação de Prompt Mestre[/bold]\n"
        "[dim]Testando geração de planos de aula com Groq[/dim]",
        border_style="blue"
    ))
    
    results = []
    
    for scenario in TEST_SCENARIOS:
        try:
            result = test_single_generation(scenario)
            results.append({
                "nome": scenario.get("nome"),
                **result
            })
        except Exception as e:
            console.print(f"[red]💥 Erro inesperado: {e}[/red]")
            results.append({
                "nome": scenario.get("nome"),
                "success": False,
                "error": str(e)
            })
    
    # Resumo
    console.print("\n" + "="*60)
    
    table = Table(title="📊 Resumo da Validação")
    table.add_column("Cenário", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Tokens", justify="right")
    
    success_count = 0
    for r in results:
        status = "[green]✅[/green]" if r.get("success") else "[red]❌[/red]"
        tokens = str(r.get("tokens", "-"))
        table.add_row(r["nome"], status, tokens)
        if r.get("success"):
            success_count += 1
    
    console.print(table)
    console.print(f"\n[bold]Resultado: {success_count}/{len(results)} cenários bem-sucedidos[/bold]")


def run_full_crew_validation():
    """
    Executa validação completa com CrewAI (3 agentes).
    Mais lento mas fornece avaliação qualitativa.
    """
    from src.agents import run_validation_crew
    
    console.print(Panel.fit(
        "[bold]🤖 PlanBel 2.0 - Validação com CrewAI[/bold]\n"
        "[dim]Executando crew de 3 agentes para avaliar prompts[/dim]",
        border_style="magenta"
    ))
    
    # Usar primeiro cenário como teste
    scenario = TEST_SCENARIOS[0]
    
    bncc_context = get_bncc_context(scenario["disciplina"], scenario["ano_escolar"])
    prompt = build_prompt(
        disciplina=scenario["disciplina"],
        ano_escolar=scenario["ano_escolar"],
        tema=scenario["tema"],
        duracao_aulas=scenario.get("duracao_aulas", 1),
        bncc_context=bncc_context
    )
    
    console.print(f"\n[bold]Cenário: {scenario['nome']}[/bold]")
    console.print("[dim]Iniciando crew de validação...[/dim]\n")
    
    result = run_validation_crew(prompt, scenario)
    
    console.print("\n[bold green]✅ Validação concluída![/bold green]")
    console.print(result)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="PlanBel 2.0 - Validação de Prompts")
    parser.add_argument(
        "--mode",
        choices=["quick", "crew"],
        default="quick",
        help="Modo de validação: 'quick' (só Groq) ou 'crew' (CrewAI completo)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "quick":
        run_quick_validation()
    else:
        run_full_crew_validation()
