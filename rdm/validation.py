import random


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
    import orange
    random_seed = random.randint(0, 10**6) if not random_seed else random_seed
    input_list = context.orng_tables.get(context.target_table, None)
    indices = orange.MakeRandomIndicesCV(input_list, randseed=random_seed, folds=folds,
                                         stratified=orange.MakeRandomIndices.Stratified)

    fold_contexts = []
    for i in range(folds):
        train = input_list.select(indices, i, negate=1)
        test = input_list.select(indices, i)
        train.name = input_list.name
        test.name = input_list.name
        train_context = context.copy()
        train_context.orng_tables[context.target_table] = train
        test_context = context.copy()
        test_context.orng_tables[context.target_table] = test
        fold_contexts.append((train_context, test_context))

    return fold_contexts
