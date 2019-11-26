import Orange

from rdm.db import DBVendor, DBConnection, DBContext, RSDConverter, mapper
from rdm.wrappers import RSD
from rdm.validation import cv_split
from rdm.helpers import arff_to_orange_table

# Provide connection information
connection = DBConnection(
    'ilp',  # User
    'ilp123',  # Password
    'workflow.ijs.si',  # Host
    'imdb_top',  # Database
    vendor=DBVendor.MySQL
)

# Define learning context
context = DBContext(connection, target_table='movies', target_att='quality')

# Cross-validation loop
predictions = []
folds = 10

a = cv_split(context, folds=folds, random_seed=0)

for train_context, test_context in cv_split(context, folds=folds, random_seed=0):
    # Find features on the train set
    conv = RSDConverter(train_context)
    rsd = RSD()
    features, train_arff, _ = rsd.induce(
        conv.background_knowledge(),   # Background knowledge
        examples=conv.all_examples(),  # Training examples
        cn2sd=False                    # Disable built-in subgroup discovery
    )

    a = conv.background_knowledge()
    b = conv.all_examples()

    # Train the classifier on the *train set*
    train_data = arff_to_orange_table(train_arff)
    tree_learner = Orange.classification.TreeLearner(max_depth=5)
    tree_classifier = tree_learner(train_data)

    # Map the *test set* using the features from the train set
    test_arff = mapper.domain_map(features, 'rsd', train_context, test_context, format='arff')

    # Classify the test set
    test_data = arff_to_orange_table(test_arff)
    fold_predictions = [(ex.get_class(), tree_classifier(ex)) for ex in test_data]
    predictions.append(fold_predictions)

acc = 0
for fold_predictions in predictions:
    acc += sum([1.0 for actual, predicted in fold_predictions if actual == predicted]) / len(fold_predictions)
acc = 100 * acc / folds

print('Estimated predictive accuracy: {0:.2f}%'.format(acc))
