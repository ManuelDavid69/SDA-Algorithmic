# TP 5 — Arbres

## Objectifs

- construire un **arbre binaire de recherche** (ABR) avec des nœuds chaînés, et implémenter
  l'insertion, la recherche et la suppression ;
- afficher un arbre en ASCII pour vérifier les opérations ;
- utiliser des **arbres d'expression** pour représenter et évaluer des expressions
  arithmétiques, y compris la notation polonaise inverse (RPN) ;
- analyser des **expressions ternaires** imbriquées (`a?b:c`) ;
- implémenter un **Akinator** simplifié qui apprend de nouveaux animaux.

Le code se trouve dans `src/sda/tp05_trees` :

| Module | Contenu |
|---|---|
| `bst.py` | `BSTNode`, `BST` (insertion, recherche, suppression, parcours, hauteur) |
| `tree_printer.py` | rendu ASCII d'un arbre binaire |
| `expression_tree.py` | analyseur RPN, parcours infixe/postfixe, évaluateur |
| `ternary.py` | analyseur descendant récursif pour les expressions `a?b:c` |
| `akinator.py` | arbre question/animal, jeu interactif, persistance JSON |

---

## 1. Arbre binaire de recherche

### Séquence d'insertion

Insérer `25, 60, 35, 10, 5, 20, 65, 45, 70, 40, 50, 55, 30, 15` donne :

```
25
|-- 10
|   |-- 5
|   `-- 20
|       `-- 15
`-- 60
    |-- 35
    |   |-- 30
    |   `-- 45
    |       |-- 40
    |       `-- 50
    |           `-- 55
    `-- 65
        `-- 70
```

Le parcours infixe est la séquence triée, ce qui est la propriété caractéristique
d'un ABR.

### Suppression

- supprimer **35** (deux enfants) : son successeur infixe est **40**, le
  minimum de son sous-arbre droit. `40` remplace `35` et est retiré de son ancienne
  position ;
- supprimer **25** (deux enfants) : son successeur est **30**. `30` devient la
  nouvelle racine.

```
30
|-- 10
|   |-- 5
|   `-- 20
|       `-- 15
`-- 60
    |-- 40
    |   `-- 45
    |       `-- 50
    |           `-- 55
    `-- 65
        `-- 70
```

Les trois cas de suppression sont implémentés dans `BST._delete` :

1. une feuille est remplacée par `None` ;
2. un nœud avec un seul enfant est remplacé par cet enfant ;
3. un nœud avec deux enfants est remplacé par son successeur.

### Complexité

| Opération | Complexité |
|---|---|
| `insert`, `search`, `delete` | `O(h)`, où `h` est la hauteur |
| infixe / préfixe / postfixe | `O(n)` |
| `height`, `len` | `O(n)` / `O(1)` |

Dans le pire cas (insertions triées) `h = n - 1` et les opérations sont
`O(n)`.  Pour un ABR construit aléatoirement, la hauteur attendue est `O(log n)`, ce qui
explique l'existence de variantes équilibrées (AVL, rouge-noir) ; l'arbre AVL est implémenté
au TP 6.

La suite de tests rejoue la séquence d'insertion et de suppression de l'énoncé
et vérifie l'invariant d'ABR après chaque suppression.

---

## 2. Arbres d'expression et RPN

### Construction de l'arbre

La formule `((5 + z) / -8) * (4 ^ 2)` devient :

```
          *
        /   \
       /     ^
      /     / \
     /     4   2
    +
   / \
  5   z
```

Le nœud de division a la constante `-8` comme enfant droit.  Il existe deux
représentations valides de `-8` :

- une **feuille** dont la valeur est la constante négative `-8` (le choix le plus simple,
  et celui utilisé par `build_from_rpn` lorsqu'il lit le jeton `-8`) ;
- un **nœud de moins unaire** avec la feuille positive `8` comme unique enfant, noté
  `8 neg` en RPN.  Cela est nécessaire lorsque le signe moins est un opérateur
  appliqué à une sous-expression plutôt que faisant partie d'un littéral.

`build_from_rpn` prend en charge les deux formes.

### Parcours infixe

Un simple parcours infixe écrit :

```
5 + z / -8 * 4 ^ 2
```

ce qui n'est **pas** la formule d'origine : sans parenthèses, les règles de priorité
usuelles donnent un arbre différent.  Les parenthèses sont nécessaires pour préserver
la structure.  `to_infix` ajoute donc une paire de parenthèses autour de chaque
opération binaire et autour du moins unaire :

```
(((5 + z) / (-8)) * (4 ^ 2))
```

Un afficheur tenant compte des priorités peut en omettre certaines, mais la forme
entièrement parenthésée est toujours correcte et constitue la réponse la plus simple
à la question.

### Quel parcours donne la RPN ?

Le parcours **postfixe** (gauche, droite, racine) donne la notation polonaise
inverse : d'abord les opérandes, puis l'opérateur.  Pour l'exemple :

```
5 z + 8 neg / 4 2 ^ *
```

Le test `to_postfix(build_from_rpn(tokens)) == tokens` vérifie l'aller-retour.

### Évaluation de la RPN

Évaluer le parcours postfixe avec une pile donne directement le résultat :

- un nombre est empilé ;
- un opérateur binaire dépile deux valeurs, applique l'opération et empile le
  résultat ;
- `neg` dépile une valeur et empile son opposé.

À la fin, la pile contient exactement une valeur : le résultat.  C'est ce que fait
`evaluate_rpn` ; `build_from_rpn` + `evaluate` effectue le même calcul à travers
l'arbre.  Les deux renvoient `-16` pour `z = 3`.

---

## 3. Expressions ternaires imbriquées

La grammaire est associée à droite :

```
expression := atom ('?' expression ':' expression)?
atom       := identifier
```

Avec `a?b:c`, la racine est la condition `a`, l'enfant gauche est `b` et
l'enfant droit est `c`.

Avec `a?b?c:d:e`, l'analyseur attache le ternaire interne à la branche **alors** :

```
        a
      /   \
     b     e
   /   \
  c     d
```

`to_ternary(tree, parenthesize=True)` affiche `(a?(b?c:d):e)`, ce qui rend la
structure explicite.  `evaluate_ternary` résout les conditions à partir d'un
dictionnaire et suit la branche correspondante ; une feuille qui n'est pas une condition
connue est le résultat de l'expression (par exemple `c`).

---

## 4. Akinator

Le jeu stocke un arbre binaire :

- un **nœud interne** contient une question oui/non ;
- une **feuille** contient un nom d'animal.

Le programme commence avec un seul animal (`oiseau`) et demande
`Est-ce un oiseau ?`.

- Si la réponse est oui, le programme a trouvé l'animal.
- Si la réponse est non, il demande le nom du nouvel animal, une question qui
  le distingue de l'ancien, et la réponse que le nouvel animal donnerait
  à cette question.  La feuille est remplacée par un nouveau nœud question dont
  les deux enfants sont le nouvel animal et l'ancien.

Par exemple, après avoir appris `chat` avec la question
`A-t-il des moustaches ?` et la réponse `oui`, l'arbre devient :

```
A-t-il des moustaches ?
        /       \
     chat      oiseau
```

L'arbre peut être sauvegardé dans un fichier JSON et chargé depuis celui-ci, de sorte que
le programme conserve ce qu'il a appris entre les sessions.  La méthode `play` accepte des
fonctions d'entrée/sortie injectées, ce qui rend tout le jeu testable sans terminal.

---

## Exécution

```bash
python -m sda.tp05_trees.demo
python -m pytest tests/test_tp05_trees.py
```
