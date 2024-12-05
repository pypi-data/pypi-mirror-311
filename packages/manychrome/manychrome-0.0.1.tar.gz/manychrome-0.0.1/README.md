# Manychrome

This is a package predominantly created for those who prefer working from the CLI. It is to add colours and to style text so to easily make warnings, notification messages, or finding text when searching for it easily pop out.

# Installation
pip install manychrome

To uninstall use: pip uninstall manychrome

# Usage
import manychrome

## Classes to import
* Colorful()
* Styleish()
* FindMe()


## Colorful()
See below for the current functions and config for class Colorful()

### Functions:
write(words)
styleme(words)
choose_color()
save_favs()

### Config:
c = Colorful(fg=1, bg=2, it=True)  --All config can be set inside here, or as shown below.
c.fg = 1
c.bg = 2
c.it = True
c.ul = False
c.bo = False
c.st = False
c.sh = False
c.ft = False  --not sure if this one is working totally properly yet
Can set the style straight when calling the class, or set it like displayed above.


## FindMe()
See below for the current functions and config for class FindMe()

### Functions
showme(document)
listme(TBC)
listmepretty(TBC)



### Config
styled = FindMe(
    key1=value1,
    key2=value2,
    key3=value3
)
styled.fg = 207
styled.bo = True
styled.it = True
etc etc... Has all the same fg, bg, it, bo, ul etc etc.

for the key=values:
use {key} in the text document, and for value simply write what you want it to be.
For example:
document = "Here is a {sample} that serves as an {example} to {show} how this works."
styled = FindMe(
    sample="sweet story"
    example="eternal uplifter"
    show="literally display"
)
styled.fg = 208
styled.bo = True
styled.ul = True
styled.showme(document)



## Styleish()
See below for the current functions and config for class Styleish()

### Functions
findme()
highlight(words)
italics(words)
underline(words)
strikethrough(words)
swap(words)
bold(words)

### Config
For styleish, set config
s = Styleish()
s.fg = 117
s.bg = 218
Can do s.it = True etc but the functions below aren't affected by that so they can be used in combination with each others.


## Combinations
Combine Findme() and Colorful()
For example:

```python
dogs = ["Max", "Bobby", "Dracula", "Leopold"]
c = Colorful(fg=204, it=True)
d = FindMe()
d.listme([c.styleme(dog) for dog in dogs])
```
