# TP 8 — NetworkX et Dijkstra

## Objectifs

- découvrir NetworkX sur le graphe de Petersen (sommets, arêtes, degrés,
  matrices, sous-graphe induit, dessin) ;
- charger un graphe pondéré à partir d'une liste d'adjacence multiligne ;
- implémenter **l'algorithme de Dijkstra** à la main, avec trois variantes de
  l'ensemble des sommets visités ;
- comparer les temps d'exécution et expliquer les différences ;
- appliquer le résultat à un réseau routier réel avec OSMnx (facultatif).

Le code se trouve dans `src/sda/tp08_networkx` :

| Module | Contenu |
|---|---|
| `fixture.py` | graphe pondéré reproductible à 20 sommets / 30 arêtes et son fichier |
| `dijkstra.py` | `dijkstra1` (liste), `dijkstra2` (ensemble), `dijkstra_heap` |
| `routing.py` | chargement OSMnx, fonctions de géocodage, tracé d'itinéraire |

Notebooks :

- [`notebooks/tp08_networkx_dijkstra.ipynb`](../notebooks/tp08_networkx_dijkstra.ipynb)
  — découverte de NetworkX, dessin de graphes, les trois versions de Dijkstra et
  les mesures de temps (exécuté, sorties incluses) ;
- [`notebooks/tp08_osmnx_routing.ipynb`](../notebooks/tp08_osmnx_routing.ipynb)
  — le calculateur d'itinéraires lyonnais (non exécuté : il nécessite un accès à
  Internet et le paquet facultatif OSMnx).

---

## 1. Premiers pas avec NetworkX

NetworkX stocke un graphe sous forme de dictionnaire de dictionnaires :
`G[node]` associe à chaque voisin ses données d'arête. Les graphes peuvent être
créés à partir d'une liste d'arêtes, d'une matrice d'adjacence, d'un générateur,
d'un fichier ou d'une copie.

Appels utiles :

| Appel | Résultat |
|---|---|
| `G.is_directed()` | orientation |
| `G.nodes`, `G.edges` | sommets et arêtes |
| `G.neighbors(v)`, `G.degree[v]` | voisinage et degré |
| `nx.is_regular(G)`, `nx.is_connected(G)` | propriétés globales |
| `nx.to_numpy_array(G)` | matrice d'adjacence |
| `nx.incidence_matrix(G)` | matrice d'incidence |
| `G.subgraph(vertices)` | sous-graphe induit |
| `nx.shortest_path(G, s, t, weight=...)` | plus court chemin de référence |

### Vérifications sur le graphe de Petersen

- `G.is_directed()` → `False` ;
- 10 sommets, 15 arêtes ;
- `neighbors(2)` → `[7, 5, 4]` (l'ordre dépend de l'insertion), soit
  `{4, 5, 7}` ; `degree(9)` → 3 ;
- `nx.is_regular(G)` → `True`, degré 3 ;
- connexe, non biparti ;
- la matrice d'adjacence est de taille 10 × 10 et la matrice d'incidence de
  taille 10 × 15, avec deux `1` par colonne ;
- le sous-graphe induit sur `{6, 3, 7, 8, 1, 5}` possède 6 sommets et 6 arêtes.

Le notebook dessine le graphe avec la disposition habituelle en deux pentagones
et affiche le sous-graphe induit.

---

## 2. Le graphe pondéré

`data/tp08_graph.txt` suit le format de liste d'adjacence multiligne de l'énoncé
et contient 20 sommets, 30 arêtes et des poids entiers entre 1 et 50. Il est
chargé avec :

```python
graph = nx.read_multiline_adjlist(path, nodetype=int)
```

