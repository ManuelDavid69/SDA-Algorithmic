# TP 3 — Récursion et diviser pour régner

## Objectifs

- écrire des fonctions récursives simples (affichages croissant/décroissant) ;
- comparer trois implémentations de Fibonacci (naïve, mémoïsée, récursive terminale) ;
- appliquer diviser pour régner au maximum d'une liste ;
- résoudre les Tours de Hanoï ;
- implémenter la recherche dichotomique, puis l'analyser avec la méthode d'itération et le
  théorème maître.

---

## 1. Affichages récursifs

`numbers_ascending(n)` suit directement la définition :

```python
if n == 0:
    return []
return numbers_ascending(n - 1) + [n]
```

`numbers_descending(n)` place la valeur courante avant l'appel récursif. Les
variantes `print_*` appellent une fonction de sortie configurable, ce qui les rend faciles
à tester. Les deux versions utilisent `O(n)` appels et `O(n)` d'espace total pour le résultat
(ou pour la pile d'appels lors de l'affichage).

---

## 2. Fibonacci

Avec la convention de l'énoncé, `F(0) = F(1) = 1`.

### `fibonacci1` — récursion naïve

```python
if n <= 1:
    return 1
return fibonacci1(n - 1) + fibonacci1(n - 2)
```

La récurrence est `T(n) = T(n-1) + T(n-2) + 1`, donc `T(n) = Theta(phi^n)` avec
`phi = (1 + sqrt(5)) / 2 ≈ 1.618`. L'arbre d'appels contient de nombreux sous-problèmes
identiques : calculer `F(30)` effectue déjà plus d'un million d'appels.

### `fibonacci2` — mémoïsation

Un dictionnaire stocke les valeurs déjà calculées. Chaque indice est calculé une seule fois,
donc la complexité temporelle tombe à `O(n)` et la complexité spatiale est `O(n)`.

### `fibonacci3` — récursion terminale

À partir de `F(k) = a + b`, la paire suivante est `(b, a + b)`. La fonction auxiliaire
transporte les deux accumulateurs et effectue un seul appel récursif :

```python
def fib(k, a, b):
    if k == 0:
        return a
    return fib(k - 1, b, a + b)

return fib(n, 1, 1)
```

Le travail arithmétique est `O(n)` et seuls deux entiers sont transportés, donc l'algorithme
utilise `O(1)` d'état arithmétique supplémentaire. Python n'effectue pas d'optimisation des
appels terminaux, donc la pile d'appels croît tout de même jusqu'à `O(n)` trames ; dans un
langage avec appels terminaux appropriés, la pile serait constante.

### Comportement mesuré

`python -m sda.tp03_recursion.demo` affiche les temps pour `n = 5, 10, 15, 20, 25,
30`. La version naïve croît approximativement d'un facteur `phi` à chaque étape, tandis que
les deux autres restent dans l'ordre de la microseconde.

---

## 3. Maximum par diviser pour régner

`max_list` divise la liste en deux moitiés, calcule récursivement le maximum de chaque moitié
et renvoie le plus grand :

```
T(n) = 2 T(n/2) + O(1)
```

Le théorème maître (cas 1, `a = b = 2`) donne `T(n) = Theta(n)`. C'est le même coût
asymptotique qu'un parcours linéaire, avec une constante plus grande et `O(log n)` trames de
pile ; l'exercice porte sur la méthode, pas sur le fait de battre `max()`.

---

## 4. Tours de Hanoï

```python
solve(n - 1, source, auxiliary, target)
move(source, target)
solve(n - 1, auxiliary, target, source)
```

La récurrence est `T(n) = 2 T(n-1) + 1` avec `T(0) = 0`, d'où `T(n) = 2^n - 1`
déplacements. La suite de tests rejoue les déplacements sur trois piles et vérifie qu'aucun
disque n'est jamais placé sur un disque plus petit.

---

## 5. Recherche séquentielle et dichotomique

### Recherche séquentielle

- meilleur cas : le premier élément correspond, `O(1)` ;
- pire cas : l'élément est absent (ou en dernier), `O(n)` ;
- cas moyen : `O(n)` (environ `n/2` comparaisons).

### Recherche dichotomique

La liste doit être triée. À chaque étape, l'algorithme compare l'élément du milieu avec la
cible et élimine une moitié :

```
T(n) = T(n/2) + O(1)
```

La méthode d'itération donne `T(n) = O(log n)`. Le théorème maître s'applique avec
`a = 1`, `b = 2`, `f(n) = O(1)` : `log_b(a) = 0`, donc le cas 2 donne
`Theta(log n)`. Les versions récursive et itérative sont implémentées ; `dicho` est un alias
de la version récursive, comme dans l'énoncé.

---

## 6. Théorème maître

### 1. Application du théorème

| Récurrence | Paramètres | Cas | Résultat |
|---|---|---|---|
| `T(n) = 8 T(n/2) + 1000 n^3` | `a=8, b=2, log_b a=3` | 2 | `Theta(n^3 log n)` |
| `T(n) = 2 T(n/2) + 10 n` | `a=2, b=2, log_b a=1` | 2 | `Theta(n log n)` |
| `T(n) = 2 T(n/2) + n^2` | `a=2, b=2, log_b a=1` | 3 | `Theta(n^2)` |
| `T(n) = 9 T(n/3) + n^2 log n` | `a=9, b=3, log_b a=2` | cas 2 étendu | `Theta(n^2 log^2 n)` |

Pour la dernière, `f(n) = n^2 log n` est plus grand que `n^2` mais pas polynomialement plus
grand, donc le cas 3 standard ne s'applique pas ; le cas 2 étendu fournit le logarithme
supplémentaire.

### 2. Pourquoi le théorème ne s'applique pas

| Récurrence | Raison |
|---|---|
| `T(n) = 2n T(n/2) + n` | le nombre de sous-problèmes `a = 2n` dépend de `n` ; `a` doit être une constante |
| `T(n) = (1/2) T(n/2) + n` | `a = 1/2 < 1` : le sous-problème est plus petit que l'original d'une manière qui ne définit pas une récurrence de type diviser pour régner |
| `T(n) = 64 T(n/8) - n^2 log n` | le « coût » est négatif ; le théorème exige un `f(n)` positif |
| `T(n) = T(n/2) + n(2 - cos n)` | `f(n)` oscille et ne satisfait pas la condition de régularité `a f(n/b) <= c f(n)` |

### 3. Changement de variable

Pour `T(n) = 2 T(sqrt(n)) + log2 n`, posons `m = log2 n` et
`S(m) = T(2^m)`. Comme `sqrt(n) = 2^(m/2)` :

```
S(m) = 2 S(m/2) + m
```

Le théorème maître donne `S(m) = Theta(m log m)` (cas 2 avec `a = b = 2`).
En revenant à `n` :

```
T(n) = Theta(log n * log log n)
```

---

## Exécution

```bash
python -m sda.tp03_recursion.demo
python -m pytest tests/test_tp03_recursion.py
```
