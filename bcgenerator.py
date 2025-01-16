"""
Script per generare EAN13

Va chiamato passando come argomenti il codice da convertire e il path per l'output

Dipendenze:
pip install python-barcode pillow
"""

from barcode import EAN13_GUARD
import sys
from barcode.writer import ImageWriter


_, number, path_out = sys.argv


my_code = EAN13_GUARD(number, writer=ImageWriter())
my_code.save(path_out)
