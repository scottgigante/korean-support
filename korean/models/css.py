# -*- coding: utf-8 -*-
#
# Copyright © 2012-2014 Thomas Tempe <thomas.tempe@alysse.org>
# Copyright © 2012 Roland Sieker <ospalh@gmail.com>
# Copyright © 2018 Scott Gigante <scottgigante@gmail.com>

"""
CSS used by the different Korean models.
"""

style = u"""\
.card { word-wrap: break-word; }

.win .hanja { font-family: "MS Mincho", "ＭＳ 明朝"; }
.mac .hanja { }
.linux .hanja { font-family: "Kochi Mincho", "東風明朝"; }
.mobile .hanja { font-family: "Hiragino Mincho ProN"; }
.hanja { font-size: 30px; color: rgb(173,122,190) }
.button { font-size: 30px; color: rgb(173,122,190) }

.korean { font-family: "Malgun Gothic", "sans-serif"; font-size: 30px;}

.english { font-size: 20px;}
.comment {font-size: 15px; color:grey;}
.tags {color:gray;text-align:right;font-size:10pt;}
.note {color:gray;font-size:12pt;margin-top:20pt;}
.hint {font-size:12pt;}
.answer { background-color:bisque; border:dotted;border-width:1px}
"""
