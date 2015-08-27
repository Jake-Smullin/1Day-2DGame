
import sys
import os
try:
    __file__
except NameError:
    pass
else:
    pygameDir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'pygame'))
    sys.path.insert(0, pygameDir)

sys.path.insert(1, 'pygame')
import driverProgram
driverProgram.main()