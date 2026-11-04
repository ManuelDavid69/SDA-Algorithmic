# TP 7 — Graphes : notions de base

## Objectifs

- représenter un graphe à l'aide d'une liste d'adjacence, et construire ses
  matrices d'adjacence et d'incidence ;
- calculer les degrés, les voisinages, les sous-graphes induits et la régularité ;
- parcours (BFS/DFS), composantes connexes et bipartisme ;
- circuits et chaînes eulérien(ne)s ;
- coloration gloutonne et exacte, ensembles indépendants, couplages et couvertures ;
- appliquer ces notions au graphe de Petersen, à un emploi du temps, à une
  enveloppe, au problème des ambassadeurs et aux plans du musée et du château.

La bibliothèque se trouve dans `src/sda/tp07_graphs` :

| Module | Contenu |
|---|---|
| `graph.py` | `Graph` et tous les algorithmes |
| `examples.py` | graphe de Petersen, enveloppe, emploi du temps des langues |
| `analysis.py` | les réponses du TD, calculées à partir des graphes |

Le TD est essentiellement théorique. Les graphes entièrement spécifiés dans
l'énoncé (Petersen, l'emploi du temps des langues, l'enveloppe) sont encodés dans
`examples.py` ; les deux exercices fournis uniquement sous forme d'image (le
musée et les cinq pièces) sont résolus par les algorithmes génériques une fois
leur plan encodé sous forme d'arêtes.

---

## Exercice 1 — Le graphe de Petersen

### a) Orienté ou non ?

Non orienté. Les arêtes sont symétriques : si `6` est adjacent à `7`, alors `7`
est adjacent à `6` ; aucune flèche n'est dessinée.

### b) Sommets et arêtes

Sommets : `1, 2, ..., 10`. Arêtes (15) :

```
6-7, 7-8, 8-9, 9-10, 10-6          (pentagone extérieur)
6-1, 7-2, 8-3, 9-4, 10-5          (rayons)
1-3, 3-5, 5-2, 2-4, 4-1           (pentagramme intérieur)
```

### c) Voisins de 2, degré de 10

`N(2) = {4, 5, 7}` (rayon `2-7`, arêtes en étoile `2-4` et `2-5`).

`deg(10) = 3` (voisins `6`, `9` et `5`).

### d) Régulier ?

Oui : chaque sommet a pour degré 3, donc le graphe est **3-régulier** (cubique).

### e) Matrices

Matrice d'adjacence (lignes/colonnes `1..10`) :

```
0 0 1 1 0 1 0 0 0 0
0 0 0 1 1 0 1 0 0 0
1 0 0 0 1 0 0 1 0 0
1 1 0 0 0 0 0 0 1 0
0 1 1 0 0 0 0 0 0 1
1 0 0 0 0 0 1 0 0 1
0 1 0 0 0 1 0 1 0 0
0 0 1 0 0 0 1 0 1 0
0 0 0 1 0 0 0 1 0 1
0 0 0 0 1 1 0 0 1 0
```

La matrice d'incidence a 10 lignes (sommets) et 15 colonnes (arêtes) ; chaque
colonne contient exactement deux `1`, aux extrémités de l'arête. Les deux
matrices sont produites par `graph.adjacency_matrix()` et
`graph.incidence_matrix()` dans `petersen_report()`.

### f) Sous-graphe induit sur `{1, 3, 5, 6, 7, 8}`

Les arêtes induites sont :

```
1-3, 1-6, 3-5, 3-8, 6-7, 7-8
```

Il possède 6 sommets et 6 arêtes : un cycle de longueur 5 `1-3-8-7-6-1` avec le
sommet pendant `5` rattaché à `3`. Degrés : `deg(1)=2`, `deg(3)=3`, `deg(5)=1`,
`deg(6)=2`, `deg(7)=2`, `deg(8)=2`.

### g) Planaire ?

Non. Le graphe de Petersen est l'exemple classique de graphe non planaire : il
contient une subdivision de `K3,3` (théorème de Kuratowski). C'est également le
plus petit graphe cubique non planaire sans pont.

### Bonus

| Quantité | Valeur |
|---|---|
| Nombre chromatique | 3 |
| Nombre d'indépendance | 4 |
| Couplage maximum | 5 |
| Couverture de sommets minimum | 6 |

---

## Exercice 2 — Emploi du temps des langues

Données :

