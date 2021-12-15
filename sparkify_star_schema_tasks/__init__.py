# TODO: create doc strings for all functions


import functools


def _compose(*functions):
    reducer = lambda acc, cur: lambda x: acc(cur(x))
    last_function = lambda x_tuple: x_tuple[0]

    return functools.reduce(reducer, reversed(functions), last_function)


def create_basic_pipeline(rename_transformations={}, cast_transformations={}):
    def rename_columns(input_tuple):
        df, schema = input_tuple

        fields = [
            field
            for field in schema.names
            # first: field from schema is in transformation keys
            if (field in rename_transformations)
            # second: data frame has a field name asked by the transformation list
            and (rename_transformations[field] in df.columns)
            # third: data frame does not already have the field
            and (field not in df.columns)
        ]

        reducer = lambda df, field: df.withColumnRenamed(
            rename_transformations[field], field
        )
        df_reduced = functools.reduce(reducer, fields, df)

        return (df_reduced, schema)

    def select_expr_columns(input_tuple):
        df, schema = input_tuple

        exprs = [
            col_name
            if col_name not in cast_transformations
            else cast_transformations[col_name]
            for col_name in schema.names
        ]

        return df.selectExpr(exprs), schema

    return _compose(rename_columns, select_expr_columns)
