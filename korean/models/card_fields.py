# -*- coding: utf-8 -*-
#
# Copyright © 2012 Thomas Tempe <thomas.tempe@alysse.org>
# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
# Copyright © 2018 Scott Gigante <scottgigante@gmail.com>
#
# Original: Damien Elmes <anki@ichi2.net> (from japanese/model.py)
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

deck_tags = "<div class=tags>{{Deck}}{{#Tags}} -- {{Tags}}{{/Tags}}</div><br>"

hanja_button = """\
{{#Hanja}}
<button class="button" type="button" onclick="
    if (document.getElementById('hanja').style.display=='none') {
        document.getElementById('hanja').style.display=''
    } else {
        document.getElementById('hanja') .style.display='none'
    }
">
<span class=button>Hanja</span>
</button>
<div class="spoiler" id="hanja" style="display:none">
<span class=hanja>{{Hanja}}</span>
</div>
{{/Hanja}}"""

korean = "<span class=korean>{{Korean}}</span>"

english = "<span class=english>{{English}}</span>"

silhouette = "<div class=korean>{{Silhouette}}</span>"

comment = "<div class=comment>{{Comment}}</span>"

sound = "<!-- {{Sound}}-->"

front_side = """\
{{FrontSide}}
<hr id=answer>
"""
