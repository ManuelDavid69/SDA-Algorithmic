# TP 6 — Tableaux associatifs : tables de hachage et arbres AVL

## Contexte

Vinyl Records Co. souhaite interroger son catalogue de deux manières :

- **requêtes ponctuelles** : le prix du disque de référence
  `9782070360024` ;
- **requêtes par intervalle** : tous les disques publiés entre 1965 et 1975.

Deux index sont construits :

| Index | Structure | Requête |
|---|---|---|
| référence | table de hachage, `m = 1009`, sondage linéaire | clé exacte |
| année | arbre AVL, chaque nœud contient une liste de références | intervalle |

L'implémentation se trouve dans `src/sda/tp06_associative_arrays` :

| Module | Contenu |
|---|---|
| `hash_table.py` | `HashTable` avec sondage linéaire et pierres tombales `DELETED` |
| `avl.py` | `AVLTree` avec les quatre rotations et les requêtes par intervalle |
| `catalogue.py` | `VinylRecord`, `Catalogue` (les deux index) |

---

## Exercice 1 — Tables de hachage

### Question 1 — Insertions

Avec `h(k) = k mod 1009` et le sondage linéaire :

| Référence `k` | `h(k)` | Collision ? | Sondages supplémentaires | Emplacement final |
|---|---|---|---|---|
| 9782010000000 | 335 | non | 0 | 335 |
| 9782210000000 | 391 | non | 0 | 391 |
| 9782210000137 | 528 | non | 0 | 528 |
| 9782010138233 | 335 | oui (335) | 1 | 336 |
| 9782210000274 | 665 | non | 0 | 665 |
| 9782010276466 | 335 | oui (335, 336) | 2 | 337 |

L'énoncé mentionne « les 4 clés » mais son tableau contient six références ;
les six sont traitées ci-dessus et dans la suite de tests.

### Question 2 — Facteur de charge et coût du sondage

Avec 700 éléments dans une table de taille 1009 :

```
alpha = 700 / 1009 = 0.6938
E[sondages] = 1/2 * (1 + 1 / (1 - alpha)^2)
          = 1/2 * (1 + 1 / 0.3062^2)
          = 1/2 * (1 + 10.664)
          = 5.83
```

