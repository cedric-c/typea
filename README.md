# typea

TypeA is a file renaming tool used by [Type-A personalities][1] to rename PDFs, typically research articles. These research articles often have long names with little meaning. TypeA reads extended file attributes (xattrs) and copies the file to an `out` directory using the format `author_title.pdf`.

## For Geeks

TypeA uses `mdls` to retrieve the extended file attributes. As such, it is not currently available on Windows. I plan to support Windows in future releases (as well as a more robust solution).

## Instructions

Soon...

## Screenshots

![sample1](screenshots/sample1.png)

## Todo

1. Support for multiple parameters.
2. Compiled version, placed in bin for easier calls
3. PDF parsing for articles which don't have the needed xattrs.
4. GUI.
5. Tutorial and instructions.
6. Support for other environments.

If you like this I expect to be referenced in your PhD dissertation! :-)

[1]: https://en.wikipedia.org/wiki/Type_A_and_Type_B_personality_theory
