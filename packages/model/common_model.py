import numpy as np


def standardize_col_name(name):
    return name.lower().replace(' ', '_')


def filter_unnamed_cols(cols):
    unnamed = cols.str.contains('Unnamed')
    cols = cols.mask(unnamed, np.nan)
    cols = cols.ffill()
    return cols


def modify_column_names(main_columns, sub_columns):
    mod_cols = []
    main_columns = filter_unnamed_cols(main_columns)
    for main_col, sub_col in zip(main_columns, sub_columns):
        main_col = standardize_col_name(main_col)
        if sub_col is np.nan or isinstance(sub_col, np.float64):
            mod_cols.append(main_col)
        else:
            sub_col = standardize_col_name(sub_col)
            mod_cols.append(main_col + ':' + sub_col)
    return mod_cols
