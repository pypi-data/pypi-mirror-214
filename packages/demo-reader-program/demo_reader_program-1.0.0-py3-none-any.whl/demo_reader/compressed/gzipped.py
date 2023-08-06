import gzip
from ..util import writer
opener = gzip.open

if __name__ == '__main__':
    '''Use gzip to create compressed file and write data into it'''
    writer.main(opener)