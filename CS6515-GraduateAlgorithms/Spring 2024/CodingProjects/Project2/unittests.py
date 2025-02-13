import pytest
import math
import GA_ProjectUtils as util
from findX import findXinA
params = [
    (1234, 10, 100000),
    (1234, 0, 100000),
    (1234, 1, 100000),
    (1234, 10, 10000),
    (123456, 100000, 200000),
    (123456, 1, 2000),
    (23, 1, 2000),
    (1234, 10, 16),
    (174, 10, 11000)
]
@pytest.mark.parametrize("seed,nLower,nUpper", params)
def test_find_x(seed, nLower, nUpper):
    findX = util.findX()
    x = findX.start(seed, nLower, nUpper)
    
    A = findX.__dict__['_findX__A']
    index, calls = findXinA(x, findX)
    assert findX._findX__A[index] == x
    print(f"\nValue found: {x}, Index: {index}")
    print(f"Calls made: {calls}, Max calls allowed: {findX._findX__maxCalls}")
    assert calls <= findX._findX__maxCalls
@pytest.mark.parametrize("seed,nLower,nUpper", params)
def test_dont_find_x(seed, nLower, nUpper):
    findX = util.findX()
    x = findX.start(seed, nLower, nUpper)
    count_x = findX._findX__A.count(x)
    findX._findX__A = [ele for ele in findX._findX__A if ele != x]
    findX._findX__n -= count_x
    findX._findX__maxCalls = int(math.log(findX._findX__n, 2) * 2) + 2
    index, calls = findXinA(x, findX)
    assert index is None
    print(f"\nValue not found: {x}, Index: {index}")
    print(f"Calls made: {calls}, Max calls allowed: {findX._findX__maxCalls}")
    assert calls <= findX._findX__maxCalls