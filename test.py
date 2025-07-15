"""
Test 1
Tests for basic tokenization functionality.
"""

from parser import GrootParser, TokenType

def run_tests():
    parser = GrootParser()
    
    print("=== Phase 1 Benchmark Tests ===\n")
    
    # Test 1: Basic identity with period
    print("Test 1: tokenize('I am Groot.')")
    result1 = parser.tokenize("I am Groot.")
    expected1 = [TokenType.IDENTITY, TokenType.PUNCTUATION_PRINT]
    print(f"Expected: {expected1}")
    print(f"Got:      {result1}")
    print(f"Status:   {'✓ PASS' if result1 == expected1 else '✗ FAIL'}\n")
    
    # Test 2: Force identity with exclamation
    print("Test 2: tokenize('I AM GROOT!')")
    result2 = parser.tokenize("I AM GROOT!")
    expected2 = [TokenType.IDENTITY_FORCE, TokenType.PUNCTUATION_INPUT]
    print(f"Expected: {expected2}")
    print(f"Got:      {result2}")
    print(f"Status:   {'✓ PASS' if result2 == expected2 else '✗ FAIL'}\n")
    
    # Additional tests for success criteria (5 basic patterns)
    additional_tests = [
        ("I am not Groot?", [TokenType.IDENTITY_NEGATIVE, TokenType.PUNCTUATION_QUERY]),
        ("i am groot,", [TokenType.IDENTITY, TokenType.PUNCTUATION_PAUSE]),
        ("I am Groot...", [TokenType.IDENTITY, TokenType.PUNCTUATION_CONTINUE]),
    ]
    
    for i, (input_text, expected) in enumerate(additional_tests, 3):
        print(f"Test {i}: tokenize('{input_text}')")
        result = parser.tokenize(input_text)
        print(f"Expected: {expected}")
        print(f"Got:      {result}")
        print(f"Status:   {'✓ PASS' if result == expected else '✗ FAIL'}\n")
    
    # Summary
    all_tests = [
        (parser.tokenize("I am Groot."), [TokenType.IDENTITY, TokenType.PUNCTUATION_PRINT]),
        (parser.tokenize("I AM GROOT!"), [TokenType.IDENTITY_FORCE, TokenType.PUNCTUATION_INPUT]),
    ] + [(parser.tokenize(test[0]), test[1]) for test in additional_tests]
    
    passed = sum(1 for result, expected in all_tests if result == expected)
    total = len(all_tests)
    
    print(f"=== Summary ===")
    print(f"Tests passed: {passed}/{total}")
    print(f"Success criteria: {'✓ MET' if passed >= 5 else '✗ NOT MET'}")

if __name__ == "__main__":
    run_tests()
