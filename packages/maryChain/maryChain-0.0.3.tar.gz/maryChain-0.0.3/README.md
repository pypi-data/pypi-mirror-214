# README.md

## Introduction

`maryChain` is a powerful programming language designed to meet modern programming needs. It combines characteristics from functional and object-oriented programming paradigms to create an expressive, dynamic, and powerful syntax. The language includes important features such as: 

- Functions and lambdas
- Pipelining
- Binary operations
- Control structures (conditional and loops)
- Lazy evaluation
- Support for standard data types like numbers, strings, and booleans
- Type casting functions
- Support for modules and namespaces
- Support for comments

## Main Features

### Functions and Lambdas

Functions are first-class citizens in `maryChain` and can be declared using the `def` keyword. Lambda expressions, on the other hand, are represented by the `LAMBDA` keyword and allow for creating inline anonymous functions.

### Pipelining

Pipelining is a feature that allows the output of one function to be directly fed as the input of the next. The `PIPE` symbol is used to represent this operation.

### Binary Operations

Standard mathematical binary operations are supported, including addition (`PLUS`), subtraction (`MINUS`), multiplication (`TIMES`), and division (`DIVIDE`). Comparison operators are also supported, including equals (`EQUALITY`), greater than (`GREATER`), less than (`LESS`), greater or equal (`GREATEREQUAL`), and less or equal (`LESSEQUAL`).

### Control Structures

Conditional structures like `IF`, `THEN`, `ELSE`, along with loops like `WHILE` `DO`, are provided in the `maryChain` language. 

### Lazy Evaluation

In `maryChain`, expressions can be declared as lazy, which means they are not evaluated until their result is needed.

### Data Types

`maryChain` supports standard data types such as numbers, strings, and booleans.

### Type Casting Functions

Type casting is supported through casting functions like `INTEGERCAST`, `DOUBLECAST`, `STRINGCAST`, `BOOLEANCAST`.

### Support for Modules and Namespaces

`maryChain` provides support for modules and namespaces using `IMPORT` and `NAMESPACE_OP` features. This allows for better code organization and modular programming.

### Comments

Comments in `maryChain` are supported, enabling developers to include explanations and documentation within the code itself.

## BNF Grammar for `maryChain` 

The BNF (Backus-Naur Form) grammar for `maryChain` can be inferred from the parser implementation and is as follows:

```
<program> ::= <import>* <expression>?
<import> ::= IMPORT <IDENTIFIER> AS <IDENTIFIER>
<expression> ::= <assignment> | <let_in> | <binop> | <uminus> | <paren_expression> | <term> 
<assignment> ::= <IDENTIFIER> EQUALS <expression>
<let_in> ::= LET <IDENTIFIER> EQUALS <expression> IN <expression>
<binop> ::= <expression> <bin_op> <expression>
<uminus> ::= MINUS <expression>
<paren_expression> ::= LPAREN <expression> RPAREN
<term> ::= <factor>
<factor> ::= NUMBER | STRING | BOOLEAN | <function_call> | <IDENTIFIER>
<function_call> ::= <IDENTIFIER> LPAREN <args> RPAREN
<args> ::= <arg>* 
<arg> ::= <expression>
```

This grammar represents the syntactic structure of a `maryChain` program. The keywords in the language are represented as they are, while in `<bin_op>`, `<IDENTIFIER>`, `<args>`, and `<arg>`, the angle brackets signify a category of symbol.

Please note that this is a simplified representation of the `mary

Chain` grammar for illustration purposes. In the actual parser, additional rules and constructs are included to handle precedence, associativity, and complex expressions.

