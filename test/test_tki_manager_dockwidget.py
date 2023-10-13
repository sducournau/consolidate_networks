# coding=utf-8
"""DockWidget test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'simon.ducournau@circet.fr'
__date__ = '2022-02-25'
__copyright__ = 'Copyright 2022, Simon Ducournau / Circet'

import unittest

from qgis.PyQt.QtGui import QDockWidget

from tki_manager_dockwidget import TkiManagerDockWidget

from utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class TkiManagerDockWidgetTest(unittest.TestCase):
    """Test dockwidget works."""

    def setUp(self):
        """Runs before each test."""
        self.dockwidget = TkiManagerDockWidget(None)

    def tearDown(self):
        """Runs after each test."""
        self.dockwidget = None

    def test_dockwidget_ok(self):
        """Test we can click OK."""
        pass

if __name__ == "__main__":
    suite = unittest.makeSuite(TkiManagerDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

