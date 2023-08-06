# with this __all__, when we run from demo_reader_program.compressed import *
# the bzipped module and gzipped module will also be imported, but we only want to import the functions,
__all__ = ['bz2_opener', 'gzip_opener']
