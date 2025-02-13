import pytest
from knapsack import knapsack


def sample_items_1():
    return {
        # name, weight, value
        1: ("item1", 2, 4),
        2: ("item2", 4, 1),
        3: ("item3", 3, 2),
        4: ("item4", 2, 3)
    }


def sample_items_2():
    return {
        # name, weight, value
        1: ("item1", 2, 4),
        2: ("item2", 1, 1),
        3: ("item3", 2, 3),
        4: ("item4", 4, 3)
    }


@pytest.mark.parametrize("items_f,capacity,expected_items,expected_value", [
    (sample_items_1, 0, set(), 0),
    (sample_items_1, 1, set(), 0),
    (sample_items_1, 2, {"item1"}, 4),
    (sample_items_1, 3, {"item1"}, 4),
    (sample_items_1, 4, {"item1", "item4"}, 7),
    (sample_items_1, 5, {"item1", "item4"}, 7),
    (sample_items_1, 6, {"item1", "item4"}, 7),
    (sample_items_1, 7, {"item1", "item3", "item4"}, 9),
    (sample_items_1, 8, {"item1", "item3", "item4"}, 9),
    (sample_items_1, 9, {"item1", "item3", "item4"}, 9),
    (sample_items_1, 10, {"item1", "item3", "item4"}, 9),
    (sample_items_1, 11, {"item1", "item2", "item3", "item4"}, 10),
    (sample_items_1, 12, {"item1", "item2", "item3", "item4"}, 10),
    (sample_items_1, 13, {"item1", "item2", "item3", "item4"}, 10),
    (sample_items_2, 0, set(), 0),
    (sample_items_2, 1, {"item2"}, 1),
    (sample_items_2, 2, {"item1"}, 4),
    (sample_items_2, 3, {"item1", "item2"}, 5),
    (sample_items_2, 4, {"item1", "item3"}, 7),
    (sample_items_2, 5, {"item1", "item2", "item3"}, 8),
    (sample_items_2, 6, {"item1", "item2", "item3"}, 8),
    (sample_items_2, 7, {"item1", "item2", "item3"}, 8),
    (sample_items_2, 8, {"item1", "item3", "item4"}, 10),
    (sample_items_2, 9, {"item1", "item2", "item3", "item4"}, 11),
    (sample_items_2, 10, {"item1", "item2", "item3", "item4"}, 11),
])
def test_knapsack(items_f, capacity, expected_items, expected_value):
    results = knapsack(itemsDict=items_f(), maxWeight=capacity)

    # make sure there aren't any duplicates
    actual_items_list = [r[0] for r in results]
    actual_items = set(actual_items_list)
    assert len(actual_items) == len(actual_items_list)

    # make sure returned items and value match
    actual_value = sum([r[2] for r in results])
    assert actual_items == expected_items
    assert actual_value == expected_value