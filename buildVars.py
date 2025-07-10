# -*- coding: UTF-8 -*-

def _(arg):
    return arg

addon_info = {
    "addon_name": "net_speed_counter",
    "addon_summary": _("net_speed_counter"),
    "addon_description": _("este complemento permite que, com apenas um click, você possa medir a velocidade de download, upload e laténcia de sua internet."),
    "addon_version": "2025.7.2",
    "addon_author": "Wallan Martins",
    "addon_url": "https://github.com/wl-fw/NVDA-network_speed_counter/",
    "addon_sourceURL": "https://github.com/wl-fw/NVDA-network_speed_counter",
    "addon_docFileName": "readme.html",
    "addon_minimumNVDAVersion": "2023.1",
    "addon_lastTestedNVDAVersion": "2025.1.2",
    "addon_updateChannel": None,
    "addon_license": "GPL v2",
    "addon_licenseURL": "https://www.gnu.org/licenses/gpl-2.0.html",
}

pythonSources = [
    "addon/*.py",
    "addon/globalPlugins/net_speed_counter/*.py"
]

i18nSources = pythonSources + ["buildVars.py"]

excludedFiles = []

baseLanguage = "pt_BR"

markdownExtensions = []

brailleTables = {}
symbolDictionaries = {}
