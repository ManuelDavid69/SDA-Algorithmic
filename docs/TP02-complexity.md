# TP 2 — Complexité des algorithmes

## Objectifs

- compter les opérations élémentaires de programmes courts ;
- ordonner des fonctions par croissance asymptotique et les regrouper en classes
  `Theta` ;
- comparer le temps d'exécution d'algorithmes de complexités différentes ;
- vérifier une analyse théorique par des mesures réelles ;
- démontrer une borne `Theta` à partir de la définition.

Le code se trouve dans `src/sda/tp02_complexity` :

| Module | Contenu |
|---|---|
| `counting.py` | les cinq programmes de l'exercice 1, instrumentés avec un compteur d'opérations |
| `growth.py` | les 15 fonctions de l'exercice 2 et leurs classes `Theta` |
| `benchmarks.py` | test de primalité, mesures de temps d'exécution et tables temps/taille |

---

## Exercice 1 — Compter les opérations élémentaires

L'énoncé demande d'ignorer les instructions de contrôle de boucle. On compte une
opération par ligne d'affectation ou d'arithmétique exécutée.

| Programme | Nombre d'opérations `T(n)` | Classe |
|---|---|---|
| 1 | `2n + 1` | `Theta(n)` |
| 2 | `n^2 + 1` | `Theta(n^2)` |
| 3 | `3n^2 + 3n + 3` | `Theta(n^2)` |
| 4 | `2(floor(log2 n) + 1) + 1` | `Theta(log n)` |
| 5 | `3n^2(n^2 + 1) + 1` | `Theta(n^4)` |

Détails :

1. deux boucles indépendantes de `n` itérations, une affectation chacune ;
2. une affectation dans la boucle double, exécutée `n^2` fois ;
3. trois opérations dans la boucle double (`x`, `y`, `z`) et trois dans la
   boucle simple (`w`, `v`, `d`), d'où `3n^2 + 3n` plus les trois affectations
   initiales ;
4. `i` part de `n` et est divisé par deux à chaque itération, donc la boucle
   s'exécute `floor(log2 n) + 1` fois, avec deux opérations par itération ;
5. la boucle la plus interne s'exécute 6 fois pour chaque `j`, et
   `1 + 2 + ... + n^2 = n^2(n^2 + 1)/2`, d'où `6 * n^2(n^2 + 1)/2`.

Les formules explicites sont implémentées sous forme de fonctions
`programX_formula` et vérifiées par rapport aux boucles instrumentées dans la
suite de tests.

---

## Exercice 2 — Ordre de croissance

Du plus lent au plus rapide :

| # | Fonction | Classe `Theta` |
|---|---|---|
| 1 | `6` | `Theta(1)` |
| 2 | `lg lg n` | `Theta(lg lg n)` |
| 3 | `lg n` | `Theta(lg n)` |
| 4 | `(lg n)^2` | `Theta((lg n)^2)` |
| 5 | `sqrt(n)` | `Theta(sqrt(n))` |
| 6 | `n` | `Theta(n)` |
| 7 | `n lg n` | `Theta(n lg n)` |
| 8 | `n^2` | `Theta(n^2)` |
| 9 | `n^3` | `Theta(n^3)` |
| 10 | `n^3 + lg n` | `Theta(n^3)` |
| 11 | `n - n^2 + 5n^3` | `Theta(n^3)` |
| 12 | `(3/2)^n` | `Theta((3/2)^n)` |
| 13 | `2^(n-1)` | `Theta(2^n)` |
| 14 | `2^n` | `Theta(2^n)` |
| 15 | `n!` | `Theta(n!)` |

Justification :

- les constantes disparaissent (`6` est `Theta(1)`) ;
- `lg lg n` croît plus lentement que `lg n`, qui croît plus lentement que
  `(lg n)^2` ;
- toute puissance de `n` domine toute puissance de `lg n`, et
  `sqrt(n) = n^(1/2)` se situe entre `(lg n)^2` et `n` ;
- `n lg n` se situe entre `n` et `n^2` ;
- `n^3 + lg n` et `n - n^2 + 5n^3` sont tous deux `Theta(n^3)` (termes d'ordre
  inférieur) ;
- `2^(n-1) = (1/2) * 2^n`, donc les deux sont `Theta(2^n)` ;
- `(3/2)^n` croît plus lentement que `2^n` car `3/2 < 2` ;
- la formule de Stirling donne `n! = Theta(sqrt(n) * (n/e)^n)`, qui domine toute
  exponentielle `c^n` à constante `c`.

---

## Exercice 3 — Comparer les temps d'exécution

### Question 1

Avec une microseconde par opération élémentaire et `n = 10^6` :

| Complexité | Temps |
|---|---|
| `log n` | `19.9 us` |
| `n` | `1.00 s` |
| `n^2` | `11.57 jours` |
| `2^n` | environ `10^301016` années |

`log2(10^6) ≈ 19.93` ; `(10^6)^2 = 10^12` microsecondes, soit `10^6` secondes ou
environ 11,57 jours. `2^(10^6)` est un nombre de plus de 300 000 chiffres
décimaux : il dépasse de très loin l'âge de l'univers.

