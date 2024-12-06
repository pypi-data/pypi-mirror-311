def are_similar(a, b, precision=4):
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            return False
        return all(are_similar(a[key], b[key], precision) for key in a)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        return all(are_similar(x, y, precision) for x, y in zip(a, b))
    elif isinstance(a, float) and isinstance(b, float):
        return round(a, precision) == round(b, precision)
    else:
        return a == b
