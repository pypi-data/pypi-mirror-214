import logging, json
from .util import read_source_files, get_code


def discard_tail(json_data: dict, max_elements: int = 5) -> dict:
    """
    Reduces arrays and dictionaries sizes by keeping only a given number of
    items from the head of the collection and discarding the tail.

    :param json_data: The json data to simplify
    :param max_elements: The maximum number of head elements to keep
    :returns: A structure of the json data that is easier to read
    """
    if max_elements < 1:
        raise ValueError("max_elements must be greater than 0")

    if isinstance(json_data, dict):
        return {k: discard_tail(v, max_elements=max_elements) for k, v in list(json_data.items())[:max_elements]}

    if isinstance(json_data, (list, set)):
        if len(json_data) <= max_elements:
            return [discard_tail(item, max_elements=max_elements) for item in json_data]
        else:
            return [discard_tail(item, max_elements=max_elements) for item in list(json_data)[:max_elements]]

    return json_data


def _discard_shallow_tail(json_data: dict, max_elements: int = 5):
    """
    Helper for discard_shallow_tail, returns the summary and max depth
    of the nested structure.
    """
    if max_elements < 1:
        raise ValueError("max_elements must be greater than 0")

    depth = {0: 0}
    aggregates = None
    primitives = None

    if isinstance(json_data, dict):
        aggregates = {}
        primitives = {}
        for k, v in json_data.items():
            if isinstance(v, (list, dict, set)):
                aggregates[k], depth[k] = _discard_shallow_tail(v, max_elements=max_elements)
            elif len(primitives) < max_elements:
                primitives[k] = v

    elif isinstance(json_data, (list, set)):
        aggregates = []
        primitives = []
        for item in json_data:
            if isinstance(item, (list, dict, set)):
                aggregate_item, d = _discard_shallow_tail(item, max_elements=max_elements)
                depth[len(aggregates)] = d
                aggregates.append(aggregate_item)
            elif len(primitives) < max_elements:
                primitives.append(item)

    if len(aggregates) > max_elements:
        if isinstance(aggregates, dict):
            sorted_agg = sorted(aggregates.items(), key=lambda k, v: depth.get(k) or 1, reverse=True)
            aggregates = {k: v for k, v in sorted_agg[:max_elements]}
        else:
            sorted_agg = sorted(enumerate(aggregates), key=lambda kv: depth.get(kv[0]) or 1, reverse=True)
            aggregates = [v for k, v in sorted_agg[:max_elements]]

        return aggregates, max(depth.values()) + 1

    # not enough aggregate items
    result = aggregates
    if isinstance(primitives, dict):
        for k, v in primitives.items():
            result[k] = v
            if len(result) >= max_elements:
                break
    else:
        result = [*aggregates, *primitives[0 : max_elements - len(aggregates)]]

    return result, max(depth.values()) + 1


def discard_shallow_tail(json_data: dict, max_elements: int = 5) -> dict:
    """
    Summarizes very large, pententially nested json data by generating a
    human-readable structure from the input data.

    Reduces arrays and dictionaries sizes by keeping only a few exemplary items
    and discarding the rest. To create the most accurate data structure summary,
    items with shallow nesting are discarded in favor of items with deeper
    nesting level.

    This method works great for dense and regular data.
    """
    result, _ = _discard_shallow_tail(json_data, max_elements)
    return result
