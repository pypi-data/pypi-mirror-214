# demo_reader_program/multireader.py
import os

from .compressed import gzipped, bzipped

extension_map = {
    '.bz2' : bzipped.opener,
    '.gz' : gzipped.opener
}
class MultiReader:
    def __init__(self, filename):
        extension = os.path.splitext(filename)[1]
        opener = extension_map.get(extension, open)
        self.filename = filename
        self.f = opener(filename, 'rt') # open the file to read in text mode

    def close(self):
        self.f.close()

    def read(self):
        return self.f.read() # return the entire conent of the text file as a str