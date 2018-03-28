#Build in console with
#python setup.py build

import sys
from cx_Freeze import setup, Executable

base = 'Console'
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
		'includes': ['atexit', 'numpy', 'numpy.core._methods', 
					 'numpy.lib.format', 'matplotlib.backends.backend_tkagg',
					 'tkinter', 'tkinter.filedialog']
    }
}

executables = [
    Executable('qtPlotter.py', base=base)
]

setup(name='qtPlotter',
      version='0.1',
      description='Sample matplotlib script',
      executables=executables,
      options=options
      )