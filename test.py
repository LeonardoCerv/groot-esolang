"""
Unit tests for basic tokenization functionality in the Groot language parser.
Each test checks a single Groot statement and compares the token type output.
"""

from parser import GrootParser

def run_tests():
    parser = GrootParser()
    print("=== Tests ===\n")

    # Test 1: Basic print statement
    print("Test 1: tokenize('I am groot')")
    result1 = parser.tokenize("I am groot")
    expected1 = ['PRINT']
    print(f"Expected: {expected1}")
    print(f"Got:      {[t.type for t in result1]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result1] == expected1 else '\u2717 FAIL'}\n")

    # Test 2: Increment statement
    print("Test 2: tokenize('I am GROOT!')")
    result2 = parser.tokenize("I am GROOT!")
    expected2 = ['INCREMENT']
    print(f"Expected: {expected2}")
    print(f"Got:      {[t.type for t in result2]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result2] == expected2 else '\u2717 FAIL'}\n")

    # Test 3: Decrement statement
    print("Test 3: tokenize('I am groot?')")
    result3 = parser.tokenize("I am groot?")
    expected3 = ['DECREMENT']
    print(f"Expected: {expected3}")
    print(f"Got:      {[t.type for t in result3]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result3] == expected3 else '\u2717 FAIL'}\n")

    # Test 4: Assignment statement
    print("Test 4: tokenize('I am groot, I am GROOT')")
    result4 = parser.tokenize("I am groot, I am GROOT")
    expected4 = ['ASSIGN']
    print(f"Expected: {expected4}")
    print(f"Got:      {[t.type for t in result4]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result4] == expected4 else '\u2717 FAIL'}\n")

    # Test 5: Function assignment
    print("Test 5: tokenize('I am groot, I am... Groot')")
    result5 = parser.tokenize("I am groot, I am... Groot")
    expected5 = ['FUNC_ASSIGN']
    print(f"Expected: {expected5}")
    print(f"Got:      {[t.type for t in result5]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result5] == expected5 else '\u2717 FAIL'}\n")

    # Test 6: Binary operation (add)
    print("Test 6: tokenize('I am groot! I am GROOT')")
    result6 = parser.tokenize("I am groot! I am GROOT")
    expected6 = ['ADD']
    print(f"Expected: {expected6}")
    print(f"Got:      {[t.type for t in result6]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result6] == expected6 else '\u2717 FAIL'}\n")

    # Test 7: Binary operation (subtract)
    print("Test 7: tokenize('I am groot? I am GROOT')")
    result7 = parser.tokenize("I am groot? I am GROOT")
    expected7 = ['SUBTRACT']
    print(f"Expected: {expected7}")
    print(f"Got:      {[t.type for t in result7]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result7] == expected7 else '\u2717 FAIL'}\n")

    # Test 8: Function declaration
    print("Test 8: tokenize('I am... Groot,')")
    result8 = parser.tokenize("I am... Groot,")
    expected8 = ['FUNCTION_DECL']
    print(f"Expected: {expected8}")
    print(f"Got:      {[t.type for t in result8]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result8] == expected8 else '\u2717 FAIL'}\n")

    # Test 9: Function call
    print("Test 9: tokenize('I am... Groot')")
    result9 = parser.tokenize("I am... Groot")
    expected9 = ['FUNCTION_CALL']
    print(f"Expected: {expected9}")
    print(f"Got:      {[t.type for t in result9]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result9] == expected9 else '\u2717 FAIL'}\n")

    # Test 10: Try block start
    print("Test 10: tokenize('I am Groot???')")
    result10 = parser.tokenize("I am Groot???")
    expected10 = ['TRY_START']
    print(f"Expected: {expected10}")
    print(f"Got:      {[t.type for t in result10]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result10] == expected10 else '\u2717 FAIL'}\n")

    # Test 11: Catch block start
    print("Test 11: tokenize('I am Groot!!!')")
    result11 = parser.tokenize("I am Groot!!!")
    expected11 = ['CATCH_START']
    print(f"Expected: {expected11}")
    print(f"Got:      {[t.type for t in result11]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result11] == expected11 else '\u2717 FAIL'}\n")

    # Test 12: Return statement
    print("Test 12: tokenize('I am groot.')")
    result12 = parser.tokenize("I am groot.")
    expected12 = ['RETURN']
    print(f"Expected: {expected12}")
    print(f"Got:      {[t.type for t in result12]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result12] == expected12 else '\u2717 FAIL'}\n")

    # Test 13: Error output
    print("Test 13: tokenize('I am Groot!!!.')")
    result13 = parser.tokenize("I am Groot!!!.")
    expected13 = ['ERROR_OUTPUT']
    print(f"Expected: {expected13}")
    print(f"Got:      {[t.type for t in result13]}")
    print(f"Status:   {'\u2713 PASS' if [t.type for t in result13] == expected13 else '\u2717 FAIL'}\n")

    # Summary of all tests
    all_tests = [
        ([t.type for t in parser.tokenize("I am groot")], ['PRINT']),
        ([t.type for t in parser.tokenize("I am GROOT!")], ['INCREMENT']),
        ([t.type for t in parser.tokenize("I am groot?")], ['DECREMENT']),
        ([t.type for t in parser.tokenize("I am groot, I am GROOT")], ['ASSIGN']),
        ([t.type for t in parser.tokenize("I am groot, I am... Groot")], ['FUNC_ASSIGN']),
        ([t.type for t in parser.tokenize("I am groot! I am GROOT")], ['ADD']),
        ([t.type for t in parser.tokenize("I am groot? I am GROOT")], ['SUBTRACT']),
        ([t.type for t in parser.tokenize("I am... Groot,")], ['FUNCTION_DECL']),
        ([t.type for t in parser.tokenize("I am... Groot")], ['FUNCTION_CALL']),
        ([t.type for t in parser.tokenize("I am Groot???")], ['TRY_START']),
        ([t.type for t in parser.tokenize("I am Groot!!!")], ['CATCH_START']),
        ([t.type for t in parser.tokenize("I am groot.")], ['RETURN']),
        ([t.type for t in parser.tokenize("I am Groot!!!.")], ['ERROR_OUTPUT']),
    ]

    passed = sum(1 for result, expected in all_tests if result == expected)
    total = len(all_tests)

    print(f"=== Summary ===")
    print(f"Tests passed: {passed}/{total}")
    print(f"Success criteria: {'\u2713 MET' if passed >= total else '\u2717 NOT MET'}")

if __name__ == "__main__":
    run_tests()
