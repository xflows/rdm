import tempfile
import orange


def arff_to_orange_table(arff):
    with tempfile.NamedTemporaryFile(suffix='.arff', delete=True) as f:
        f.write(arff)
        f.flush()
        table = orange.ExampleTable(f.name)
        return table