# TP 5 — Trees

## Objectives

- build a **binary search tree** (BST) with chained nodes, and implement
  insertion, search and deletion;
- render a tree as ASCII to check the operations;
- use **expression trees** to represent and evaluate arithmetic expressions,
  including reverse Polish notation (RPN);
- parse nested **ternary expressions** (`a?b:c`);
- implement a simplified **Akinator** that learns new animals.

The code lives in `src/sda/tp05_trees`:

| Module | Contents |
|---|---|
| `bst.py` | `BSTNode`, `BST` (insert, search, delete, traversals, height) |
| `tree_printer.py` | ASCII rendering of a binary tree |
| `expression_tree.py` | RPN parser, infix/postfix traversals, evaluator |
| `ternary.py` | recursive-descent parser for `a?b:c` expressions |
| `akinator.py` | question/animal tree, interactive game, JSON persistence |

---

## 1. Binary search tree

### Insertion sequence

Inserting `25, 60, 35, 10, 5, 20, 65, 45, 70, 40, 50, 55, 30, 15` gives:

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

The in-order traversal is the sorted sequence, which is the defining property
of a BST.

### Deletion

- deleting **35** (two children): its in-order successor is **40**, the
  minimum of its right subtree. `40` replaces `35` and is removed from its old
  position;
- deleting **25** (two children): its successor is **30**. `30` becomes the
  new root.

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

The three deletion cases are implemented in `BST._delete`:

1. a leaf is replaced by `None`;
2. a node with one child is replaced by that child;
3. a node with two children is replaced by its successor.

### Complexity

| Operation | Complexity |
|---|---|
| `insert`, `search`, `delete` | `O(h)`, where `h` is the height |
| in-order / pre-order / post-order | `O(n)` |
| `height`, `len` | `O(n)` / `O(1)` |

In the worst case (sorted insertions) `h = n - 1` and the operations are
`O(n)`.  For a randomly built BST the expected height is `O(log n)`, which is
why balanced variants (AVL, red-black) exist; the AVL tree is implemented in
TP 6.

The test suite replays the insertion and deletion sequence of the statement
and checks the BST invariant after each deletion.

---

## 2. Expression trees and RPN

### Building the tree

The formula `((5 + z) / -8) * (4 ^ 2)` becomes:

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

The division node has the constant `-8` as its right child.  There are two
valid representations of `-8`:

- a **leaf** whose value is the negative constant `-8` (the simplest choice,
  and the one used by `build_from_rpn` when it reads the token `-8`);
- a **unary minus node** with the positive leaf `8` as its only child, written
  `8 neg` in RPN.  This is necessary when the minus sign is an operator
  applied to a sub-expression rather than part of a literal.

`build_from_rpn` supports both forms.

### Infix traversal

A plain in-order traversal writes:

```
5 + z / -8 * 4 ^ 2
```

which is **not** the original formula: without parentheses, the usual
precedence rules give a different tree.  Parentheses are needed to preserve
the structure.  `to_infix` therefore adds a pair of parentheses around every
binary operation and around the unary minus:

```
(((5 + z) / (-8)) * (4 ^ 2))
```

A precedence-aware printer can omit some of them, but the fully parenthesised
form is always correct and is the simplest answer to the question.

### Which traversal gives RPN?

The **post-order** traversal (left, right, root) gives the reverse Polish
notation: operands first, then the operator.  For the example:

```
5 z + 8 neg / 4 2 ^ *
```

The test `to_postfix(build_from_rpn(tokens)) == tokens` checks the round trip.

### Evaluating RPN

Evaluating the post-order traversal with a stack gives the result directly:

- a number is pushed;
- a binary operator pops two values, applies the operation and pushes the
  result;
- `neg` pops one value and pushes its opposite.

At the end, the stack contains exactly one value: the result.  This is what
`evaluate_rpn` does; `build_from_rpn` + `evaluate` performs the same
computation through the tree.  Both return `-16` for `z = 3`.

---

## 3. Nested ternary expressions

The grammar is right-associative:

```
expression := atom ('?' expression ':' expression)?
atom       := identifier
```

With `a?b:c`, the root is the condition `a`, the left child is `b` and the
right child is `c`.

With `a?b?c:d:e`, the parser attaches the inner ternary to the **then** branch:

```
        a
      /   \
     b     e
   /   \
  c     d
```

`to_ternary(tree, parenthesize=True)` prints `(a?(b?c:d):e)`, which makes the
structure explicit.  `evaluate_ternary` resolves the conditions from a
dictionary and follows the corresponding branch; a leaf that is not a known
condition is the result of the expression (for example `c`).

---

## 4. Akinator

The game stores a binary tree:

- an **internal node** contains a yes/no question;
- a **leaf** contains an animal name.

The program starts with a single animal (`oiseau`) and asks
`Est-ce un oiseau ?`.

- If the answer is yes, the program has found the animal.
- If the answer is no, it asks for the name of the new animal, a question that
  distinguishes it from the old one, and the answer that the new animal would
  give to that question.  The leaf is replaced by a new question node whose
  two children are the new animal and the old one.

For example, after learning `chat` with the question
`A-t-il des moustaches ?` and the answer `oui`, the tree becomes:

```
A-t-il des moustaches ?
        /       \
     chat      oiseau
```

The tree can be saved to and loaded from JSON, so the program keeps what it
learned between sessions.  The `play` method accepts injected input/output
functions, which makes the whole game testable without a terminal.

---

## Run it

```bash
python -m sda.tp05_trees.demo
python -m pytest tests/test_tp05_trees.py
```
