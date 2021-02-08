
## NOTE FOR simplicity we are not judging the cross re cross just a cross. So i at idx 1 we have a cross and then at idx 5
# we have a cross we will treat both the same.


def find_boolean_pattern_in_column(pattern, pattern_column, window_length=2):

    true_where_pattern_is_found = \
        (pattern_column.rolling(window=window_length).apply(lambda x: (x == pattern).all(), raw=True)).astype(bool)
    # for some reason idx 0 is always returning true when its not
    true_where_pattern_is_found.iloc[0] = False
    return true_where_pattern_is_found