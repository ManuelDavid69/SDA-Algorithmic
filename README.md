# SDA Algorithmic

![Python CI](https://github.com/ManuelDavid69/SDA-Algorithmic/actions/workflows/python.yml/badge.svg)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![Tests](https://img.shields.io/badge/tests-333%20r%C3%A9ussis-brightgreen)
![Licence MIT](https://img.shields.io/badge/licence-MIT-yellow)

Travaux pratiques du cours de **Structures de données et algorithmique** à
**CPE Lyon** (3IRC, 2025/2026), réécrits intégralement en Python.

Le dépôt suit les huit séances du cours : listes chaînées et piles, analyse de
complexité, récursivité et diviser pour régner, tri, arbres, tables de hachage
et arbres AVL, théorie des graphes, et enfin NetworkX avec l'algorithme de plus
court chemin de Dijkstra.

> Les énoncés des exercices sont des supports de cours de CPE Lyon. Ce dépôt
> contient les implémentations, les tests, les benchmarks et les réponses
> rédigées.

---

## Sommaire

- [Vue d'ensemble](#vue-densemble)
- [Points forts](#points-forts)
- [Démarrage rapide](#démarrage-rapide)
- [Structure du dépôt](#structure-du-dépôt)
- [Les huit séances](#les-huit-séances)
- [Tests](#tests)
- [Récapitulatif des complexités](#récapitulatif-des-complexités)
- [Notebooks](#notebooks)
- [Documentation](#documentation)
- [Crédits](#crédits)
- [Licence](#licence)

---

## Vue d'ensemble

| # | Séance | Principaux livrables | Documentation |
|---|---|---|---|
| 1 | **Structures de données** | `Node`/`LinkedList` réimplémentés, simulation de train, pile chaînée, vérificateur de parenthèses qui indique la ligne et la colonne | [TP01](docs/TP01-data-structures.md) |
| 2 | **Complexité** | comptage d'opérations, classement de la croissance de 15 fonctions, benchmark de primalité, tables temps/taille, preuve en `Theta` | [TP02](docs/TP02-complexity.md) |
| 3 | **Récursivité** | trois variantes de Fibonacci, maximum par diviser pour régner, Tours de Hanoï, recherche dichotomique récursive/itérative, théorème maître | [TP03](docs/TP03-recursion.md) |
| 4 | **Tri** | tri par sélection, tri fusion, tri aux deux tiers, distribution de bonbons (force brute vs fenêtre glissante) | [TP04](docs/TP04-sorting.md) |
| 5 | **Arbres** | ABR avec suppression, affichage ASCII, arbres d'expression RPN, analyseur d'expressions ternaires imbriquées, Akinator avec persistance JSON | [TP05](docs/TP05-trees.md) |
| 6 | **Tableaux associatifs** | table de hachage avec pierres tombales `DELETED`, arbre AVL avec requêtes par intervalle, catalogue de vinyles à deux index | [TP06](docs/TP06-associative-arrays.md) |
| 7 | **Graphes** | bibliothèque de graphes, graphe de Petersen, emploi du temps, chaînes eulériennes, coloration, couplages et couvertures | [TP07](docs/TP07-graphs.md) |
| 8 | **NetworkX et Dijkstra** | graphe pondéré reproductible, trois implémentations de Dijkstra, notebook de routage OSMnx | [TP08](docs/TP08-networkx-dijkstra.md) |

---

## Points forts

- **333 tests** couvrant chaque séance, y compris les cas limites et les
  invariants.
- Algorithmes essentiels écrits **sans raccourcis** : pas de `list.sort()` dans
  les implémentations de tri, pas d'appel au plus court chemin de NetworkX dans
  Dijkstra, pas de `collections.deque` dans les structures chaînées.
- Trois variantes de Dijkstra qui rendent mesurable l'impact de la structure de
  données des sommets visités : sur un graphe de 400 sommets, la version avec
  liste est environ **20× plus lente** que la version avec ensemble, et environ
  **130× plus lente** que la version avec tas.
- Les réponses de complexité sont vérifiées par le code : les formules de
  comptage d'opérations sont comparées aux boucles instrumentées, l'ordre de
  croissance est encodé sous forme de classes `Theta`, et l'algorithme des
  bonbons est comparé à la force brute sur des instances aléatoires.
- **Notebook Jupyter** exécuté pour la séance NetworkX/Dijkstra, et un
  calculateur d'itinéraire OSMnx prêt à l'emploi.

---

## Démarrage rapide

Prérequis : **Python 3.11+**.

```bash
git clone https://github.com/ManuelDavid69/SDA-Algorithmic.git
cd SDA-Algorithmic

python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

python -m pip install -e ".[dev]"
python -m pytest
```

Lancer la démonstration d'une séance :

```bash
python -m sda.tp01_data_structures.demo
python -m sda.tp02_complexity.demo
python -m sda.tp03_recursion.demo
python -m sda.tp04_sorting.demo
python -m sda.tp05_trees.demo
python -m sda.tp06_associative_arrays.demo
python -m sda.tp07_graphs.demo
python -m sda.tp08_networkx.demo
```

Vérifier le code avec Ruff :

```bash
python -m ruff check .
```

---

## Structure du dépôt

```
src/sda/
|-- tp01_data_structures/    liste chaînée, train, pile, analyse de parenthèses
|-- tp02_complexity/         comptages d'opérations, classes de croissance, benchmarks
|-- tp03_recursion/          affichages, Fibonacci, Hanoï, recherche dichotomique
|-- tp04_sorting/            sélection, fusion, deux tiers, bonbons
|-- tp05_trees/              ABR, affichage, arbres d'expression, ternaire, Akinator
|-- tp06_associative_arrays/ table de hachage, arbre AVL, catalogue de vinyles
|-- tp07_graphs/             bibliothèque de graphes, exemples, réponses de TD
`-- tp08_networkx/           jeu de données, variantes de Dijkstra, utilitaires OSMnx

tests/                       333 tests pytest, un fichier par séance
docs/                        un document détaillé par séance
notebooks/                   notebooks NetworkX/Dijkstra et OSMnx
data/                        jeu de données de graphe pondéré pour le TP 8
.github/workflows/python.yml CI sur Python 3.11, 3.12 et 3.13
```

---

## Les huit séances

### 1. Listes chaînées et piles

- `Node` et `LinkedList` avec insertion, suppression, recherche, accès, taille
  et un `repr` lisible.
- Simulation de train : chaque wagon contient quatre passagers ; un wagon plein
  envoie le passager vers le suivant, avec l'extension optionnelle « retour vers
  l'avant ».
- `Stack` chaînée et vérificateur de parenthèses pour `()`, `[]`, `{}` et `<>`,
  avec la ligne et la colonne exactes de la première erreur.

### 2. Complexité

- Cinq programmes instrumentés avec des formules explicites de comptage
  d'opérations.
- Les 15 fonctions de l'énoncé classées en 12 classes `Theta`.
- Benchmark de test de primalité, table théorique des temps pour `n = 10^6`, et
  table inverse (plus grande instance en 1 seconde, 1 minute, ...).
- Preuve que `3n^2 - 100n + 6 = Theta(n^2)` à partir de la définition.

### 3. Récursivité et diviser pour régner

- Fibonacci naïf, mémoïsé et récursif terminal, avec des temps mesurés.
- Maximum par diviser pour régner, Tours de Hanoï (déplacements rejoués et
  vérifiés quant à leur légalité), recherche dichotomique récursive et
  itérative.
- Réponses complètes sur le théorème maître, y compris les cas où il ne
  s'applique pas.

### 4. Tri

- Tri par sélection avec son invariant de boucle, tri fusion avec trois
  analyses (itération, arbre de récursion, théorème maître).
- Tri aux deux tiers de l'examen 2024, avec une preuve de correction et sa
  complexité `Theta(n^2.71)`.
- Distribution de bonbons : force brute et solution en `O(n log n)` par fenêtre
  glissante, recoupées sur des instances aléatoires.

### 5. Arbres

- ABR avec les trois cas de suppression, parcours, hauteur et vérification de
  validité.
- Rendu ASCII de n'importe quel arbre binaire.
- Arbres d'expression à partir de la RPN, affichage infixe avec parenthèses, et
  évaluation directe de la RPN avec une pile.
- Analyseur descendant récursif pour les expressions ternaires imbriquées.
- Akinator qui pose des questions, apprend un nouvel animal et sauvegarde son
  arbre en JSON.

### 6. Tables de hachage et arbres AVL

- Table de hachage avec sondage linéaire, comptage des sondages et pierres
  tombales `DELETED` ; le contre-exemple de suppression est reproduit dans les
  tests.
- Arbre AVL avec rotations LL/RR/LR/RL, facteurs d'équilibre et requêtes par
  intervalle en `O(log n + k)`.
- Catalogue de Vinyl Records Co. indexé à la fois par référence (hachage) et par
  année (AVL), avec une comparaison des deux structures.

### 7. Graphes

- Graphe par listes d'adjacence avec matrices, sous-graphes, BFS/DFS,
  composantes et bipartisme.
- Circuits/chaînes eulériennes (Hierholzer), coloration gloutonne et exacte,
  ensembles indépendants, couplages, couvertures de sommets et d'arêtes, tests
  d'isomorphisme.
- Graphe de Petersen encodé, emploi du temps des langues et enveloppe ; réponses
  de TD calculées par la bibliothèque.

### 8. NetworkX et Dijkstra

- Découverte de NetworkX sur le graphe de Petersen (degrés, matrices,
  sous-graphe, dessin).
- Dijkstra avec une **liste**, un **ensemble** et un **tas binaire** de sommets
  visités, tous renvoyant le même itinéraire ; comparaison des temps sur 20 et
  400 sommets.
- Utilitaires OSMnx pour Lyon : charger le réseau routier, géocoder les deux
  adresses, trouver les nœuds les plus proches, calculer et tracer l'itinéraire.

---

## Tests

```bash
python -m pytest
```

| Fichier de test | Tests | Couverture |
|---|---:|---|
| `test_tp01_linked_list.py` | 16 | opérations de liste, bornes, égalité |
| `test_tp01_train.py` | 12 | capacité, débordement, retour en arrière |
| `test_tp01_stack.py` | 25 | LIFO, parenthèses valides/invalides, positions des erreurs |
| `test_tp02_complexity.py` | 102 | formules explicites, classes de croissance, benchmarks, tables |
| `test_tp03_recursion.py` | 40 | affichages, Fibonacci, légalité de Hanoï, recherches |
| `test_tp04_sorting.py` | 52 | tableaux aléatoires, invariants, bonbons vs force brute |
| `test_tp05_trees.py` | 37 | suppression dans un ABR, rendu, RPN, ternaire, Akinator |
| `test_tp06_associative.py` | 16 | collisions, pierres tombales, rotations, catalogue |
| `test_tp07_graphs.py` | 15 | matrices, parcours, Euler, coloration, couvertures |
| `test_tp08_dijkstra.py` | 18 | jeu de données, trois variantes, comparaison avec NetworkX |
| **Total** | **333** | |

La suite s'exécute en moins d'une seconde et est lancée par GitHub Actions sur
Python 3.11, 3.12 et 3.13.

---

## Récapitulatif des complexités

| Algorithme / structure | Temps | Remarques |
|---|---|---|
| Accès / insertion / suppression dans une liste chaînée | `O(k)` | `O(1)` en tête |
| Pile `push` / `pop` | `O(1)` | implémentation chaînée |
| Insertion / recherche / suppression dans un ABR | `O(h)` | `O(log n)` en moyenne, `O(n)` au pire |
| Insertion / recherche / suppression dans un AVL | `O(log n)` | hauteur stockée dans chaque nœud |
| Requête par intervalle dans un AVL | `O(log n + k)` | `k` années renvoyées |
| Table de hachage (sondage linéaire) | `O(1)` en moyenne, `O(n)` au pire | exemple avec `alpha = 0.694` |
| Tri par sélection | `Theta(n^2)` | meilleur et pire cas |
| Tri fusion | `Theta(n log n)` | `T(n) = 2T(n/2) + Theta(n)` |
| Tri aux deux tiers | `Theta(n^2.71)` | `T(n) = 3T(2n/3) + Theta(1)` |
| Recherche dichotomique | `O(log n)` | entrée triée |
| Dijkstra avec liste des visités | `O(VE)` au pire | test d'appartenance linéaire |
| Dijkstra avec ensemble des visités | `O(V^2 + E)` | recherche linéaire du minimum |
| Dijkstra avec tas | `O((V + E) log V)` | entrées obsolètes ignorées |

---

## Notebooks

- [`notebooks/tp08_networkx_dijkstra.ipynb`](notebooks/tp08_networkx_dijkstra.ipynb)
  — **exécuté**, avec sorties et figures : dessin du graphe de Petersen,
  sous-graphe induit, graphe pondéré, les trois versions de Dijkstra et les
  temps d'exécution.
- [`notebooks/tp08_osmnx_routing.ipynb`](notebooks/tp08_osmnx_routing.ipynb)
  — le calculateur d'itinéraire pour Lyon ; non exécuté car il nécessite un
  accès à Internet et le paquet optionnel `osmnx`.

Pour les ouvrir :

```bash
python -m jupyter notebook notebooks/
```

Pour réexécuter le notebook principal :

```bash
python -m nbconvert --to notebook --execute --inplace notebooks/tp08_networkx_dijkstra.ipynb
```

---

## Documentation

Chaque séance dispose d'un document détaillé présentant les choix
d'implémentation, l'analyse de complexité et les réponses rédigées :

| Séance | Document |
|---|---|
| 1 | [Listes chaînées et piles](docs/TP01-data-structures.md) |
| 2 | [Complexité](docs/TP02-complexity.md) |
| 3 | [Récursivité et diviser pour régner](docs/TP03-recursion.md) |
| 4 | [Tri](docs/TP04-sorting.md) |
| 5 | [Arbres](docs/TP05-trees.md) |
| 6 | [Tables de hachage et arbres AVL](docs/TP06-associative-arrays.md) |
| 7 | [Graphes](docs/TP07-graphs.md) |
| 8 | [NetworkX et Dijkstra](docs/TP08-networkx-dijkstra.md) |

---

## Crédits

- **Cours et énoncés des exercices** : CPE Lyon, *Structures de données et
  algorithmique*, 3IRC, 2025/2026.
- **Implémentations, tests, benchmarks, notebooks et documentation** :
  [Manuel David](https://github.com/ManuelDavid69).

---

## Licence

MIT — voir [LICENSE](LICENSE).
