# PokeProject
pokédex en Python en python utilisant l'API https://pokeapi.co

# Pokédex Combat

Un Pokédex interactif avec gestion d’équipe et module de combat simple. Parcours tous les Pokémon, filtre par génération, consulte les fiches détaillées (stats, types, sprite) et constitue une équipe pour affronter une équipe ennemie générée aléatoirement.

---

## Table des matières

- [Fonctionnalités](#fonctionnalités)  
- [Prérequis](#prérequis)  
- [Installation](#installation)  
- [Lancement](#lancement)  
- [Utilisation rapide](#utilisation-rapide)  


---

## Fonctionnalités

- **Liste paginée de tous les Pokémon** récupérés depuis l’API PokeAPI.  
- **Recherche par nom** et **filtrage par génération**.  
- **Fiche Pokémon détaillée** : types, taille, poids, sprite et statistiques (HP, Attack, Defense, Speed, …).  
- **Gestion d’équipe** :
  - Ajouter / retirer des Pokémon.
  - **Limite d’équipe : 6 Pokémon**.
- **Module de combat** :
  - Équipe ennemie générée aléatoirement (taille équivalente à l’équipe du joueur).
  - **Ordre d’action déterminé par la stat `speed`**.
  - Calcul de dégâts simple (prise en compte `attack` et `defense`).
  - Barres de vie proportionnelles et recalculées après chaque action.
  - **Journal de combat** listant action par action (attaquant, cible, dégâts, KO).
  - Modal résultat (Victoire / Défaite) et bouton **Rejouer**.
- Messages utilisateur via `django.contrib.messages`.  
- Responsive et styles CSS pour cartes, barres de PV et boutons.

---

## Prérequis

- Python 3.8 ou supérieur  
- Django 3.2 ou supérieur  
- Connexion Internet (accès à l’API PokeAPI)

---

## Installation

Copier‑coller les commandes suivantes dans un terminal à la racine du projet :

```bash
# cloner le dépôt
git clone <URL_DE_TON_REPO>
cd <NOM_DU_REPO>

# créer et activer un environnement virtuel
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
# Windows (cmd)
venv\Scripts\activate

# installer les dépendances
pip install -r requirements.txt

# appliquer les migrations Django
python manage.py migrate

```
---

## Lancement

Copier‑coller les commandes suivantes pour démarrer le serveur de développement :

# activer l'environnement si nécessaire
- **macOS / Linux**
source venv/bin/activate
- **Windows (PowerShell)**
venv\Scripts\Activate.ps1

- **lancer le serveur de développement**
python manage.py runserver

- **ouvrir dans le navigateur**
 http://127.0.0.1:8000/

---

## Utilisation rapide

- **Parcourir le Pokédex :**
page d’accueil — recherche et filtrage par génération.

- **Voir une fiche :** 
cliquer sur un Pokémon pour consulter ses stats et son sprite.

- **Gérer l’équipe :** 
depuis la fiche, cliquer sur Ajouter (max 6). Voir la page Équipe pour gérer les membres.

- **Lancer un combat :** 
depuis la page Équipe, cliquer sur Lancer un combat. Choisir une attaque pour le Pokémon actif ; l’ordre d’action est déterminé par la stat speed. Le journal de combat (en haut) affiche chaque action. À la fin, un modal indique Victoire ou Défaite ; cliquer sur Rejouer pour recommencer.

---




