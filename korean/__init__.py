# -*- coding: utf-8 -*-
# Korean Support; an add-on for Anki <http://ankisrs.net/>

# Copyright 2012 Roland Sieker <ospalh@gmail.com>
# Copyright 2012 Thomas Tempé <thomas.tempe@alysse.org>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# Copyright © 2018 Scott Gigante <scottgigante@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from aqt import mw, addons, gui_hooks
from aqt.utils import showInfo

from . import edit
from .models import advanced
from .models import basic
from .ui import loadMenu
from .migration import run_migrations

gui_hooks.main_window_did_init.append(loadMenu)
gui_hooks.collection_did_load.append(run_migrations)


# hack to force updates
def check_for_updates():
    mgr = mw.addonManager
    for dir in mgr.allAddons():
        if mgr.addonName(dir) == "Korean Support":
            addon_id = dir
            break
    try:
        updated = str(addon_id) in mgr.checkForUpdates()
    except:
        updated = False

    if updated:
        showInfo(
            "An update is available for Korean Support. Please update it by going to Tools -> Addons -> Check for Updates."
        )


gui_hooks.main_window_did_init.append(check_for_updates)