Le jeu de données de test est déterministe (liste d'arêtes fixe), donc les tests
et le notebook produisent toujours le même plus court chemin :

```
0 -> 8 -> 6 -> 13 -> 19, longueur 112
```

---

## 3. Dijkstra à la main

L'algorithme maintient :

- `distances[v]` : meilleure distance connue depuis la source ;
- `previous[v]` : prédécesseur sur le meilleur chemin trouvé jusqu'ici ;
- `visited` : sommets dont la distance est définitive.

À chaque itération :

1. sélectionner le sommet non visité `u` de plus petit `distances[u]` ;
2. le marquer comme visité ;
3. pour chaque voisin `v` de `u`, relâcher l'arête :
   `distances[v] = min(distances[v], distances[u] + w(u, v))`.

Lorsque la destination est sélectionnée, sa distance est définitive ; le chemin
est reconstruit en remontant `previous` à rebours.

### `dijkstra1` — liste des visités

```python
visited = []
...
if node not in visited:      # O(V)
    ...
```

Le test d'appartenance est linéaire. Il est effectué pour chaque candidat de la
recherche du minimum et pour chaque voisin de chaque sommet sélectionné, d'où un
facteur `O(V)` supplémentaire sur les graphes creux. Sur le graphe de test à 400
sommets, cette version est environ **20 fois plus lente** que la version avec
ensemble.

### `dijkstra2` — ensemble des visités

```python
visited = set()
...
if node not in visited:      # O(1)
```

Le test d'appartenance devient de coût constant. La recherche du minimum reste
un parcours linéaire des sommets non visités, donc la complexité totale est
`O(V^2 + E)` : l'algorithme est correct et bien plus rapide sur les graphes
creux, mais reste quadratique.

### `dijkstra_heap` — tas binaire

```python
queue = [(0.0, start)]
...
heapq.heappush(queue, (candidate, neighbour))
```

Un tas renvoie le minimum en `O(log V)`. Le module `heapq` de Python ne propose
pas de diminution de clé (decrease-key), donc une distance améliorée empile une
nouvelle paire et les paires obsolètes sont ignorées lors de leur extraction. Le
coût total est `O((V + E) log V)`, le meilleur des trois pour les grands graphes
creux.

### Temps mesurés

Sur le jeu de données de test à 20 sommets :

| Version | Temps |
|---|---|
| `dijkstra1` (liste) | ≈ 145 µs |
| `dijkstra2` (ensemble) | ≈ 104 µs |
| `dijkstra_heap` | ≈ 72 µs |

Sur un graphe aléatoire à 400 sommets / 900 arêtes (même machine) :

| Version | Temps |
|---|---|
| `dijkstra1` (liste) | ≈ 205 ms |
| `dijkstra2` (ensemble) | ≈ 9,4 ms |
| `dijkstra_heap` | ≈ 1,6 ms |

Les valeurs exactes dépendent de la machine ; les ordres de grandeur et le
classement sont stables. Les trois versions renvoient le même chemin et la même
longueur que `networkx.shortest_path`.

---

## 4. Calculateur d'itinéraires OSMnx

Installer les dépendances facultatives :

```bash
pip install -e ".[routing]"
```

### Charger le réseau

```python
import osmnx as ox
G = ox.graph_from_place("Lyon, France", network_type="drive")
```

Le résultat est un `MultiDiGraph` : une arête est un dictionnaire d'arcs
parallèles, chacun portant des attributs tels que `length`, `highway`, `name`,
`speed_kph` et une géométrie. Par exemple :

```python
G.get_edge_data(u, v)
# {0: {"length": 42.3, "highway": "residential", ...}}
```

`edge_weight` dans `dijkstra.py` gère cette forme imbriquée en lisant
`data[0]["length"]` lorsque c'est nécessaire.

### Afficher et inspecter

- `ox.plot_graph(G, node_size=0, edge_color="yellow")` dessine le réseau ;
- `nodes, edges = ox.graph_to_gdfs(G)` le convertit en GeoDataFrames, qui
  peuvent être explorés de manière interactive ;
- `G.number_of_nodes()` et `G.number_of_edges()` donnent la taille.

### Renuméroter les sommets

Les identifiants OSMnx sont grands et épars. Les renuméroter avant d'utiliser un
algorithme basé sur des tableaux :

```python
mapping = {node: index for index, node in enumerate(G.nodes)}
H = nx.relabel_nodes(G, mapping)
```

### Adresses et sommets les plus proches

Les deux adresses de l'énoncé sont :

- **départ** : 6 Rue Plasson et Chaize ;
- **destination** : 21 Rue Thénard.

Les géocoder, puis trouver les sommets du graphe les plus proches :

```python
lat, lon = ox.geocode("6 Rue Plasson et Chaize, Lyon, France")
origin = ox.distance.nearest_nodes(H, X=lon, Y=lat)
```

`nearest_nodes` attend `X = longitude` et `Y = latitude`.

### Itinéraire et carte

```python
distance, route = dijkstra_heap(H, origin, destination)
ox.plot_graph_route(H, route, route_color="red", node_size=0)
```

`routing.shortest_route` encapsule cet appel ; `routing.plot_route` dessine le
résultat. La longueur de l'itinéraire est en mètres, car OSMnx stocke les
longueurs en mètres.

Le notebook OSMnx contient le code complet. Il n'est pas exécuté dans le dépôt :
le résultat dépend des données OpenStreetMap au moment du téléchargement et
nécessite une connexion Internet.

---

## 5. Ce que le TP démontre

- la différence entre un algorithme **correct** et une implémentation
  **efficace** de celui-ci ;
- pourquoi le choix d'une structure de données (liste, ensemble ou tas) change
  la complexité de plusieurs ordres de grandeur ;
- comment le même code s'exécute sur un graphe synthétique et sur un réseau
  routier réel ;
- comment NetworkX représente les graphes, les attributs et les matrices.

---

## Exécution

```bash
python -m sda.tp08_networkx.demo
python -m pytest tests/test_tp08_dijkstra.py
python -m nbconvert --to notebook --execute --inplace notebooks/tp08_networkx_dijkstra.ipynb
```
