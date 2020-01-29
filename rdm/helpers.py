import arff
import Orange


def arffheader2domain(header, target_idx=[-1]):
    '''
    Constructs Orange.data.Domain from ARFF header.
    See https://www.cs.waikato.ac.nz/~ml/weka/arff.html

    Parameters
    ----------
    header : dict
        ARFF header as returned by the ``arff.load`` function
    classes_idx : list, optional
        List of indices of target attributes. The default is [-1] (last attribute is the class)

    Returns
    -------
    Orange.data.Domain

    '''
    varlist = []
    classes = []
    metas = []
    for aname, atype in header:
        if isinstance(atype, list):
            atype = [x for x in atype if x not in [None, '']]
            var = Orange.data.DiscreteVariable(name=aname, values=atype)
        else:
            atype = atype.lower()
            if atype in ['numeric', 'real', 'float', 'double']:
                var = Orange.data.ContinuousVariable(name=aname)
            elif atype in ['date']:
                var = Orange.data.TimeVariable(name=aname)
            elif atype in ['string', 'text']:
                var = Orange.data.StringVariable(name=aname)
            elif atype in ['integer', 'int']:
                var = Orange.data.ContinuousVariable(name=aname)
            else:
                var = Orange.data.StringVariable(name=aname)
        if isinstance(var, Orange.data.StringVariable):
            metas.append(var)
        varlist.append(var)

    for cid in target_idx:
        classes.append(varlist[cid])
    for cl in classes:
        varlist.remove(cl)
    for meta in metas:
        varlist.remove(meta)
    return Orange.data.Domain(varlist, class_vars=classes, metas=metas)


def arff_to_orange_table(arff_data):
    '''
    Constructs Orange.data.Table from ARFF data stored in a string

    Parameters
    ----------
    arff_data : str
        ARFF file stored in a string.
    Returns
    -------
    table : Orange.data.Table
        Orange data table with the given domain and data. String attributes are stored as meta attributes.

    '''
    arff_description = arff.loads(arff_data)
    domain = arffheader2domain(arff_description['attributes'])
    table = Orange.data.Table.from_list(domain, arff_description['data'])
    table.name = arff_description['relation']
    return table
