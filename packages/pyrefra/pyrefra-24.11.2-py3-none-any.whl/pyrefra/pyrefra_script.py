"""
Last modification Nov 25 2024

@author: Hermann Zeyen <hermann.zeyen@universite-paris-saclay.fr>
         Universite Paris-Saclay, France

Wrapper for pyrefra program
"""
import sys
import os
from pathlib import Path
from PyQt5 import QtWidgets

from pyrefra import pyrefra

if __name__ == "__main__":
    dir0 = os.getcwd()

    def my_exception_hook(exctype, value, tracebk):
        """
        Test to capture CTLR-C, but does not work...

        Parameters
        ----------
        exctype : TYPE
            DESCRIPTION.
        value : TYPE
            DESCRIPTION.
        tracebk : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        print(exctype, value, tracebk)
        sys._excepthook(exctype, value, tracebk)
        sys.exit(1)

    if __name__ == "__main__" and __package__ is None:
        file = Path(__file__).resolve()
        parent, top = file.parent, file.parents[0]

        sys.path.append(str(top))
        try:
            sys.path.remove(str(parent))
        except ValueError:  # Already removed
            pass
        if top not in sys.path:
            sys.path.append(top)

        __package__ = "pyrefra"

    try:
        app = QtWidgets.QApplication(sys.argv)
        sys._excepthook = sys.excepthook
        sys.excepthook = my_exception_hook
        main = pyrefra.Main(str(top), dir0)
        main.window.showMaximized()
        sys.exit(app.exec_())
    except Exception as error:
        print(f'An unexpected exception occurred: {error}.')
        #        sys.exit()
        pass
