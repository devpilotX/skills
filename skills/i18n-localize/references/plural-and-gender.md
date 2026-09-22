# Plurals and grammatical gender

The English habit of one singular and one plural is a special case, not a universal rule. A template that writes "1 item" or "N items" by checking whether the count equals one is grammatically wrong in most of the world's languages. The ICU message format encodes the real rules, and every major ecosystem has a library that reads it.

## Plural categories

ICU defines up to six plural categories: zero, one, two, few, many, and other. A language uses some subset of them, and the mapping from a number to a category is the language's rule, not yours.

English uses two: one for 1, other for everything else including 0.

Many Slavic languages use one, few, and many, with the category depending on the last digit and the last two digits of the number, so 21 and 22 take different forms than 25.

Arabic uses all six, including distinct forms for zero and for two.

Japanese, Chinese, and Korean use only other, because the noun does not change with number at all.

The point is that you cannot know how many forms a message needs; the locale decides. So the message must be able to carry all six, and the translator fills the ones their language uses.

## A plural message

Write the message so every form is a slot, using the project's ICU capable formatter. The shape, in ICU syntax:

```
{count, plural,
  =0 {No files}
  one {# file}
  other {# files}
}
```

The `=0` is an exact match, useful when zero deserves special wording rather than the grammatical zero category. The `#` is replaced by the formatted number, itself locale aware, so a thousand separator appears correctly. When this message goes to a translator for a language with more categories, their tool exposes the extra slots.

Never build this by hand with an if statement on the count. The if statement encodes English and cannot be translated.

## Ordinals are a separate rule

First, second, third do not follow the plural rule; they follow the ordinal rule, which is different again. ICU has a separate `selectordinal` for them. Do not reuse the plural forms for ordinals.

## Grammatical gender

Many languages change words based on grammatical gender: the gender of the subject, the object, or the person being addressed. A message like "You added a photo" can require different words depending on the gender of the user in some languages. Carry gender as an explicit parameter and let the message select on it:

```
{gender, select,
  female {She added a photo}
  male {He added a photo}
  other {They added a photo}
}
```

Always include an `other` branch, because gender data is often unknown, optional, or non binary, and the message must render correctly without it. Defaulting to a gendered form when the value is missing is both a bug and a slight.

## Do not nest yourself into a corner

A message can combine plural and gender select, and it gets hard to read fast. Keep the combination shallow, and when a sentence needs several interacting variables, split the interface so the translator sees whole, translatable sentences rather than a deeply nested expression they cannot safely edit.
