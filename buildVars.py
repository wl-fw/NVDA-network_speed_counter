import os.path

addon_info = {
    "addon_name": "network_speed_counter",
    "addon_summary": "Network Speed Counter",
    "addon_description": "Este complemento permite que, com apenas um clique, você possa medir a velocidade de download, upload e latência de sua internet.",
    "addon_version": "2025.3.1",
    "addon_author": "Wallan <wallandacosta@gmail.com>",
    "addon_url": "https://palaciodecristal.ddns.net",
    "addon_license": "GPL-2.0",
    "addon_updateChannel": "Beta",
    "addon_minimumNVDAVersion": "2024.1.0",
    "addon_lastTestedNVDAVersion": "2025.1.0",
}

pythonSources = [
    os.path.join("addon", "globalPlugins", "net_speed_counter", "*.py"),
]

i18nSources = pythonSources

packageFiles = {}

docFileName = "readme.md"

# Define markdownExtensions for Markdown processing
markdownExtensions = []  # Empty list for default Markdown behavior

# Define excludedFiles to specify files to exclude from the add-on bundle
excludedFiles = ["*.nvda-addon"]  # Empty list if no exclusions are needed
# Example: excludedFiles = ["*.pyc", "temp/*"]  # Exclude Python bytecode and temp directory

brailleTables = {}
symbolDictionaries = {}

baseLanguage = "pt_BR"