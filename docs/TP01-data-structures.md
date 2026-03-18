# TP 1 — Linked lists and stacks

## Objectives

Re-implement two fundamental linear structures without Python's `list`:

- a **singly linked list** (`Node` + `LinkedList`);
- a **LIFO stack** (`Stack`), built on the same node representation.

The session also introduces a small simulation (a train) and a classic stack
application: checking that a text is correctly parenthesised.

---

## 1. `LinkedList`

| Operation | Meaning | Complexity |
|---|---|---|
| `insert(value, k)` | insert at position `k` (`0 <= k <= size`) | `O(k)` |
| `delete(k)` | remove and return the element at `k` | `O(k)` |
| `search(value)` | index of the first occurrence, or `-1` | `O(n)` |
| `get(k)` | value at position `k` | `O(k)` |
| `append(value)` | add at the end | `O(n)` |
| `size` / `is_empty()` | current length / emptiness | `O(1)` |
| `__repr__` | `1 -> 2 -> 3 -> None` | `O(n)` |

Implementation choices:

- a `Node` is a dataclass with a `value` and a `next` pointer;
- the list keeps a `head` pointer and a cached `_size`, so `len()` is `O(1)`
  while the other operations walk the chain;
- positions are 0-based, and out-of-range indexes raise `IndexError` instead
  of silently returning `None`;
- `__iter__` makes the list usable in `for` loops, `list(...)` and tests.

`append` is deliberately `O(n)`: the course list only stores a head pointer.
Keeping a tail pointer would make it `O(1)` but would complicate deletion of
the last element; the simple variant is enough for this session.

---

## 2. Train simulation

Each wagon holds at most **4 passengers**. `Train.board(passenger, k)` starts
at wagon `k` and goes towards the end of the train:

- if the wagon is full, the passenger tries the next one;
- if the last wagon is full, boarding fails and `None` is returned.

Question 4 is implemented with the optional `search_backwards=True` argument:
when no room is found after wagon `k`, the search restarts at the front of the
train and stops before `k`. This is the "rebrousser chemin" behaviour of the
statement.

`Train.alight(k)` removes the last passenger who entered wagon `k` and returns
their name. `repr(train)` prints every wagon, its occupancy and its passengers.

---

## 3. Stack and bracket analysis

`Stack` is a linked stack: `push`, `pop`, `peek`, `is_empty` and `size` are all
`O(1)`. Popping or peeking an empty stack raises `IndexError`.

`analyse(expression)` scans the string once and returns a boolean:

1. an opening bracket `(`, `[`, `{` or `<` is pushed;
2. a closing bracket must match the top of the stack, otherwise the answer is
   `False`;
3. the expression is valid only if the stack is empty at the end.

Every other character is ignored, as required by the statement. The scan is
`O(n)` in time and `O(d)` in space, where `d` is the maximum nesting depth.

### Locating the first error

`analyse_text(text)` returns a `BracketReport` with a 1-based `line` and
`column`:

- an unexpected closing bracket is reported at its own position;
- a mismatched closing bracket reports the position of the opening bracket it
  should have closed;
- an opening bracket left at the end of the file is reported at its own
  position.

`analyse_file(path)` applies the same analysis to a UTF-8 text file, which
covers the two HTML files of the statement.

---

## Run it

```bash
python -m sda.tp01_data_structures.demo
python -m pytest tests/test_tp01_linked_list.py tests/test_tp01_train.py tests/test_tp01_stack.py
```
