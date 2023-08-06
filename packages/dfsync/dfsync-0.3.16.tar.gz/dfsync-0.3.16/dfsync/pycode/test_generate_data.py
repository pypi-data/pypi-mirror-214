from .generate_data import discard_tail, discard_shallow_tail


def test_list_discard_tail():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert discard_tail(data, 2) == [1, 2]


def test_list_discard_shallow_tail():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert discard_shallow_tail(data, 2) == [1, 2]


def test_set_discard_tail():
    data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    assert len(discard_tail(data, 2)) == 2


def test_set_discard_shallow_tail():
    data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    assert len(discard_shallow_tail(data, 2)) == 2


def test_list_discard_shallow_tail():
    data = [1, [2, 2], 3, 4, 5, 6, 7, 8, 9, 10]
    assert discard_shallow_tail(data, 2) == [[2, 2], 1]


def test_dict_list_discard_shallow_tail():
    data = [1, {"a": "a", "b": "b"}, {"a": "aa", "b": "bb"}, {"a": "aaa", "b": "bbb"}, 5, 6, 7, 8, 9, 10]
    assert discard_shallow_tail(data, 2) == [
        {"a": "a", "b": "b"},
        {"a": "aa", "b": "bb"},
    ]


def test_dict_list_deeper_discard_shallow_tail():
    data = [1, {"a": "a", "b": "b"}, {"a": "aa", "b": "bb"}, {"a": "aaa", "b": {"bbb": "depth3"}}, 5, 6, 7, 8, 9, 10]
    assert discard_shallow_tail(data, 2) == [
        {"a": "aaa", "b": {"bbb": "depth3"}},
        {"a": "a", "b": "b"},
    ]


def test_dict_list_deeper_wider_discard_shallow_tail():
    data = [1, {"a": "a", "b": "b", "c": "c", "d": "d"}, {"a": "aa"}, {"a": "aaa", "b": {"bbb": "depth3"}}, 5, 6, 7, 8]
    assert discard_shallow_tail(data, 2) == [
        {"a": "aaa", "b": {"bbb": "depth3"}},
        {"a": "a", "b": "b", "c": "c", "d": "d"},
    ]


def test_dict_list_deeper_dict_discard_shallow_tail():
    data = [1, {"a": "a", "b": "b", "c": "c", "d": "d"}, 3, 4]
    assert discard_shallow_tail(data, 2) == [
        {"a": "a", "b": "b", "c": "c", "d": "d"},
        1,
    ]
