"""Módulo BNCC do PlanBel 2.0"""
from .bncc_data import (
    COMPETENCIAS_GERAIS,
    load_habilidades,
    get_bncc_context,
    list_available_habilidades,
    get_habilidade_por_codigo,
    get_disciplinas_disponiveis,
    count_habilidades
)

# Alias para compatibilidade
HABILIDADES = load_habilidades()

__all__ = [
    "COMPETENCIAS_GERAIS",
    "HABILIDADES",
    "load_habilidades",
    "get_bncc_context",
    "list_available_habilidades",
    "get_habilidade_por_codigo",
    "get_disciplinas_disponiveis",
    "count_habilidades"
]
