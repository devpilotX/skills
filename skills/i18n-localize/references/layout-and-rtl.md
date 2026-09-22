# Layout expansion and right to left

Translated text does not keep the size or the direction of the source. A layout that fits English and hardcodes left alignment breaks the first time it meets German or Arabic. Design for expansion and for direction from the start, because retrofitting either into a fixed layout is expensive.

## Text expansion

The same meaning takes different room in different languages. As a rule of thumb, translations from English run longer, and the shorter the source string the larger the proportional growth. A single word button label can double or more; a paragraph grows less in proportion.

A working budget to design against, treating these as rules of thumb rather than measured limits:

```
source length     allow for expansion
1 to 10 chars     up to 200 percent
11 to 20 chars    up to 100 percent
21 to 50 chars    up to 80 percent
over 50 chars     up to 40 percent
```

The practical consequences: do not size a button or a column to the English text, do not truncate with an ellipsis where the full text carries meaning, and do not place text in a fixed width box that cannot grow or wrap. Let containers size to content and let content wrap.

## Right to left

Arabic, Hebrew, Persian, and Urdu are written right to left. Supporting them is not translating the words; it is mirroring the layout. The whole interface flips: text aligns right, the reading order reverses, navigation moves, and directional icons like a back arrow point the other way.

Do this with the framework's direction support, not by hand. Set the document or component direction to right to left for those locales and use logical properties, so that start and end replace left and right and the layout mirrors automatically. Hand coding left and right values guarantees a broken mirror.

What does not flip: things with an inherent direction. A phone number, a numeric progress bar in some cases, a logo, and code samples stay as they are. Numbers themselves are written left to right even inside right to left text, which the bidirectional algorithm handles if you do not fight it.

## Bidirectional text

When left to right content sits inside right to left text, such as a Latin brand name or a URL in an Arabic sentence, the Unicode bidirectional algorithm decides the visual order. Usually it gets it right. Where it does not, isolate the embedded run with the proper Unicode isolation controls so a stray piece of punctuation does not jump to the wrong end of the line. Do not concatenate strings of mixed direction and hope; wrap the foreign run explicitly.

## Icons, images, and cultural meaning

Some icons carry direction: arrows, the send and reply symbols, progress and back and forward. Mirror these for right to left. Some images and colours carry cultural meaning that does not transfer, so a hand gesture or a colour that is positive in one culture can be rude in another. Flag anything culturally loaded for review by someone from the target region rather than deciding alone.

## Test before a human sees it

Every layout claim here is checkable with the pseudo locale from the main procedure: a pseudo locale that pads strings to the expansion budget and one that forces right to left will expose the fixed widths, the truncations, and the unmirrored components before a translator or a user finds them.
