PyRegistry
===============

A windows registry script generator written in pure Python. 

The uninstallation implementations of many softwares are careless, leaving a large number of outdated keys in the system registry.
Although some software in the AppStore claims that they can implement one click cleaning, their function implementation of is opaque and inflexible to advanced users.
PyWinRegistry is a program written in pure Python. It conceptually divides registry cleaning into three steps: PyWinRegistry automatically generates '.reg' scripts, the user reviews the generated items, and the user manually performs the deletion operation by simply right-click 'merge into system registry'. Users can control the whole process. In addition, the PyWinRegistry also provides a recovery '.reg' script to deal with accidents.
Features

.. code-block:: python

   # install via pypi.org
   python -m pip install pywinregistry

   # or install from github.com
   git clone https://github.com/songs18/PyWinRegistry.git
   python -m pip install ./PyWinRegistry

   import pywinregistry
   # this will generate .reg script.
   pywinregistry.query('keyword') 

