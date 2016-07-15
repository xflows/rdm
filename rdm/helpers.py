import tempfile
import orange


def arff_to_orange_table(arff):
    '''
    Convert a string in arff format to an Orange table.

        :param arff: string in arff format

        :return: Orange data table object constructed from the arff string
        :rtype: orange.ExampleTable
    '''
    with tempfile.NamedTemporaryFile(suffix='.arff', delete=True) as f:
        f.write(arff)
        f.flush()
        table = orange.ExampleTable(f.name)
        return table
