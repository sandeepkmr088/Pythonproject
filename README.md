# Problem Overview:
## Write a Python program, that takes a json file (which contains the information of a directory in nested structure) and prints out its content in the console in the style of ls (linux utility).

This is meant to be equivalent to the following structure:
interpreter
|-- .gitignore
|-- LICENSE
|-- README.md
|-- ast
|   |-- ast.go
|   |-- go.mod
|-- go.mod
|-- lexer
|   |-- go.mod
|   |-- lexer.go
|   |-- lexer_test.go
|-- main.go
|-- parser
|   |-- go.mod
|   |-- parser.go
|   |-- parser_test.go
|-- token
|-- go.mod
|-- token.go
As might be evident from the structure, the field name refers to the name of
the file or directory, size refers to the size on disk in bytes, time_modified
refers to the time the file or directory was last modified, in seconds (epoch),
permissions refers to the permissions for the file or directory in unix terms.
The field contents are only present for items (file/directory), which
are directories, and can contain a list of other items that are present within
the directory.

