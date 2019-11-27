import random

import Orange


def cv_split(context, folds=10, random_seed=None, stratified=True):
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
    random_seed = random.randint(0, 10**6) if random_seed is None else random_seed
    input_list = context.orng_tables.get(context.target_table, None)

    # indices = Orange.MakeRandomIndicesCV(input_list, randseed=random_seed, folds=folds,
    #                                      stratified=orange.MakeRandomIndices.Stratified)
    # indices = Orange.data.sample.SubsetIndicesCV(input_list, randseed=random_seed, folds=folds,
    #                                              stratified=Orange.data.sample.SubsetIndices.Stratified)
    cv = Orange.evaluation.CrossValidation(k=folds, random_state=random_seed, stratified=stratified)
    cv_indices = cv.get_indices(input_list)

    fold_contexts = []
    for i in range(folds):
        train_indices = cv_indices[i][0]
        test_indices = cv_indices[i][1]

        train = input_list[train_indices]
        test = input_list[test_indices]
        train.name = input_list.name
        test.name = input_list.name
        train_context = context.copy()
        train_context.orng_tables[context.target_table] = train
        test_context = context.copy()
        test_context.orng_tables[context.target_table] = test
        fold_contexts.append((train_context, test_context))

    return fold_contexts
