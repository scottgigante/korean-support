# -*- coding: utf-8 -*-
# Copyright 2012 Thomas TEMPÉ <thomas.tempe@alysse.org>
# Copyright 2017 Luo Li-Yan <joseph.lorimer13@gmail.com>
# Copyright © 2018 Scott Gigante <scottgigante@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt import mw
from aqt.qt import QAction
from aqt.utils import showInfo, openLink, askUser

from .about import CSR_GITHUB_URL, showAbout
from .config import korean_support_config
from .fill_missing import (fill_silhouette,
                           fill_sounds,
                           fill_translation)


ui_actions = {}

dictionaries = [
    ('None', _('None')),
    ('local_en', _('English')),
]

speech_options = [
    'None',
    'Google TTS',
]

msTranslateLanguages = [
    ('Arabic', 'ar'),
    ('Bulgarian', 'bg'),
    ('Catalan', 'ca'),
    ('Czech', 'cs'),
    ('Danish', 'da'),
    ('Dutch', 'nl'),
    ('English', 'en'),
    ('Estonian', 'et'),
    ('Finnish', 'fi'),
    ('French', 'fr'),
    ('German', 'de'),
    ('Greek', 'el'),
    ('Haitian Creole', 'ht'),
    ('Hebrew', 'he'),
    ('Hindi', 'hi'),
    ('Hmong Daw', 'mww'),
    ('Hungarian', 'hu'),
    ('Indonesian', 'id'),
    ('Italian', 'it'),
    ('Japanese', 'ja'),
    ('Korean', 'ko'),
    ('Latvian', 'lv'),
    ('Lithuanian', 'lt'),
    ('Malay', 'ms'),
    ('Norwegian', 'no'),
    ('Persian (Farsi)', 'fa'),
    ('Polish', 'pl'),
    ('Portuguese', 'pt'),
    ('Romanian', 'ro'),
    ('Russian', 'ru'),
    ('Slovak', 'sk'),
    ('Slovenian', 'sl'),
    ('Spanish', 'es'),
    ('Swedish', 'sv'),
    ('Thai', 'th'),
    ('Turkish', 'tr'),
    ('Ukrainian', 'uk'),
    ('Urdu', 'ur'),
    ('Vietnamese ', 'vi')
]


def display_next_tip():
    (tip, link) = korean_support_config.get_next_tip()
    if tip:
        if link:
            if askUser(tip):
                openLink(link)
        else:
            showInfo(tip)


def set_dict_constructor(dict):
    def set_dict():
        korean_support_config.set_option('dictionary', dict)
        update_dict_action_checkboxes()
    return set_dict


def toggle_option_constructor(option):
    def set_option():
        value = not korean_support_config.options[option]
        korean_support_config.set_option(option, value)
        update_dict_action_checkboxes()
    return set_option


def set_option_constructor(option, value):
    def set_option():
        korean_support_config.set_option(option, value)
        update_dict_action_checkboxes()
    return set_option


def add_action(title, to, funct, checkable=False):
    action = QAction(_(title), mw)
    if checkable:
        action.setCheckable(True)
    action.triggered.connect(funct)
    to.addAction(action)
    return action


def update_dict_action_checkboxes():
    global ui_actions

    for d, d_name in dictionaries:
        ui_actions['dict_' + d].setChecked(
            d == korean_support_config.options['dictionary'])

#    for name, code in msTranslateLanguages:
#        ui_actions['dict_' + code].setChecked(
#            code == korean_support_config.options['dictionary'])

    for t in speech_options:
        ui_actions['speech_' + t].setChecked(
            t == korean_support_config.options['speech'])

    ui_actions['debug'].setChecked(korean_support_config.options['debug'])


def loadMenu():
    global ui_actions

    menu = mw.form.menuTools.addMenu('Korean Support')

    submenu = menu.addMenu(_('Use local dictionary'))
    for d, d_names in dictionaries:
        ui_actions['dict_' + d] = add_action(
            d_names, submenu, set_dict_constructor(d), True)

#    submenu = menu.addMenu(_('Use Microsoft Translate'))
#    for name, code in msTranslateLanguages:
#        ui_actions['dict_' + code] = add_action(
#            name, submenu, set_dict_constructor(code), True)

    submenu = menu.addMenu(_('Set speech engine'))
    for i in speech_options:
        ui_actions['speech_' + i] = add_action(
            i, submenu, set_option_constructor('speech', i), True)

    submenu = menu.addMenu(_('Fill incomplete notes'))
    add_action(_('Fill missing sounds'), submenu, fill_sounds)
    add_action(_('Fill translation'), submenu, fill_translation)
    add_action(_('Fill silhouette'), submenu, fill_silhouette)

    submenu = menu.addMenu(_('Help'))
    add_action(_('Report a bug or make a feature request'),
               submenu,
               lambda: openLink(CSR_GITHUB_URL + '/issues'))
    ui_actions['debug'] = add_action(
        _('Debug mode'), submenu, toggle_option_constructor('debug'), True)

    add_action(_('About...'), menu, showAbout)

    update_dict_action_checkboxes()


display_next_tip()
