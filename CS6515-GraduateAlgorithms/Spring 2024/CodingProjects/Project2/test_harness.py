
"""Test harness for Coding project 2. Great Jorb!"""
import argparse
import random
import sys

import GA_ProjectUtils as util
from findX import findXinA

def x_at_index_one_through_ten() -> bool:
    """Test when x is at index 1, 2, 3, 4, 5, 6, 7, 8, 9, and 10."""
    ret = True
    findX = util.findX()

    for idx in range(1, 11):
        findX.start(123456, 100000, 200000)
        x = findX._findX__A[idx]

        # Expect to find x at idx
        index, _calls = findXinA(x, findX)

        if index != idx:
            print(f"FAILED! x_at_index_one_through_ten() Unable to find x when it was at index: {idx}. You said index: {index}")
            ret = False

    return ret


def x_at_end() -> bool:
    """Test when x is at the end."""
    ret = True
    findX = util.findX()
    findX.start(123456, 100000, 200000)
    x = findX._findX__A[-1]
    index, _calls = findXinA(x, findX)

    if index != len(findX._findX__A) - 1:
        print(f"FAILED! x_at_end() Unable to find x when it's the last element in the array")
        ret = False

    return ret


def x_not_in_array() -> bool:
    """Test when x is not in the array."""
    ret = True
    findX = util.findX()
    findX.start(123456, 100000, 200000)
    x = findX._findX__A[-1] + 1
    index, _calls = findXinA(x, findX)

    if index is not None:
        print(f"FAILED! x_not_in_array() Unable to handle when x is not in the array")
        ret = False

    return ret


def provided_solution() -> bool:
    """Test the provided solution."""
    ret = True
    findX = util.findX()
    x = findX.start(1234, 10, 100000)
    index, _calls = findXinA(x, findX)

    if index != 48335:
        print(f"FAILED! provided_solution() Expected to find x at index 48335 per the example solution in the project description")
        ret = False

    return ret


def my_tiny_test() -> bool:
    """Test I came up with while building the algorithm. Nothing special."""
    ret = True
    findX = util.findX()
    x = findX.start(4321, 10, 25)
    index, _calls = findXinA(x, findX)

    if index != 9:
        print(f"FAILED! my_tiny_test() Expected to find x at index 9")
        ret = False

    return ret


def len_of_array_is_one() -> bool:
    """Test when the length of the array is 1."""
    ret = True
    findX = util.findX()
    findX.start(42069247, 1, 1)
    x = findX._findX__A[1]
    index, _calls = findXinA(x, findX)

    # Find x when it exists and the length of the array is 1
    if index != 1:
        print(f"FAILED! len_of_array_is_one() Expected to find x at index 1")
        ret = False

    findX.start(42069247, 1, 1) # Reset the lookup count
    findX._findX__A[1] = x + 1  # Just change it so x is no longer there
    index, _calls = findXinA(x, findX)

    # Handle x not being there when the length of the array is 1
    if index is not None:
        print(f"FAILED! len_of_array_is_one() expected not to find x in the array")
        ret = False

    return ret


def main():
    """Entry Point"""
    ret = 0
    parser = argparse.ArgumentParser("it tests the thing")
    parser.add_argument("--number-of-random-tests-to-run", type=int, default=100)
    args = parser.parse_args()
    nrandom = args.number_of_random_tests_to_run

    # First we'll run the edge cases identified by Andrey Znamensky along with some others
    if x_at_index_one_through_ten():
        print("SUCCESS! You find x when it's at any index between 1 and 10 inclusive.")
    else:
        ret = 1

    if x_at_end():
        print("SUCCESS! You find x when it's at the end of the array.")
    else:
        ret = 1

    if x_not_in_array():
        print("SUCCESS! You can handle when x is not in the array.")
    else:
        ret = 1

    if provided_solution():
        print("SUCCESS! You can handle the provided solution in the coding project")
    else:
        ret = 1

    if my_tiny_test():
        print("SUCCESS! You can handle my tiny test")
    else:
        ret = 1

    if len_of_array_is_one():
        print("SUCCESS! You handle when the length of the array is 1")
    else:
        ret = 1

    # Reset the random seed to something random (uses time or OS randomness source when nothing provided)
    failures = {}
    random.seed()
    print(f"Running {nrandom} purely random tests...")
    for iteration in range(nrandom):
        state = "+"
        findX = util.findX()
        seed = random.randint(1000, 2 ** 32)
        upper_bound = random.randint(25, 500000)
        lower_bound = random.randint(10, upper_bound)

        findX = util.findX()
        findX.start(seed, lower_bound, upper_bound)
        answer_idx = random.randint(1, findX._findX__n)
        x = findX._findX__A[answer_idx]
        idx, calls = findXinA(x, findX)

        # Need to handle the case where we found x at a different index
        # since there can be duplicate values for x
        val_at_idx = findX._findX__A[idx]

        if idx != answer_idx and val_at_idx != x:
            state = "-"
            failures[iteration] = {
                "params": (seed, lower_bound, upper_bound),
                "x": x,
                "x_expected_at_idx": answer_idx,
                "wrong_idx": idx,
                "value_in_array_at_wrong_idx": findX._findX__A[idx],
                "num_calls": calls
            }
            ret = 1

        print(f"\r[{state}] {iteration + 1}/{nrandom}", end="")
    print()

    if failures:
        print(f"\nYou had {len(failures)} failures. They were for the following inputs:\n")
        for failure in failures.values():
            print(f"[-] Seed: {failure['params'][0]}, lower bound: {failure['params'][1]}, upper bound: {failure['params'][2]}")
            print(f"\tNumber of calls: {failure['num_calls']}")
            print(f"\tYou were looking for x = {failure['x']} at array index {failure['x_expected_at_idx']}")
            print(f"\tBut you found value: {failure['value_in_array_at_wrong_idx']} at index {failure['wrong_idx']}")
    else:
        print(f"\n\n!!! All tests pass !!!\n\n")

    return ret

if __name__ == "__main__":
    sys.exit(main())