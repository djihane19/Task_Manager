#!/usr/bin/env python3
"""
Task Manager CLI —  Edition.
Simple. Rapide. Efficace. Pas de pitié pour les bugs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

TASKS_FILE = Path("tasks.json")


@dataclass
class Task:
    title: str
    done: bool = False


def load_tasks(file_path: Path = TASKS_FILE) -> List[Task]:
    """Charge les tâches depuis un fichier JSON. Retourne [] si absent/vide."""
    if not file_path.exists():
        return []

    try:
        raw = file_path.read_text(encoding="utf-8").strip()
        if not raw:
            return []

        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("Le JSON doit contenir une liste de tâches.")

        tasks: List[Task] = []
        for item in data:
            if not isinstance(item, dict) or "title" not in item:
                raise ValueError("Format de tâche invalide dans le JSON.")
            tasks.append(
                Task(
                    title=str(item["title"]),
                    done=bool(item.get("done", False))
                )
            )
        return tasks

    except (json.JSONDecodeError, OSError, ValueError) as exc:
        print(f"[ERREUR] Impossible de charger {file_path}: {exc}")
        return []


def save_tasks(tasks: List[Task], file_path: Path = TASKS_FILE) -> None:
    """Sauvegarde les tâches en JSON lisible."""
    try:
        payload = [asdict(t) for t in tasks]
        file_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        print(f"[ERREUR] Impossible d'écrire {file_path}: {exc}")


def add_task(tasks: List[Task]) -> None:
    """Ajoute une tâche. Refuse les titres vides."""
    title = input("Titre de la tâche: ").strip()
    if not title:
        print("Non. Une tâche vide, c’est du bruit. Recommence.")
        return

    tasks.append(Task(title=title))
    save_tasks(tasks)
    print("Boom. Tâche ajoutée.")


def list_tasks(tasks: List[Task]) -> None:
    """Affiche toutes les tâches."""
    if not tasks:
        print("Rien à faire. Soit t’es trop fort, soit tu procrastines.")
        return

    print("\n=== TES TÂCHES ===")
    for idx, task in enumerate(tasks, start=1):
        status = "✓" if task.done else " "
        print(f"{idx:>2}. [{status}] {task.title}")
    print()


def mark_done(tasks: List[Task]) -> None:
    """Marque une tâche comme terminée (avec contrôle d'index)."""
    if not tasks:
        print("Aucune tâche à terminer. Logique.")
        return

    list_tasks(tasks)
    raw = input("Numéro de la tâche à terminer: ").strip()

    try:
        num = int(raw)
    except ValueError:
        print("Numéro invalide. Tu sais compter, non ?")
        return

    if num < 1 or num > len(tasks):
        print("Hors limites. Choisis un numéro existant.")
        return

    task = tasks[num - 1]
    if task.done:
        print("Déjà terminée. Tu veux juste faire du bruit.")
        return

    task.done = True
    save_tasks(tasks)
    print("Terminé. Propre.")


def menu() -> None:
    """Boucle principale CLI."""
    tasks = load_tasks()

    while True:
        print("=== TASK MANAGER (Bakugo Mode) ===")
        print("1) Ajouter une tâche")
        print("2) Voir les tâches")
        print("3) Marquer comme terminée")
        print("4) Sauver (tasks.json)")
        print("5) Recharger (tasks.json)")
        print("0) Quitter")
        choice = input("Choix: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            save_tasks(tasks)
            print("Sauvegardé. Pas d’excuses.")
        elif choice == "5":
            tasks = load_tasks()
            print("Rechargé. On repart au combat.")
        elif choice == "0":
            print("Dégage proprement. À la prochaine.")
            break
        else:
            print("Choix invalide. Arrête de taper n’importe quoi.")


if __name__ == "__main__":
    menu()
