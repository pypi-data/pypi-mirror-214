# ReBNF

<div>
  <a href="#"><img src="https://img.shields.io/badge/%F0%9F%94%96%20Version-0.7-ec3832.svg?color=ec3832&style=flat"/></a>
  <a href="https://opsocket.com" style="text-decoration: none;">
    <img alt="opsocket" height="42" src="https://gitlab.com/opsocket/rebnf/-/raw/main/docs/assets/imgs/logo.svg" loading="lazy" />
  </a>
</div>


**ReBNF** (*Regexes for Extended Backus-Naur Form*) is a notation used to define the
syntax of a language using regular expressions.

It is an extension of the EBNF (Extended Backus-Naur Form) notation, allowing
for more flexibility and ease of use.

```
ooooooooo.             oooooooooo.  ooooo      ooo oooooooooooo 
`888   `Y88.           `888'   `Y8b `888b.     `8' `888'     `8 
 888   .d88'  .ooooo.   888     888  8 `88b.    8   888         
 888ooo88P'  d88' `88b  888oooo888'  8   `88b.  8   888oooo8    
 888`88b.    888ooo888  888    `88b  8     `88b.8   888    "    
 888  `88b.  888    .o  888    .88P  8       `888   888         
o888o  o888o `Y8bod8P' o888bood8P'  o8o        `8  o888o       
```

## Table of Contents

- [Syntax](#syntax)
- [Example](#example)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Syntax

The **ReBNF** notation uses regular expressions to define the structure of a
language. Each *rule* consists of a *left-hand side* (non-terminal) and a
*right-hand side* separated by an **assignment operator** (either `::=`, `:=` or `=`).

The general syntax of a **ReBNF** rule is as follows:

```
<alnum> ::= r"[a-zA-Z0-9]" ; # any alphanumeric character
```

The alphanumeric set is composed of all letters and all digits, which sums up
36 characters. 

The **EBNF** syntax requires *quotes* and `|` operators in between characters to
define the `alnum` identifier as matching any alphanumeric character, which sums up to 143 characters.

Using **ReBNF**, a single regex is required such as `r"[a-zA-Z0-9]"`, which sums up to 14 characters.

### Identifiers

 The enclosures `<` and `>` are optional, such as:

```
alnum = r"[a-zA-Z0-9]"       # shorter definition
```

To improve readability and consistency, spaces are removed from *identifiers*,
and the **snake_case** naming convention is used instead.

Snake case identifiers consist of **lowercase letters**, **digits**,
and **underscores**. 

The naming convention also dictates that each word within an identifier is
separated by an underscore.

This convention makes a clear distinction between individual words and
ensures that identifiers are easily recognizable.

For example, an identifier `non-terminal symbol` would have to be written as `non_terminal_symbol`. 

By adhering to the snake case convention, ReBNF identifiers maintain a
standardized and consistent style throughout the notation, enabling easier
comprehension and usage.

### Modularity

In **ReBNF**, `import` statements are used to bring in *grammar rules* defined
in separate specification files. This enables the reuse of existing rules and
promotes modular design in grammar specifications.

As a result, we can organize grammar rules into separate `.rebnf`
specification files, making it easier to manage and maintain complex
grammars. This allows for better code organization, reuse of common rules,
and separation of concerns.

To import rules from another specification file, we can use the `import`
statement followed by the dotted path to a specification file or the `from`
statement to import only specific items. This enables us to selectively use
and reference rules defined in other files.

Given a folder hierarchy such as:

```
grammar/
├── common.rebnf
└── spec.rebnf
```

Here's an example:

```
from common import *
```

Using modularity in **ReBNF** files can lead to more maintainable and scalable
grammar specifications.

### Optional groups

Square brackets `[ ]` are used to define optional groups rather than
repetition. In **EBNF**, `3 * [aa]` would indicate the generation of multiple
occurrences of `aa` (e.g., A, AA, AAA), whereas in **ReBNF**, it denotes an
optional group that can occur *zero or one* times.

In **EBNF**:
```
aa = "A";
bb = 3 * aa, "B";
cc = 3 * [aa], "C";
```

Which means:

- `aa`: A
- `bb`: AAAB
- `cc`: C, AC, AAC, AAAC


In **ReBNF**:
```
aa = "A";
bb = 3 * aa "B";
cc = 3 * [aa] "C";
```

Which means:

- `aa`: A
- `bb`: AAAB
- `cc`: AAAC

### Concatenation

**ReBNF** also introduces a change in concatenation. 

In **EBNF**, explicit concatenation is required using a comma `,` between two
identifiers. 

However, in **ReBNF**, since snake cased identifiers are enforced,
concatenation is implicit. Adjacent terminals or identifiers are
concatenated.

That's why we are able to drop the comma in `3 * aa, "C"` if we want `cc` to be `"AAAC"`.

## Example

Here's a short example of a **ReBNF** definition for a simple arithmetic
expression language:

```
expression = term { ('+' | '-') term }
term = factor { ('*' | '/') factor }
factor = number | expression
number = r'\d+'
```
## Usage

**ReBNF** notation is used to define the syntax of programming languages,
configuration file formats, or any other formal language. 

It provides a concise and powerful way to express language structures with a
addition of regular expressions.

> Note that the functions in this module are only designed to parse
> syntactically valid **ReBNF** code (code that does not raise when parsed
> using `parse()`). The behavior of the functions in this module is undefined
> when providing invalid **ReBNF** code and it can change at any point. 

## Contributing

Contributions are welcome! If you have suggestions, improvements, or new ideas
related to the **ReBNF** notation, please feel free to open an issue or
submit a pull request.

## License

This project is licensed under the [GPLv3][#gplv3] license - see [LICENSE.md][#license] for details.

[#gplv3]: https://www.gnu.org/licenses/gpl-3.0.html
[#license]: https://gitlab.com/opsocket/rebnf/-/blob/main/LICENSE.md