| Étudiant | Cours |
|---|---|
| Axel | anglais, espagnol |
| Béatrice | russe, grec |
| Corentin | anglais, italien |
| Dylan | russe, espagnol |
| Emilie | anglais, russe |

### a) Graphe et nature

La représentation naturelle est un **graphe biparti** : les étudiants d'un côté,
les cours de l'autre, et une arête `(étudiant, cours)` lorsque l'étudiant suit
le cours. Aucune arête ne relie deux étudiants ou deux cours, donc le graphe est
biparti par construction.

Un second graphe utile est le **graphe des étudiants** : deux étudiants sont
adjacents lorsqu'ils partagent au moins un cours. Il n'est pas biparti (par
exemple `Axel - Corentin - Emilie - Axel` est un triangle).

### b) Paires possibles

Deux étudiants forment une paire lorsqu'ils partagent au moins un cours. Les
sept paires sont :

```
Axel-Corentin, Axel-Dylan, Axel-Emilie,
Béatrice-Dylan, Béatrice-Emilie,
Corentin-Emilie, Dylan-Emilie
```

### c) Plus grand groupe sans cours commun

Au plus **2**. Exemple : `{Axel, Béatrice}` (Axel suit anglais/espagnol,
Béatrice russe/grec) ; `{Corentin, Dylan}` en est un autre. Il n'existe pas
d'ensemble indépendant de taille 3 dans le graphe des étudiants.

### d) Diffusion du message

Oui. Le graphe biparti étudiant-cours est connexe. Par exemple :

```
grec -- Béatrice -- russe -- Dylan -- espagnol
                      |
                    Emilie -- anglais -- Corentin -- italien
```

Le message peut donc circuler de n'importe quel cours vers n'importe quel autre
cours en passant par des étudiants.

### e) Emploi du temps

Construire le **graphe de conflits des cours** : deux cours sont adjacents
lorsqu'au moins un étudiant suit les deux. Ses arêtes sont :

```
anglais-espagnol, anglais-italien, anglais-russe,
russe-espagnol, russe-grec
```

Il est 3-colorable et 3 couleurs sont nécessaires (le triangle
`anglais-espagnol-russe`). Ainsi :

- au plus **3 cours** peuvent être placés dans le même créneau ;
- **3 créneaux** sont nécessaires et suffisants.

Une affectation valide :

| Créneau | Cours |
|---|---|
| 1 | anglais, grec |
| 2 | russe, italien |
| 3 | espagnol |

Vérification : anglais et grec ne partagent aucun étudiant ; russe et italien
non plus.

---

## Exercice 3 — L'enveloppe

Les cinq points d'intersection sont les sommets `T` (haut), `UL`, `UR`, `LL`,
`LR`. Le graphe possède 8 arêtes et les degrés suivants :

| Sommet | T | UL | UR | LL | LR |
|---|---|---|---|---|---|
| Degré | 2 | 4 | 4 | 3 | 3 |

### a) Se terminer au point de départ ?

Non. Un **circuit** eulérien exige que chaque sommet ait un degré pair ; `LL` et
`LR` sont impairs.

### b) Sans nécessairement finir au départ ?

Oui. Il y a exactement deux sommets impairs, ce qui est la condition nécessaire
et suffisante pour une **chaîne** eulérienne. Il faut partir de l'un des sommets
impairs et terminer à l'autre. Par exemple :

```
LL -> UL -> T -> UR -> UL -> LR -> UR -> LL -> LR
```

Ce parcours utilise chacune des 8 arêtes exactement une fois ; le chemin inverse
est également valide.

---

## Exercice 4 — Graphes isomorphes

Les deux dessins ont 10 sommets et sont 3-réguliers, comme le graphe de Petersen,
donc la suite des degrés ne suffit pas à décider. Le dessin de droite est le
plongement habituel de Petersen (pentagone extérieur, pentagramme intérieur,
cinq rayons). Pour décider pour le dessin de gauche, encoder sa liste d'arêtes et
appeler :

```python
left = Graph.from_edges([...])
left.is_isomorphic(petersen_graph())
```

`Graph.is_isomorphic` vérifie la suite des degrés, puis cherche une bijection qui
préserve l'adjacence (petits graphes uniquement). Un invariant plus rapide à
calculer à la main est la **maille** : Petersen a une maille de 5 ; un dessin qui
contient un triangle ou un cycle de longueur 4 ne peut pas lui être isomorphe.

---

## Exercice 5 — Réception à l'ambassade