Une recherche **infructueuse** coûte environ **5,8 sondages** en moyenne.  C'est
élevé pour une recherche infructueuse : à un facteur de charge d'environ 0,7, le sondage
linéaire crée de longs amas, et le coût croît rapidement lorsque `alpha`
s'approche de 1.  Les implémentations pratiques maintiennent `alpha` en dessous de 0,5-0,7,
redimensionnent la table ou utilisent une meilleure stratégie de collision (double hachage,
chaînage).  Les recherches fructueuses sont moins coûteuses (environ
`1/2 * (1 + 1/(1 - alpha)) ≈ 2.13` sondages avec l'approximation usuelle).

### Question 3 — Suppression avec `None`

Contre-exemple avec une table de taille 7 et les clés `1, 8, 15` (toutes de hachage vers
l'emplacement 1) :

```
insérer 1  -> emplacement 1
insérer 8  -> emplacement 2   (collision, un sondage)
insérer 15 -> emplacement 3   (collision, deux sondages)
```

Si `8` est supprimé en écrivant `None` à l'emplacement 2 :

```
emplacement 1 : 1
emplacement 2 : None
emplacement 3 : 15
```

Rechercher `15` commence à l'emplacement 1, voit une clé différente de 15, puis voit
`None` et conclut que 15 est absent.  C'est faux : le `None` a rompu la chaîne de
sondage.

La solution standard est une **pierre tombale** `DELETED` :

- une recherche traite `DELETED` comme « occupé mais non correspondant » et continue à sonder ;
- une insertion peut réutiliser un emplacement `DELETED`, mais seulement après avoir vérifié que la
  clé n'est pas déjà stockée plus loin dans la chaîne ;
- la table est pleine seulement lorsque chaque emplacement contient une vraie clé (une pierre tombale peut
  toujours être réutilisée).

`HashTable` implémente exactement cette stratégie ; `test_hash_deletion_leaves_a_tombstone`
vérifie que `15` reste accessible et que `22` réutilise la pierre tombale.

### Question 4 — Requêtes par intervalle avec la table de hachage

Une table de hachage détruit l'ordre des clés : tous les disques publiés entre 1965 et 1975
peuvent se retrouver n'importe où.  La seule stratégie correcte consiste à **parcourir les
`m` emplacements** et à tester l'année de chaque emplacement occupé :

```
O(m) = O(n)   (avec m proportionnel à n)
```

Un parcours naïf du catalogue est aussi `O(n)`, donc la table de hachage n'apporte aucune
amélioration asymptotique pour cette requête (et ajoute une surcharge de hachage).  L'arbre AVL,
en revanche, maintient les années triées et répond à une requête par intervalle en
`O(log n + k)`, où `k` est le nombre de disques correspondants.

---

## Exercice 2 — Arbres AVL

### Question 1 — Séquence d'insertion

Insérer `66, 72, 69, 58, 80, 75` :

1. `66` devient la racine.
2. `72` va à droite de `66`.
3. `69` va à gauche de `72`.  Le nœud `66` a un facteur d'équilibre de `-2`
   et son enfant droit `72` est lourd à gauche : c'est un cas **RL**.  Une rotation
   à droite sur `72`, puis une rotation à gauche sur `66`, fait de `69` la racine :

   ```
        69
       /  \
     66    72
   ```

4. `58` va à gauche de `66` ; aucune rotation.
5. `80` va à droite de `72` ; aucune rotation.

   ```
        69
       /  \
     66    72
     /       \
    58       80
   ```

6. `75` va à gauche de `80`.  Le nœud `72` a maintenant un facteur d'équilibre de
   `-2`, et son enfant droit `80` est lourd à gauche : encore un cas **RL**.
   Rotation à droite sur `80`, rotation à gauche sur `72` :

   ```
         69
        /  \
      66    75
      /    /  \
     58   72   80
   ```

Les seules rotations sont les deux doubles rotations **RL** (insertions de `69`
et `75`).

### Question 2 — Hauteur et facteurs d'équilibre

L'arbre a **3 niveaux** (2 arêtes sur le plus long chemin, de `69` à `58` ou
à `72`/`80`).

| Nœud | `h(gauche)` | `h(droite)` | Équilibre | Équilibré ? |
|---|---|---|---|---|
| 69 | 2 | 2 | 0 | oui |
| 66 | 1 | 0 | +1 | oui |
| 58 | 0 | 0 | 0 | oui |
| 75 | 1 | 1 | 0 | oui |
| 72 | 0 | 0 | 0 | oui |
| 80 | 0 | 0 | 0 | oui |

Chaque facteur d'équilibre appartient à `{-1, 0, +1}`, donc la condition AVL est satisfaite.

### Question 3 — Requête par intervalle

L'arbre AVL est ordonné par année.  Pour un intervalle `[a, b]`, la requête
récursive :

- va à gauche seulement si `node.key > a` ;
- affiche le nœud si `a <= node.key <= b` ;
- va à droite seulement si `node.key < b`.

Les sous-arbres entièrement sous `a` ou au-dessus de `b` sont élagués.  Le coût est
`O(log n + k)` pour `n` nœuds et `k` années renvoyées (plus le coût de
collecte des références stockées dans chaque nœud).  Une table de hachage ne peut pas faire
cela, car elle n'a aucun ordre à exploiter.

### Question 4 — Comparaison

| Opération | Table de hachage | Arbre AVL | Gagnant |
|---|---|---|---|
| Insertion | `O(1)` en moyenne, `O(n)` au pire | `O(log n)` | table de hachage |
| Recherche par clé exacte | `O(1)` en moyenne, `O(n)` au pire | `O(log n)` | table de hachage |
| Recherche par intervalle | `O(n)` | `O(log n + k)` | arbre AVL |
| Mémoire | `O(m)` emplacements, `m ≈ n` | `O(n)` nœuds + pointeurs | table de hachage (légèrement) |
| Parcours ordonné | `O(n log n)` (collecter puis trier) | `O(n)` infixe | arbre AVL |

La table de hachage est le meilleur **dictionnaire** ; l'arbre AVL est le meilleur
**index ordonné**.  Le catalogue utilise les deux, un par famille de requêtes.

### Exercice 3 — AVL vs arbres rouge-noir

Les deux garantissent des opérations en `O(log n)`, mais :

- un arbre **AVL** est plus strictement équilibré (hauteur au plus environ
  `1.44 log2 n`, contre `2 log2 n` pour un arbre rouge-noir), donc les recherches sont
  légèrement plus rapides ;
- un arbre **rouge-noir** effectue moins de rotations à l'insertion/suppression,
  car sa condition d'équilibre est plus souple, donc les mises à jour sont moins coûteuses ;
- la surcharge mémoire est comparable (un bit de couleur contre un champ de hauteur).

Le catalogue est construit une fois puis principalement lu, ce qui favorise l'arbre AVL.
Un arbre rouge-noir serait préférable pour une charge de travail fortement orientée écriture.

### Exercice 4 — Implémentation

`HashTable` utilise les sentinelles `EMPTY` et `DELETED` et compte les sondages pour
chaque insertion.  `AVLTree` stocke `(year, list of references)` dans chaque nœud,
effectue les rotations LL/RR/LR/RL et conserve la hauteur dans chaque nœud afin que
le facteur d'équilibre soit en `O(1)`.

---

## Exécution

```bash
python -m sda.tp06_associative_arrays.demo
python -m pytest tests/test_tp06_associative.py
```
