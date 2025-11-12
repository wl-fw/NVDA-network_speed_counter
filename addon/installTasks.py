# Copyright (C) 2025 Wallan
# Autor: Wallan
# Este código é distribuído sob a licença GNU GPL 2.0

import os
import globalVars
import gui
from logHandler import log
import wx
import addonHandler
import shutil

addonHandler.initTranslation()

def onInstall():
    oldAddonName = "net_speed_counter"
    oldConfigDir = os.path.join(globalVars.appArgs.configPath, "addons", oldAddonName, "globalPlugins", "net_speed_counter")
    oldConfigPath = os.path.join(oldConfigDir, "net_speed_counter.ini")

    pendingDir = os.path.join(globalVars.appArgs.configPath, "addons", f"{oldAddonName}.pendingInstall", "globalPlugins", "net_speed_counter")
    newConfigPath = os.path.join(pendingDir, "net_speed_counter.ini")

    if os.path.exists(oldConfigPath):
        if gui.messageBox(
            _("Uma versão antiga deste complemento foi detectada.\n\n"
              "Deseja copiar as configurações do complemento antigo?"),
            _("Copiar Configurações"),
            wx.YES_NO | wx.ICON_QUESTION
        ) == wx.YES:
            try:
                os.makedirs(pendingDir, exist_ok=True)
                shutil.copy2(oldConfigPath, newConfigPath)
                log.info("Configurações copiadas do complemento antigo.")
            except Exception as e:
                log.error(f"Erro ao copiar configurações: {e}")
                gui.messageBox(
                    _("Falha ao copiar configurações:\n{0}").format(e),
                    _("Erro"),
                    wx.OK | wx.ICON_ERROR
                )