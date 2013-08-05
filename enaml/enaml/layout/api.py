#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import os

if os.environ.get('ENAML_DEPRECATED_DOCK_LAYOUT'):
    from .dock_layout import (
        dockitem, docktabs, docksplit, hdocksplit, vdocksplit, dockarea, docklayout
    )
else:
    from .dock_layout import (
        ItemLayout, TabLayout, SplitLayout, HSplitLayout, VSplitLayout,
        DockBarLayout, AreaLayout, DockLayout, DockLayoutWarning,
        InsertItem, InsertBorderItem, InsertDockBarItem, InsertTab,
        FloatItem, FloatArea, RemoveItem, ExtendItem, RetractItem
    )
from .layout_helpers import (
    align, hbox, vbox, horizontal, vertical, grid, spacer,
)
from .geometry import Box, BoxF, Pos, PosF, Rect, RectF, Size, SizeF
