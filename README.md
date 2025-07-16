# I Am Groot - Esoteric Programming Language

A fun, Guardians of the Galaxy-inspired esoteric programming language where every statement begins with "I am Groot" variations.

## Features

- Two Variables: `GROOT` (uppercase) and `groot` (lowercase)
- Basic Operations: Increment, decrement, print, assignment
- Arithmetic: Addition and subtraction between variables
- Functions: Define and call custom functions
- Error Handling: Try-catch blocks with themed error messages
- Interactive REPL: Command-line interpreter with file execution support

## Installation

```bash
git clone https://github.com/leonardocerv/groot-esolang.git
cd groot-esolang
python main.py
```

## Quick Start

### Interactive Mode

```bash
python main.py
```

### Run a File

```bash
# In the interpreter
groot> run examples/example.groot

# Or directly
python main.py examples/example.groot
```

## Language Syntax

### Variables

- `I am GROOT` - Print uppercase variable
- `I am groot` - Print lowercase variable

### Operations

- `I am GROOT!` - Increment GROOT by 1
- `I am groot!` - Increment groot by 1
- `I am GROOT?` - Decrement GROOT by 1 (prevents negative values)
- `I am groot?` - Decrement groot by 1 (prevents negative values)

### Assignments

- `I am groot, I am GROOT` - Set groot = GROOT
- `I am GROOT, I am groot` - Set GROOT = groot
- `I am groot, I am... Groot` - Set groot = function_result()

### Arithmetic

- `I am groot! I am GROOT` - Add GROOT to groot (groot += GROOT)
- `I am groot? I am GROOT` - Subtract GROOT from groot (groot -= GROOT)

### Functions

```
I am... Groot,
    I am GROOT!
    I am groot!
    I am groot.

I am groot, I am... Groot
```

### Error Handling

```
I am groot???
    I am GROOT?
I am groot!!!
    I am groot.
```

## Development

### Running Tests

```bash
python test.py
```

### Project Structure

```
i-am-groot-esolang/
├── main.py           # Main interpreter and REPL
├── parser.py         # Tokenizer and parser
├── interpreter.py    # AST interpreter and execution engine
├── test.py           # Unit tests
├── examples/         # Sample programs
├── README.md         # This file
└── LICENSE           # MIT License
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
