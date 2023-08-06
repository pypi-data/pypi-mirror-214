
class Loaders:
    """A class to load data from filse of different formats, that doesn't fail when
    modules to load those files don't exist

    THIS IS UNTESTED
    """

    def __init__(self):
        self.opts = {
            'csv': 'pandas.read_csv',
            'csv.gz': 'pandas.read_csv',
            'parquet': 'pandas.read_parquet',
            'fits': 'pyfits.io.fits.getdata',
        }

    def load(self, path):
        filetype = get_filetype(path)

        try:
            importstr = self.opts[filetype]
        except KeyError:
            raise ValueError(f"No loader defined for files of type {filetype}")

        package = ".".join(importstr[:-1])
        __import__(package)
        func = eval(importstr)
        return func(path)


def get_filetype(path):
    tokens = path.split('.')

    # If the suffix is gz, include previous suffix
    if tokens[-1] in "gz bz2".split():
        tokens[-1] = ".".join(tokens[-2:])

    return tokens[-1]

