import functools


def _compose(*functions):
    return functools.reduce(
        lambda acc, cur: lambda x: acc(cur(x)),
        reversed(functions),
        lambda x_tuple: x_tuple[0],
    )


def basic_pipeline(fields_to_rename={}, transformations={}):
    def rename_columns(input_tuple):
        df, schema = input_tuple

        fields = [
            field
            for field in schema.names
            if (field in fields_to_rename)
            and (fields_to_rename[field] in df.columns)
            and (field not in df.columns)
        ]

        return (
            functools.reduce(
                lambda df, field: df.withColumnRenamed(
                    existing=fields_to_rename[field], new=field
                ),
                fields,
                df,
            ),
            schema,
        )

    def select_expr_columns(input_tuple):
        df, schema = input_tuple

        exprs = [
            col_name if col_name not in transformations else transformations[col_name]
            for col_name in schema.names
        ]

        return df.selectExpr(exprs), schema

    return _compose(rename_columns, select_expr_columns)