### Question 2

Le tableau ci-dessous est généré par `complexity_table()`, avec `10^6`
opérations par seconde (une microseconde par opération).

| Complexité | 1 seconde | 1 minute | 1 heure | 1 jour | 1 mois | 1 an | 1 siècle |
|---|---|---|---|---|---|---|---|
| `lg n` | `2^1,000,000` | `2^60,000,000` | `2^3,600,000,000` | `2^86,400,000,000` | `2^2,592,000,000,000` | `2^31,536,000,000,000` | `2^3,153,600,000,000,000` |
| `sqrt(n)` | 1,000 | 7,745 | 60,000 | 293,938 | 1.610e+06 | 5.616e+06 | 5.616e+07 |
| `n` | 1.000e+06 | 6.000e+07 | 3.600e+09 | 8.640e+10 | 2.592e+12 | 3.154e+13 | 3.154e+15 |
| `n lg n` | 62,746 | 2.801e+06 | 1.334e+08 | 2.755e+09 | 7.187e+10 | 7.976e+11 | 6.861e+13 |
| `n^2` | 1,000 | 7,745 | 60,000 | 293,938 | 1.610e+06 | 5.616e+06 | 5.616e+07 |
| `n^3` | 100 | 391 | 1,532 | 4,420 | 13,736 | 31,593 | 146,645 |
| `2^n` | 19 | 25 | 31 | 36 | 41 | 44 | 51 |
| `n!` | 9 | 11 | 12 | 13 | 15 | 16 | 17 |

La ligne `lg n` est calculée comme `n = 2^(nombre d'opérations)` : le budget
disponible est si grand que seule la valeur symbolique a un sens. Pour
`n lg n`, la valeur est obtenue en résolvant numériquement
`n log2(n) = operations`.

---

## Exercice 4 — Simplifier les expressions `O`

| # | Simplification | Réponse | Peut être remplacé par `Theta` ? |
|---|---|---|---|
| 1 | `11n^3 = O(n^3)` vs `O(n^2)` | faux | non |
| 2 | `n^13 = O(3^n)` | vrai | non |
| 3 | `-2^n = O(log^35 n)` | faux | non |
| 4 | `4n^3 + 12n^2 + 36 = O(n^3)` | vrai | oui |
| 5 | `0.01n^5 = O(n^4)` | faux | non |
| 6 | `4^n = O(n^7)` | faux | non |
| 7 | `3n log2 n = O(n)` | faux | non |
| 8 | `23 ln n = O(3^n)` | vrai | non |
| 9 | `7n^5 = O(n^5)` | vrai | oui |
| 10 | `n^5 = O(7n^5)` | vrai | oui |

Pour un polynôme `P(n)`, seul le terme de plus haut degré compte. Une
exponentielle domine toujours un polynôme, et un polynôme domine toujours un
polylogarithme. Les trois remplacements par `Theta` correspondent aux cas où les
deux membres ont exactement le même taux de croissance (à un facteur constant
près).

---

## Exercice 5 — Complexité d'un test de primalité

`is_prime(n)` effectue des divisions successives de 2 à `floor(sqrt(n))` :

- pire cas : `Theta(sqrt(n))` itérations, chacune en `O(1)` ;
- le temps d'exécution est donc en `O(sqrt(n))`.

Si `n` a `d` chiffres décimaux, alors `n ≈ 10^d` et `sqrt(n) ≈ 10^(d/2)` : le
temps d'exécution croît exponentiellement avec le **nombre de chiffres**,
c'est-à-dire linéairement avec `sqrt(n)`. Sur un axe des temps logarithmique,
les points mesurés sont donc proches d'une droite, ce qui confirme l'analyse.

Les six nombres de l'énoncé comportent jusqu'à 19 chiffres, donc leurs racines
carrées atteignent jusqu'à `10^9` valeurs : mesurer le temps de tous prendrait
des heures. L'utilitaire `measure_prime` accepte n'importe quelle liste, et la
démonstration utilise des instances plus petites tout en conservant le même
comportement asymptotique.

---

## Exercice 6 — Démontrer `3n^2 - 100n + 6 = Theta(n^2)`

Il faut exhiber trois constantes positives `c1`, `c2` et `n0` telles que, pour
tout `n >= n0` :

```
c1 * n^2 <= 3n^2 - 100n + 6 <= c2 * n^2
```

**Borne inférieure.** Pour `n >= 100` :

```
3n^2 - 100n + 6 - 2n^2 = n^2 - 100n + 6 = n(n - 100) + 6 >= 6 > 0
```

donc `3n^2 - 100n + 6 >= 2n^2` avec `c1 = 2` et `n0 = 100`.

**Borne supérieure.** Pour `n >= 3`, `6 <= n^2`, donc :

```
3n^2 - 100n + 6 <= 3n^2 + 6 <= 4n^2
```

avec `c2 = 4` et `n0 = 3`.

En prenant `n0 = 100`, les deux inégalités sont vérifiées, ce qui démontre la
borne `Theta(n^2)`.

---

## Lancer le code

```bash
python -m sda.tp02_complexity.demo
python -m pytest tests/test_tp02_complexity.py
```
