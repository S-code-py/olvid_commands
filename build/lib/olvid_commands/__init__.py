"""
Package pour la gestion des commandes du bot Olvid.

Ce module organise les commandes en groupes et sous-groupes,
et fournit une structure modulaire pour ajouter et gérer
les commandes du bot de manière extensible.
"""

from .bot import Bot
from .base import CommandGroup

__all__ = ["Bot", "CommandGroup"]
