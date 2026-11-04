# TP 1 — Listes chaînées et piles

## Objectifs

Réimplémenter deux structures linéaires fondamentales sans utiliser `list` de
Python :

- une **liste simplement chaînée** (`Node` + `LinkedList`) ;
- une **pile LIFO** (`Stack`), construite sur la même représentation de nœud.

La séance introduit aussi une petite simulation (un train) et une application
classique des piles : vérifier qu'un texte est correctement parenthésé.

---

## 1. `LinkedList`

| Opération | Signification | Complexité |
|---|---|---|
| `insert(value, k)` | insérer à la position `k` (`0 <= k <= size`) | `O(k)` |
| `delete(k)` | retirer et renvoyer l'élément en `k` | `O(k)` |
| `search(value)` | indice de la première occurrence, ou `-1` | `O(n)` |
| `get(k)` | valeur à la position `k` | `O(k)` |
| `append(value)` | ajouter à la fin | `O(n)` |
| `size` / `is_empty()` | longueur actuelle / test de vacuité | `O(1)` |
| `__repr__` | `1 -> 2 -> 3 -> None` | `O(n)` |

Choix d'implémentation :

- un `Node` est une dataclass avec un `value` et un pointeur `next` ;
- la liste conserve un pointeur `head` et un `_size` mis en cache, de sorte que
  `len()` est en `O(1)` tandis que les autres opérations parcourent la chaîne ;
- les positions sont indexées à partir de 0, et les indices hors bornes lèvent
  une `IndexError` au lieu de renvoyer silencieusement `None` ;
- `__iter__` rend la liste utilisable dans les boucles `for`, `list(...)` et les
  tests.

`append` est délibérément en `O(n)` : la liste du cours ne stocke qu'un pointeur
de tête. Conserver un pointeur de queue la rendrait `O(1)` mais compliquerait la
suppression du dernier élément ; la variante simple suffit pour cette séance.

---

## 2. Simulation de train

Chaque wagon contient au plus **4 passagers**. `Train.board(passenger, k)`
commence au wagon `k` et progresse vers la fin du train :

- si le wagon est plein, le passager essaie le suivant ;
- si le dernier wagon est plein, l'embarquement échoue et `None` est renvoyé.

La question 4 est implémentée avec l'argument optionnel `search_backwards=True` :
lorsqu'aucune place n'est trouvée après le wagon `k`, la recherche repart de
l'avant du train et s'arrête avant `k`. C'est le comportement de « rebrousser
chemin » de l'énoncé.

`Train.alight(k)` retire le dernier passager entré dans le wagon `k` et renvoie
son nom. `repr(train)` affiche chaque wagon, son taux d'occupation et ses
passagers.

---

## 3. Pile et analyse de parenthèses

`Stack` est une pile chaînée : `push`, `pop`, `peek`, `is_empty` et `size` sont
toutes en `O(1)`. Dépiler ou consulter le sommet d'une pile vide lève une
`IndexError`.

`analyse(expression)` parcourt la chaîne une seule fois et renvoie un booléen :

1. une parenthèse ouvrante `(`, `[`, `{` ou `<` est empilée ;
2. une parenthèse fermante doit correspondre au sommet de la pile, sinon la
   réponse est `False` ;
3. l'expression n'est valide que si la pile est vide à la fin.

Tout autre caractère est ignoré, comme l'exige l'énoncé. Le parcours est en
`O(n)` en temps et en `O(d)` en espace, où `d` est la profondeur d'imbrication
maximale.

### Localiser la première erreur

`analyse_text(text)` renvoie un `BracketReport` avec une `line` et une `column`
indexées à partir de 1 :

- une parenthèse fermante inattendue est signalée à sa propre position ;
- une parenthèse fermante non appariée signale la position de la parenthèse
  ouvrante qu'elle aurait dû fermer ;
- une parenthèse ouvrante restée à la fin du fichier est signalée à sa propre
  position.

`analyse_file(path)` applique la même analyse à un fichier texte UTF-8, ce qui
couvre les deux fichiers HTML de l'énoncé.

---

## Lancer le code

```bash
python -m sda.tp01_data_structures.demo
python -m pytest tests/test_tp01_linked_list.py tests/test_tp01_train.py tests/test_tp01_stack.py
```