Le lemme des poignées de main dit que la somme de tous les degrés vaut deux fois
le nombre d'arêtes, donc est **paire**.

### a) 48 ambassadeurs ?

Si les 48 personnes présentes connaissent chacune exactement 11 autres personnes,
la somme des degrés vaut `48 * 11 = 528`, qui est paire : la parité ne l'exclut
pas, et un graphe 11-régulier sur 48 sommets existe, donc l'affirmation est
possible.

Si l'hôte est un 49e participant (la formulation « 48 homologues » le suggère),
la somme vaut `49 * 11 = 539`, qui est impaire : impossible. La suite de
l'exercice (47 homologues) indique que le total visé est de 48 personnes ;
l'ambiguïté mérite d'être signalée.

### b) Un invité absent

Avec 48 personnes, la somme est paire ; avec 47 personnes elle vaut
`47 * 11 = 517`, impaire, donc l'affirmation est **impossible**. C'est
l'argument de parité que recherche l'exercice.

### c) Poignées de main

Avec 48 ambassadeurs, chacun salue les 47 autres, et chaque poignée de main est
comptée deux fois :

```
C(48, 2) = 48 * 47 / 2 = 1128
```

`ambassadors_report()` renvoie ces vérifications ; `ambassadors_possible(n, 11)`
implémente le test de parité.

---

## Exercice 6 — Une nuit au musée

Encoder chaque salle comme un sommet et chaque couloir comme une arête.

- Un gardien placé **dans un couloir** couvre les deux salles situées à ses
  extrémités. L'ensemble des couloirs choisis doit toucher chaque sommet : c'est
  une **couverture d'arêtes minimum**. Pour un graphe sans sommet isolé,
  `|couverture d'arêtes| = n - |couplage maximum|`.
- Un gardien placé **dans une salle** couvre tous les couloirs incidents à cette
  salle. L'ensemble des salles choisies doit toucher chaque arête : c'est une
  **couverture de sommets minimum**. Par complémentarité avec les ensembles
  indépendants, `|couverture de sommets| = n - |ensemble indépendant maximum|`.

Une fois le plan encodé :

```python
museum = Graph.from_edges([...])
len(museum.min_edge_cover())   # gardiens dans les couloirs
len(museum.min_vertex_cover()) # gardiens dans les salles
```

Les deux nombres diffèrent généralement : une couverture d'arêtes peut être plus
petite parce qu'un couloir couvre deux salles à la fois, tandis qu'un gardien
posté dans une salle couvre plusieurs couloirs.

---

## Exercice 7 — Les cinq pièces

Modéliser les cinq pièces **et le jardin extérieur** comme des sommets, et chaque
porte comme une arête entre les deux lieux qu'elle relie. La question « passer
exactement une fois par chaque porte » est exactement un problème de **chaîne
eulérienne** :

- si chaque sommet a un degré pair, un circuit eulérien existe (partir de
  n'importe où) ;
- si exactement deux sommets ont un degré impair, une chaîne eulérienne existe
  (partir de l'un des sommets impairs et terminer à l'autre) ;
- s'il y a plus de deux sommets impairs, une telle marche n'existe pas.

`Graph.eulerian_circuit()` et `Graph.eulerian_path()` implémentent le test et la
construction de Hierholzer. Il suffit d'encoder le plan imprimé sous forme de
liste d'arêtes ; la parité des degrés donne immédiatement la réponse.

---

## Notes d'implémentation

- `Graph` utilise un dictionnaire d'adjacence `sommet -> {voisin: poids}` ; les
  arêtes non orientées sont stockées dans les deux sens.
- `edges()` renvoie chaque arête non orientée une seule fois, `adjacency_matrix()`
  est symétrique et `incidence_matrix()` place deux `1` par arête non orientée.
- BFS/DFS et les composantes connexes sont en `O(V + E)`.
- Les chaînes eulériennes utilisent l'algorithme de Hierholzer en `O(V + E)`
  après la vérification des degrés.
- La coloration est exponentielle dans le pire cas (retour sur trace), mais les
  graphes du TD sont minuscules. `greedy_coloring()` fournit rapidement une
  borne supérieure.
- Les couplages et les ensembles indépendants utilisent une recherche par
  séparation et évaluation (branch-and-bound) / retour sur trace, adaptée aux
  graphes à 10 sommets des exercices.

---

## Exécution

```bash
python -m sda.tp07_graphs.demo
python -m pytest tests/test_tp07_graphs.py
```
