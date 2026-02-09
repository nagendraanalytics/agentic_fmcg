def to_list_of_strings(x):
    """
    Convert (n_samples, 1) array / DataFrame
    into list-of-lists for FeatureHasher.
    """
    if hasattr(x, "values"):
        x = x.values
    return [[str(v[0])] for v in x]
