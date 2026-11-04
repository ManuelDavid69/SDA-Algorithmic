# TP 4 — Algorithmes de tri

## Objectifs

- implémenter le tri par sélection et prouver son invariant de boucle ;
- analyser le tri fusion avec la méthode d'itération, un arbre de récursion et le
  théorème maître ;
- implémenter le tri aux deux tiers de l'examen 2024 et prouver sa correction ;
- résoudre le problème de la distribution des bonbons, d'abord par force brute puis avec un
  algorithme efficace en `O(n log n)`.

---

## 1. Tri par sélection

```python
for i in range(n):
    minimum = i
    for j in range(i + 1, n):
        if items[j] < items[minimum]:
            minimum = j
    swap(items[i], items[minimum])
```

### Invariant de boucle

Avant l'itération `i` :

- `items[:i]` est trié ;
- `items[:i]` contient les `i` plus petits éléments de la liste entière.

Initialement `i = 0` et le préfixe est vide, donc l'invariant est vrai.  À
l'itération `i`, la boucle interne trouve le plus petit élément de `items[i:]` et
l'échange avec la position `i`.  Le préfixe devient `items[:i+1]`, toujours trié, et
contient les `i+1` plus petits éléments.  À la fin, `i = n` et la liste entière
est triée.

### Complexité

La boucle interne effectue `n - 1 - i` comparaisons, donc le total est

```
(n-1) + (n-2) + ... + 1 = n(n-1)/2 = Theta(n^2)
```

dans le meilleur cas, le pire cas et le cas moyen.  Le nombre d'échanges
est au plus `n - 1`, mais cela ne change pas le coût asymptotique.

---

## 2. Tri fusion

### Récurrence

```
T(1) = Theta(1)
T(n) = 2 T(n/2) + Theta(n)   pour n > 1
```

Le terme `Theta(n)` est la fusion des deux moitiés triées.

### Méthode d'itération

```
T(n) = 2 T(n/2) + n
     = 4 T(n/4) + 2n
     = 8 T(n/8) + 3n
     ...
     = 2^k T(n/2^k) + kn
```

Avec `k = log2 n`, `T(n) = n T(1) + n log2 n = Theta(n log n)`.

### Arbre de récursion

Chaque niveau contient un travail total `n` (les fusions partitionnent l'entrée), et
l'arbre a `log2 n + 1` niveaux, d'où `Theta(n log n)`.

### Théorème maître

`a = 2`, `b = 2`, `log_b a = 1`, et `f(n) = Theta(n)`.  C'est le cas 2, donc
`T(n) = Theta(n log n)`.  Les trois méthodes concordent.

---

## 3. Tri aux deux tiers (examen 2024)

```
trier(les deux premiers tiers)
trier(les deux derniers tiers)
trier(les deux premiers tiers)
```

Soit `k = ceil(2n/3)`, `A = items[0:k]` (les deux premiers tiers) et
`B = items[n-k:n]` (les deux derniers tiers).  Leur chevauchement est
`O = items[n-k:k]` ; le préfixe `A \ B` correspond aux `n-k` premiers éléments et le
suffixe `B \ A` aux `n-k` derniers éléments.

### Correction

1. Après le premier tri, `A` est trié ; en particulier, tout élément de
   `A \ B` est inférieur ou égal à tout élément de `O`.
2. Pendant le second tri, `B` est trié.  Comme `O` est un préfixe de `B`, les
   `|O|` plus petits éléments de `B` se retrouvent dans `O`, donc tout élément de `O` est
   inférieur ou égal à tout élément de `B \ A`.
3. Par conséquent `A \ B <= O <= B \ A`, et `A` et `B` sont tous deux triés
   intérieurement.
4. Le troisième tri trie `A` de nouveau.  Cela rétablit l'ordre à l'intérieur du
   chevauchement `O` tout en préservant la séparation entre `A \ B`, `O` et `B \ A`.
   Le tableau entier est trié.

Le cas de base `n <= 2` trie directement les deux éléments.  Ce cas de base est
nécessaire : pour `n = 2`, les « deux premiers tiers » représentent le tableau entier et la
récursion ne diminuerait pas.

### Récurrence et complexité

Les trois appels récursifs ont une taille `ceil(2n/3)` et le travail hors des
appels est `Theta(1)` :

```
T(n) = 3 T(2n/3) + Theta(1)
```

Avec `a = 3`, `b = 3/2`, `log_b a = ln 3 / ln 1.5 ≈ 2.7095`.  Comme
`f(n) = Theta(1) = O(n^(2.7095 - epsilon))`, le cas 1 du théorème maître
donne :

```
T(n) = Theta(n^(log_(3/2)(3))) = Theta(n^2.71)
```

C'est **pire** que le tri par insertion (`Theta(n^2)`) et bien pire que le tri
fusion (`Theta(n log n)`).  L'algorithme est intéressant comme exercice, pas comme
méthode de tri pratique.

---

## 4. Distribution des bonbons

### Question 1 — force brute

Énumérer tous les sous-ensembles de `m` paquets parmi `n`, évaluer leur étendue
`max - min`, et garder le meilleur.  Il y a `C(n, m)` sous-ensembles et chaque
évaluation coûte `O(m)`, donc la complexité est `O(C(n, m) * m)`, ce qui est
exponentiel en `n`.

### Question 2 — algorithme efficace

1. trier les paquets : `O(n log n)` ;
2. faire glisser une fenêtre d'exactement `m` paquets consécutifs sur la liste triée et
   garder la fenêtre dont `last - first` est le plus petit : `O(n)`.

Pourquoi une fenêtre consécutive suffit-elle ?  Prenons un sous-ensemble optimal, soit `a`
son plus petit élément et `b` son plus grand.  Dans la liste triée, la fenêtre qui
commence à `a` et contient `m` paquets consécutifs se termine à un élément `b' <=
b`, donc son étendue est au plus `b - a`.  Remplacer le sous-ensemble optimal par cette
fenêtre ne peut donc pas augmenter la différence.  Une solution optimale est ainsi une
fenêtre consécutive.

Complexité totale : `O(n log n)` en temps, `O(n)` d'espace supplémentaire pour la copie triée.

La suite de tests compare le résultat efficace avec le résultat par force brute sur de
petites instances aléatoires.

---

## Exécution

```bash
python -m sda.tp04_sorting.demo
python -m pytest tests/test_tp04_sorting.py
```
