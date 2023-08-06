import bz2
from ..util import writer # relative import
opener = bz2.open

if __name__ == '__main__':
    writer.main(opener)