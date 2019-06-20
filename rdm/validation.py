import random
import sklearn.model_selection as skl


def cv_split(context, folds=10, random_seed=None):
    '''
    Returns a list of pairs (train_context, test_context), one for each cross-validation fold.

    The split is stratified.

        :param context: DBContext to be split
        :param folds: number of folds
        :param random_seed: random seed to be used

        :return: returns a list of (train_context, test_context) pairs
        :rtype: list

        :Example:

        >>> for train_context, test_context in cv_split(context, folds=10, random_seed=0):
        >>>     pass  # Your CV loop
    '''
    import Orange as orange
    random_seed = random.randint(0, 10**6) if not random_seed else random_seed
    input_list = context.orng_tables.get(context.target_table, None)
    splitter = skl.StratifiedKFold(folds, random_state=random_seed)
    input_listX = [pair[0] for pair in input_list]
    input_listY = range(len(input_list))

    fold_contexts = []
    for train_index, test_index in splitter.split(input_listY, input_listX):
        train = orange.data.Table.from_table_rows(input_list,train_index)
        train_context = context.copy()
        train_context.orng_tables[context.target_table] = train
        test = orange.data.Table.from_table_rows(input_list,test_index)
        test_context = context.copy()
        test_context.orng_tables[context.target_table] = test
        fold_contexts.append((train_context, test_context))

    return fold_contexts
