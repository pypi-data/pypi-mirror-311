"""
dashi documentations goes here
"""

__version__ = "2.0.1"

from . import histfactory as factory
from .fitting import model,gaussian,poly,leastsq #,poissonllh 
from .visual import visual
from .storage import histsave,histload
from .objbundle import bundle, emptybundle, bundleize

from . import junkbox

import logging
logging.basicConfig(level=logging.INFO)

from . import tests
