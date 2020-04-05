# -*- coding: utf-8 -*-
#
# Copyright © 2012 Thomas Tempe <thomas.tempe@alysse.org>
# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
# Copyright © 2018 Scott Gigante <scottgigante@gmail.com>
#
# Original: Damien Elmes <anki@ichi2.net> (as japanese/model.py)
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

import anki.stdmodels
from .css import style
from .card_fields import (
    hanja_button,
    deck_tags,
    korean,
    english,
    sound,
    front_side,
    silhouette,
    comment,
)


# List of fields
######################################################################

fields_list = ["Korean", "English", "Hanja", "Sound", "Silhouette", "Comment"]

# Card templates
######################################################################

recognition_front = u"\n<br>".join([deck_tags, korean])

recall_front = u"\n<br>".join([deck_tags, english, silhouette])

recognition_back = u"\n<br>".join([front_side, english, sound, hanja_button, comment])

recall_back = u"\n<br>".join([front_side, korean, sound, hanja_button, comment])


# Add model for korean word to Anki
######################################################################

model_name = "Korean (advanced)"


def add_model(col):
    mm = col.models
    m = mm.new(model_name)
    # Add fields
    for f in fields_list:
        fm = mm.newField(f)
        mm.addField(m, fm)
    t = mm.newTemplate(u"Recognition")
    t["qfmt"] = recognition_front
    t["afmt"] = recognition_back
    mm.addTemplate(m, t)
    t = mm.newTemplate(u"Recall")
    t["qfmt"] = recall_front
    t["afmt"] = recall_back
    mm.addTemplate(m, t)

    m["css"] += style
    m["addon"] = model_name
    mm.add(m)
    # recognition card
    return m


anki.stdmodels.models.append((model_name, add_model))
