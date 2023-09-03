# Pygametool __init__.py file
# 
# 	AUTHOR: Zoda
#	PROJECT: Pygametools
#
#
"""Pygametools"""


debug_mode=False
"Debug mode enables Warning may usefull"

import os
from . import pygametool



if "PYGAMETOOLS_INFO_HIDE_FLAG" not in os.environ:
	print(f"Pygametools, Base module {pygametool.__version__}, welcome!")

