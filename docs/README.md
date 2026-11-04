# Documentation

Un document par séance de travaux pratiques. Chacun suit la même structure :

1. objectifs et lien avec le cours ;
2. choix d'implémentation ;
3. analyse de complexité ;
4. réponses rédigées aux questions théoriques ;
5. comment lancer le code et les tests.

| Séance | Sujet | Document |
|---|---|---|
| 1 | Listes chaînées, simulation de train, piles, parenthèses | [TP01-data-structures.md](TP01-data-structures.md) |
| 2 | Complexité, classes de croissance, benchmarks | [TP02-complexity.md](TP02-complexity.md) |
| 3 | Récursivité, diviser pour régner, Hanoï, recherche | [TP03-recursion.md](TP03-recursion.md) |
| 4 | Tri par sélection, tri fusion, tri aux deux tiers, bonbons | [TP04-sorting.md](TP04-sorting.md) |
| 5 | ABR, arbres d'expression, arbres ternaires, Akinator | [TP05-trees.md](TP05-trees.md) |
| 6 | Tables de hachage, arbres AVL, catalogue de vinyles | [TP06-associative-arrays.md](TP06-associative-arrays.md) |
| 7 | Graphes, Euler, coloration, couvertures | [TP07-graphs.md](TP07-graphs.md) |
| 8 | NetworkX, Dijkstra, routage OSMnx | [TP08-networkx-dijkstra.md](TP08-networkx-dijkstra.md) |

Les notebooks se trouvent dans [`../notebooks`](../notebooks) :

- `tp08_networkx_dijkstra.ipynb` — exécuté, avec sorties et figures ;
- `tp08_osmnx_routing.ipynb` — code pour la partie optionnelle de routage dans le
  monde réel.

## Conventions

- Les commentaires et les docstrings sont désormais en français ; les
  identifiants (variables, fonctions, classes, fichiers et modules) restent en
  anglais. Les énoncés du cours et les réponses rédigées conservent la
  terminologie française d'origine (par exemple *tas*, *parcours*,
  *complexité*).
- Les positions sont indexées à partir de 0 dans le code et sont documentées
  lorsque l'énoncé lui-même utilise une autre convention.
- Toute affirmation de complexité dans ces documents est soit démontrée, soit
  illustrée par un benchmark dans le module correspondant.
