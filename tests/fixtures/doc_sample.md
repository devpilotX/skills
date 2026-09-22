---
title: Converter test
version: 1
---

# Converter test

Intro paragraph with **bold**, *italic*, ~~strike~~, `inline code`, a [link](https://example.com)
and a bare URL https://example.org/page.

## Lists

- first item
- second item
  - nested item
- third item

1. step one
2. step two

## Table

| Field | Type | Notes |
|-------|------|-------|
| id    | int  | primary key |
| name  | text | may be `null` |

## Code

```python
def f(x):
    return x < 3 and x > 1  # needs escaping: <, >, &
```

> A quoted line.
> Continued on the next line.

## Escaping

Raw HTML like <script>alert(1)</script> must not execute, and 5 < 6 & 7 > 2.
