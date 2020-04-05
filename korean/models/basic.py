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
from .card_fields import hanja_button, deck_tags, korean, english, sound, front_side

# List of fields
######################################################################

fields_list = ["Korean", "English", "Hanja", "Sound"]

# Card templates
######################################################################

recognition_front = u"\n<br>".join([deck_tags, korean])

recall_front = u"\n<br>".join([deck_tags, english])

recognition_back = u"\n<br>".join([front_side, english, sound, hanja_button])

recall_back = u"\n<br>".join([front_side, korean, sound, hanja_button])


# Add model for chinese word to Anki
######################################################################

model_name = "Korean (basic)"


def add_model_simp(col):
    model = col.models.new(model_name)
    # Add fields
    for field_name in fields_list:
        field = col.models.newField(field_name)
        col.models.addField(model, field)
    # recognition card
    t = col.models.newTemplate(u"Recognition")
    t["qfmt"] = recognition_front
    t["afmt"] = recognition_back
    col.models.addTemplate(model, t)
    # recall card
    t = col.models.newTemplate(u"Recall")
    t["qfmt"] = recall_front
    t["afmt"] = recall_back
    col.models.addTemplate(model, t)

    model["css"] += style
    model["addon"] = model_name
    col.models.add(model)
    return model


anki.stdmodels.models.append((model_name, add_model_simp))
