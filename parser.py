"""
Groot Language Parser
Handles tokenization and parsing of Groot language constructs.
"""

import re
from enum import Enum
from typing import List

class TokenType(Enum):
    """Token types for the Groot language."""
    IDENTITY = "IDENTITY"                          # "I am Groot"
    IDENTITY_FORCE = "IDENTITY_FORCE"              # "I AM GROOT" (all caps)
    IDENTITY_NEGATIVE = "IDENTITY_NEGATIVE"        # "I am not Groot"
    PUNCTUATION_PRINT = "PUNCTUATION_PRINT"        # . (period)
    PUNCTUATION_INPUT = "PUNCTUATION_INPUT"        # ! (exclamation)
    PUNCTUATION_QUERY = "PUNCTUATION_QUERY"        # ? (question mark)
    PUNCTUATION_PAUSE = "PUNCTUATION_PAUSE"        # , (comma)
    PUNCTUATION_CONTINUE = "PUNCTUATION_CONTINUE"  # ... (ellipsis)
    WHITESPACE = "WHITESPACE"                      # Spaces, tabs, newlines
    UNKNOWN = "UNKNOWN"                            # Unrecognized tokens

class Token:
    """Represents a single token in the Groot language."""
    
    def __init__(self, token_type: TokenType, value: str, position: int = 0):
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self):
        return f"Token({self.type.value}, '{self.value}')"
    
    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return False

class GrootParser:
    """Parser for the esolang"""
    
    def __init__(self):
        """Initialize the parser with token patterns."""

        # identify the tokens using regex
        self.patterns = [
            (r'I\s+am\s+not\s+Groot', TokenType.IDENTITY_NEGATIVE),
            (r'I\s+AM\s+GROOT', TokenType.IDENTITY_FORCE),
            (r'I\s+am\s+Groot', TokenType.IDENTITY),
            
            # Case-insensitive variations
            (r'i\s+am\s+not\s+groot', TokenType.IDENTITY_NEGATIVE),
            (r'i\s+am\s+groot', TokenType.IDENTITY),
            
            # Punctuations
            (r'\.{3,}', TokenType.PUNCTUATION_CONTINUE),  # ... (3 or more dots)
            (r'\.', TokenType.PUNCTUATION_PRINT),         # .
            (r'!', TokenType.PUNCTUATION_INPUT),          # !
            (r'\?', TokenType.PUNCTUATION_QUERY),         # ?
            (r',', TokenType.PUNCTUATION_PAUSE),          # ,
            
            # Whitespace
            (r'\s+', TokenType.WHITESPACE),
        ]
        
        self.compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), token_type)
            for pattern, token_type in self.patterns
        ]
    
    def tokenize(self, text: str) -> List[TokenType]:
        """
        Tokenize a string of Groot code into tokens.
        
        @Args:
            text: The input string to tokenize
            
        @Returns:
            List of TokenType enums (excluding whitespace)
        """
        tokens = []
        position = 0
        
        while position < len(text):
            matched = False
            
            for pattern, token_type in self.compiled_patterns:
                match = pattern.match(text, position)
                if match:
                    value = match.group(0)
                    token = Token(token_type, value, position)
                    
                    # Skip whitespace tokens in the output
                    if token_type != TokenType.WHITESPACE:
                        tokens.append(token)
                    
                    position = match.end()
                    matched = True
                    break
            
            if not matched:
                # Handle unknown characters
                char = text[position]
                token = Token(TokenType.UNKNOWN, char, position)
                tokens.append(token)
                position += 1
        
        # Return only the token types for the tests
        return [token.type for token in tokens]
    
    def tokenize_detailed(self, text: str) -> List[Token]:
        """
        Tokenize a string and return detailed Token objects.
        
        Args:
            text: The input string to tokenize
            
        Returns:
            List of Token objects with details
        """
        tokens = []
        position = 0
        
        while position < len(text):
            matched = False
            
            for pattern, token_type in self.compiled_patterns:
                match = pattern.match(text, position)
                if match:
                    value = match.group(0)
                    token = Token(token_type, value, position)
                    tokens.append(token)
                    position = match.end()
                    matched = True
                    break
            
            if not matched:
                # Handle unknown characters
                char = text[position]
                token = Token(TokenType.UNKNOWN, char, position)
                tokens.append(token)
                position += 1
        
        return tokens

def test_tokenizer():
    """test tokenizer functionality"""
    parser = GrootParser()
    
    test_cases = [
        ("I am Groot.", [TokenType.IDENTITY, TokenType.PUNCTUATION_PRINT]),
        ("I AM GROOT!", [TokenType.IDENTITY_FORCE, TokenType.PUNCTUATION_INPUT]),
        ("I am not Groot?", [TokenType.IDENTITY_NEGATIVE, TokenType.PUNCTUATION_QUERY]),
        ("i am groot,", [TokenType.IDENTITY, TokenType.PUNCTUATION_PAUSE]),
        ("I am Groot...", [TokenType.IDENTITY, TokenType.PUNCTUATION_CONTINUE]),
    ]
    
    print("Running tokenizer tests...")
    for i, (input_text, expected) in enumerate(test_cases, 1):
        result = parser.tokenize(input_text)
        status = "✓" if result == expected else "✗"
        print(f"Test {i}: {status} '{input_text}' -> {result}")
        if result != expected:
            print(f"  Expected: {expected}")
            print(f"  Got:      {result}")
    
    print("\nDetailed tokenization examples:")
    for input_text, _ in test_cases:
        tokens = parser.tokenize_detailed(input_text)
        print(f"'{input_text}' -> {tokens}")

if __name__ == "__main__":
    test_tokenizer()