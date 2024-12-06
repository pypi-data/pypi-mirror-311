"""
Last modification Nov 25 2024

@author: Hermann Zeyen <hermann.zeyen@universite-paris-saclay.fr>
         Universite Paris-Saclay, France

Wrapper for pyrefra program
"""
import sys
import os
# import unittest
from pathlib import Path
from PyQt5 import QtWidgets
sys.path.append("..")

from pyrefra import Pyrefra

if __name__ == "__main__":
    # unittest.main()
    print("after unittest")
    dir0 = os.getcwd()
    print(f"Folder: {dir0}")

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
        print(f"__file__: {__file__}")
        file = Path(__file__).resolve()
        print(f"file: {file}")
        parent, top = file.parent, file.parents[0]
        print(f"Parent: {parent}, top: {top}")

        sys.path.append(str(top))
        try:
            sys.path.remove(str(parent))
# Already removed
        # except ValueError:
        #     pass
        except Exception as error:
            print(f"sys.path error: {error}.")
            pass
        if top not in sys.path:
            sys.path.append(top)
            print("Top not in path: {sys.path}")

        __package__ = "Pyrefra"
        print("Final path: {sys.path}")

    try:
        app = QtWidgets.QApplication(sys.argv)
        sys._excepthook = sys.excepthook
        sys.excepthook = my_exception_hook
        print(f"Start Main with top={str(top)}, dir0={dir0}")
        main = Pyrefra.Main(str(top), dir0)
        main.window.showMaximized()
        sys.exit(app.exec_())
    except Exception as error:
        print(f'An unexpected exception occurred: {error}.')
        #        sys.exit()
        pass
