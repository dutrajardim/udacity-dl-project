import functools

def s3_path_exists(sc, path):
    """
    Description:
        This function is responsible for cheching if a s3 path
        exists using a spark context.
        Thanks @Dror, @Kini and @rosefun (https://stackoverflow.com/questions/55589969/how-to-check-a-file-folder-is-present-using-pyspark-without-getting-exception)
    Arguments:
        sc: The spark context to be used
        path: The path of the bucket.
    Return:
        It returns True if the bucket exists and
        flase otherwise.
    """
    
    # manipulating java to get a file system module
    fs = sc._jvm.org.apache.hadoop.fs.FileSystem.get(
        sc._jvm.java.net.URI.create(path),
        sc._jsc.hadoopConfiguration(),
    )
    
    return fs.exists(sc._jvm.org.apache.hadoop.fs.Path(path))

def _compose(*functions):
    """
    Description: 
        This function is responsible for compose a new function 
        chaining a sequence of functions. The output of the
        previous function is given to the next one as input. 

    Arguments:
        functions: all functions in the order that the chain will be coposed.
        All functions accept a tuple with a spark data frame and a schema, and
        returns the tuple with the transformations applied
    
    Returns:
        A composed function that accept one argument to be precessed
        by the chain. The returned function accept a tuple where
        the first element is a spark data frame and the second is
        a spark schema.
    """

    # reducer function that chain the give functions
    reducer = lambda acc, cur: lambda x: acc(cur(x))
    # the last function ensure that the last returned value 
    # will be just the spark dataframe (ignoring the schema)
    last_function = lambda x_tuple: x_tuple[0]

    return functools.reduce(reducer, reversed(functions), last_function)


def create_basic_pipeline(rename_transformations={}, cast_transformations={}):
    """
    Description: 
        This function is responsible for compose a function that
        will apply rename and cast transformations to a given spark
        data frame
    
    Arguments:
        rename_transformations: A dictionary where the keys are 
        the desired column names and values are the current names of the 
        column in the spark data frame.
        cast_tranformations: A dictionary where the keys are the current
        column names and the values are spark sql expressions to be applied.

    Returns:
        It returns a spark data frame with the transformations applied.
    """
    
    def _rename_columns(input_tuple):
        """
        Description:
            This function is responsible for apply the rename transformations
            given as arguments to create_basic_pipeline.
        
        Arguments:
            input_table: a tuple where the first element is a spark data frame
            and the second is a spark schema.

        Returns:
            The given function argumens with the lazy transformations applied to the
            spark data frame. 
        """
        df, schema = input_tuple

        # setting the fields to be renamed
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

        # reducer function that apply the spark lazy transformation
        reducer = lambda df, field: df.withColumnRenamed(
            rename_transformations[field], field
        )
        df_reduced = functools.reduce(reducer, fields, df)

        return (df_reduced, schema)

    def _select_expr_columns(input_tuple):
        """
        Description:
            This function is responsible for apply cast transformations and select
            the columns listed in the schema in the given spark data frame.

        Arguments:
            input_table: a tuple where the first element is a spark data frame
            and the second is a spark schema.

        Returns:
            The given function argumens with the lazy transformations applied to the
            spark data frame. 
        """
        df, schema = input_tuple

        # setting transformations expressions and
        # keeping columns names as is if not present
        # in given transformations 
        exprs = [
            col_name
            if col_name not in cast_transformations
            else cast_transformations[col_name]
            for col_name in schema.names
        ]

        return df.selectExpr(exprs), schema

    return _compose(_rename_columns, _select_expr_columns)