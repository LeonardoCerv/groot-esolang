import re
from typing import List, Dict, Any, Optional

# Token class represents a single token in the Groot language
class Token:
    def __init__(self, type: str, value: str, line: int, indent: int):
        self.type = type
        self.value = value
        self.line = line
        self.indent = indent

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, indent={self.indent})"

class GrootParser:
    def __init__(self):
        self.tokens = []
        self.current_token = 0
        self.line_number = 0

    def tokenize(self, code: str) -> List[Token]:
        """
        Tokenize Groot code into a list of Token objects.
        Handles comments, whitespace, and indentation.
        """
        self.tokens = []
        self.line_number = 0
        lines = code.split('\n')
        for line in lines:
            self.line_number += 1
            # Remove inline comments
            if '#' in line:
                line = line.split('#', 1)[0]
            # Skip empty or comment-only lines
            if not line.strip():
                continue
            if line.strip().startswith('#'):
                continue
            # Calculate indentation (for block structure)
            indent = len(line) - len(line.lstrip())
            line_content = line.strip()
            if not line_content:
                continue
            # Tokenize the line
            self._tokenize_line(line_content, indent)
        return self.tokens

    def _tokenize_line(self, line: str, indent: int):
        """
        Tokenize a single line of Groot code.
        Uses regex to match known patterns and delegates to helpers.
        """
        # Variable operations: increment, decrement, print
        if re.match(r'^I am (GROOT|groot)[\?\!]*$', line):
            self._parse_variable_operation(line, indent)
            
        # Variable assignments (including function assignment)
        elif re.match(r'^I am (GROOT|groot), I am(\ GROOT|\ groot|\.\.\. Groot)$', line):
            self._parse_assignment(line, indent)
        # Binary operations (add/subtract)
        elif re.match(r'^I am (GROOT|groot)[\?\!] I am (GROOT|groot)$', line):
            self._parse_binary_operation(line, indent)
        # Function declaration (start)
        elif re.match(r'^I am\.\.\.\ Groot,$', line):
            self.tokens.append(Token('FUNCTION_DECL', line, self.line_number, indent))
        # Function call
        elif re.match(r'^I am\.\.\.\ Groot$', line):
            self.tokens.append(Token('FUNCTION_CALL', line, self.line_number, indent))
        # Try block (start)
        elif re.match(r'^I am Groot\?\?\?$', line):
            self.tokens.append(Token('TRY_START', line, self.line_number, indent))
        # Catch block (start)
        elif re.match(r'^I am Groot\!\!\!$', line):
            self.tokens.append(Token('CATCH_START', line, self.line_number, indent))
        # Return statement (ends with dot)
        elif re.match(r'^I am (GROOT|groot)\.$', line):
            var_name = 'GROOT' if 'GROOT' in line else 'groot'
            self.tokens.append(Token('RETURN', var_name, self.line_number, indent))
        # Error output (catch block with dot)
        elif re.match(r'^I am Groot\!\!\!\.$', line):
            self.tokens.append(Token('ERROR_OUTPUT', line, self.line_number, indent))
        else:
            # Unknown or unsupported token
            self.tokens.append(Token('UNKNOWN', line, self.line_number, indent))
    
    def _parse_variable_operation(self, line: str, indent: int):
        """Parse variable increment/decrement/print operations"""
        if 'GROOT' in line:
            var_name = 'GROOT'
        else:
            var_name = 'groot'
            
        if line.endswith('!'):
            self.tokens.append(Token('INCREMENT', var_name, self.line_number, indent))
        elif line.endswith('?'):
            self.tokens.append(Token('DECREMENT', var_name, self.line_number, indent))
        else:
            self.tokens.append(Token('PRINT', var_name, self.line_number, indent))
    
    def _parse_assignment(self, line: str, indent: int):
        """
        Parse variable assignment or function assignment.
        Example: 'I am groot, I am GROOT' or 'I am groot, I am... Groot'
        """
        parts = line.split(', ')
        left_var = 'GROOT' if 'GROOT' in parts[0] else 'groot'
        if 'I am... Groot' in parts[1]:
            # Function assignment (e.g., groot = function())
            self.tokens.append(Token('FUNC_ASSIGN', left_var, self.line_number, indent))
        else:
            # Variable assignment (e.g., groot = GROOT)
            right_var = 'GROOT' if 'GROOT' in parts[1] else 'groot'
            self.tokens.append(Token('ASSIGN', f"{left_var},{right_var}", self.line_number, indent))
    
    def _parse_binary_operation(self, line: str, indent: int):
        """
        Parse binary operations (add/subtract) between variables.
        Example: 'I am groot! I am GROOT' (add), 'I am groot? I am GROOT' (subtract)
        """
        parts = line.split(' I am ')
        left_part = parts[0]
        right_part = parts[1]
        left_var = 'GROOT' if 'GROOT' in left_part else 'groot'
        right_var = 'GROOT' if 'GROOT' in right_part else 'groot'
        if left_part.endswith('!'):
            operation = 'ADD'
        elif left_part.endswith('?'):
            operation = 'SUBTRACT'
        else:
            operation = 'UNKNOWN'
        self.tokens.append(Token(operation, f"{left_var},{right_var}", self.line_number, indent))
    
    def parse(self, tokens: List[Token]) -> Dict[str, Any]:
        """
        Parse a list of tokens into an Abstract Syntax Tree (AST).
        Returns a dictionary representing the program structure.
        """
        self.tokens = tokens
        self.current_token = 0
        ast = {
            'type': 'PROGRAM',
            'statements': [],
            'function': None
        }
        while self.current_token < len(self.tokens):
            stmt = self._parse_statement()
            if stmt:
                if stmt['type'] == 'FUNCTION_DECL':
                    ast['function'] = stmt
                else:
                    ast['statements'].append(stmt)
        return ast
    
    def _parse_statement(self) -> Optional[Dict[str, Any]]:
        """
        Parse a single statement from the token stream.
        Returns a dictionary representing the statement, or None if unknown.
        """
        if self.current_token >= len(self.tokens):
            return None
        token = self.tokens[self.current_token]
        if token.type == 'INCREMENT':
            self.current_token += 1
            return {'type': 'INCREMENT', 'variable': token.value}
        elif token.type == 'DECREMENT':
            self.current_token += 1
            return {'type': 'DECREMENT', 'variable': token.value}
        elif token.type == 'PRINT':
            self.current_token += 1
            return {'type': 'PRINT', 'variable': token.value}
        elif token.type == 'ASSIGN':
            self.current_token += 1
            vars = token.value.split(',')
            return {'type': 'ASSIGN', 'left': vars[0], 'right': vars[1]}
        elif token.type == 'FUNC_ASSIGN':
            self.current_token += 1
            return {'type': 'FUNC_ASSIGN', 'variable': token.value}
        elif token.type == 'ADD':
            self.current_token += 1
            vars = token.value.split(',')
            return {'type': 'ADD', 'left': vars[0], 'right': vars[1]}
        elif token.type == 'SUBTRACT':
            self.current_token += 1
            vars = token.value.split(',')
            return {'type': 'SUBTRACT', 'left': vars[0], 'right': vars[1]}
        elif token.type == 'FUNCTION_DECL':
            return self._parse_function()
        elif token.type == 'FUNCTION_CALL':
            self.current_token += 1
            return {'type': 'FUNCTION_CALL'}
        elif token.type == 'TRY_START':
            return self._parse_try_catch()
        elif token.type == 'RETURN':
            self.current_token += 1
            return {'type': 'RETURN', 'variable': token.value}
        else:
            self.current_token += 1
            return None
    
    def _parse_function(self) -> Dict[str, Any]:
        """
        Parse a function declaration block.
        Collects all indented statements as the function body.
        """
        self.current_token += 1  # Skip FUNCTION_DECL
        function_body = []
        base_indent = None
        while self.current_token < len(self.tokens):
            token = self.tokens[self.current_token]
            if base_indent is None:
                base_indent = token.indent
            # End function block if indentation decreases
            if token.indent < base_indent:
                break
            if token.type == 'RETURN':
                self.current_token += 1
                function_body.append({'type': 'RETURN', 'variable': token.value})
                break
            else:
                stmt = self._parse_statement()
                if stmt:
                    function_body.append(stmt)
        return {
            'type': 'FUNCTION_DECL',
            'body': function_body
        }
    
    def _parse_try_catch(self) -> Dict[str, Any]:
        """
        Parse a try-catch block.
        Collects try and catch bodies based on indentation and block markers.
        """
        self.current_token += 1  # Skip TRY_START
        try_body = []
        catch_body = []
        base_indent = None
        in_catch = False
        while self.current_token < len(self.tokens):
            token = self.tokens[self.current_token]
            if base_indent is None:
                base_indent = token.indent
            # End try-catch block if indentation decreases (and not in catch)
            if token.indent < base_indent and not in_catch:
                break
            if token.type == 'CATCH_START':
                in_catch = True
                self.current_token += 1
                continue
            if token.type == 'ERROR_OUTPUT':
                self.current_token += 1
                catch_body.append({'type': 'ERROR_OUTPUT'})
                break
            stmt = self._parse_statement()
            if stmt:
                if in_catch:
                    catch_body.append(stmt)
                else:
                    try_body.append(stmt)
        return {
            'type': 'TRY_CATCH',
            'try_body': try_body,
            'catch_body': catch_body
        }