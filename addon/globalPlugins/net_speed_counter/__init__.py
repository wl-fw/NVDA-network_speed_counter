# Copyright (C) 2025 Wallan
# Autor: Wallan 
# Este código é distribuído sob a licença GNU GPL 2.0

import wx
import globalPluginHandler
import globalVars
import ui
import threading
import addonHandler
import gui
import logHandler
from scriptHandler import script
from .network import medir_velocidade
from .settings import PainelConfiguracoesNetSpeedCounter
from .net_speed_counter import NetSpeedCounterDialog, ErroDialog
from .config import configuracao

addonHandler.initTranslation()

if globalVars.appArgs.secure:
    raise RuntimeError(_("Este complemento não pode ser executado em telas seguras."))  # Tradutores: Mensagem de erro em telas seguras

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    CATEGORIA_NET_SPEED_COUNTER = _("Net Speed Counter")  # Tradutores: Nome da categoria do complemento

    def __init__(self):
        super().__init__()
        self._bloqueio_scripts = threading.Lock()
        self._resultado = None
        self._bloqueio_resultado = threading.Lock()
        
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(PainelConfiguracoesNetSpeedCounter)
        
        logHandler.log.info(_("Complemento Net Speed Counter inicializado com sucesso. Versão 2025.7.3"))  # Tradutores: Mensagem de inicialização do complemento

    def terminate(self):
        try:
            gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(PainelConfiguracoesNetSpeedCounter)
        except:
            pass
        super().terminate()

    def mostrar_erro(self, mensagem):
        if configuracao["Exibicao"].get("mostrarDialogoErros", "True") == "True":
            wx.CallAfter(gui.mainFrame.popupSettingsDialog, ErroDialog, mensagem)
        else:
            ui.message(mensagem)

    @script(
        description=_("Relata a velocidade da internet."),  # Tradutores: Descrição do script para testar velocidade
        gesture="kb:NVDA+shift+x",
        category=CATEGORIA_NET_SPEED_COUNTER
    )
    def script_testar_velocidade_internet(self, gesture):
        with self._bloqueio_scripts:
            try:
                if self._resultado is None:
                    ui.message(_("Testando a velocidade da internet, por favor aguarde..."))  # Tradutores: Mensagem ao iniciar teste de velocidade
                    thread = threading.Thread(target=self._medir_velocidade)
                    thread.daemon = True
                    thread.start()
                else:
                    self._exibir_resultado_dialogo()
            except Exception as e:
                self.mostrar_erro(_("Erro ao testar a velocidade da internet: {}").format(e))  # Tradutores: Mensagem de erro ao testar velocidade

    @script(
        description=_("Abre a interface gráfica do Net Speed Counter."),  # Tradutores: Descrição do script para abrir interface gráfica
        gesture="kb:NVDA+shift+z",
        category=CATEGORIA_NET_SPEED_COUNTER
    )
    def script_abrir_interface_grafica(self, gesture):
        wx.CallAfter(gui.mainFrame.popupSettingsDialog, NetSpeedCounterDialog)

    def _medir_velocidade(self):
        try:
            download, upload, ping, server_info, client_info, bytes_sent, bytes_received, duracao, share_url = medir_velocidade()
            with self._bloqueio_resultado:
                self._resultado = (download, upload, ping, server_info, client_info, bytes_sent, bytes_received, duracao, share_url)
            self._exibir_resultado_dialogo()
        except Exception as e:
            self.mostrar_erro(_("Erro ao medir a velocidade: {}").format(e))  # Tradutores: Mensagem de erro ao medir velocidade

    def _exibir_resultado_dialogo(self):
        if self._resultado:
            download, upload, ping, server_info, client_info, bytes_sent, bytes_received, duracao, share_url = self._resultado
            partes_mensagem = []
            if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
                partes_mensagem.append(_("Download: {:.2f} Mbps").format(download))  # Tradutores: Exibição da velocidade de download
            if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
                partes_mensagem.append(_("Upload: {:.2f} Mbps").format(upload))  # Tradutores: Exibição da velocidade de upload
            if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
                partes_mensagem.append(_("Ping: {:.2f} ms").format(ping))  # Tradutores: Exibição do ping
            if configuracao["Exibicao"].get("mostrarServidor", "True") == "True":
                partes_mensagem.append(_("Servidor: {}").format(server_info['name']))  # Tradutores: Exibição do servidor
            if configuracao["Exibicao"].get("mostrarServidorIP", "True") == "True":
                partes_mensagem.append(_("IP do Servidor: {}").format(server_info.get('host', 'N/A').split(':')[0]))  # Tradutores: Exibição do IP do servidor
            if configuracao["Exibicao"].get("mostrarIPCliente", "True") == "True":
                partes_mensagem.append(_("IP do Cliente: {}").format(client_info['ip']))  # Tradutores: Exibição do IP do cliente
            if configuracao["Exibicao"].get("mostrarBytesEnviados", "True") == "True":
                partes_mensagem.append(_("Bytes Enviados: {}").format(bytes_sent))  # Tradutores: Exibição dos bytes enviados
            if configuracao["Exibicao"].get("mostrarBytesRecebidos", "True") == "True":
                partes_mensagem.append(_("Bytes Recebidos: {}").format(bytes_received))  # Tradutores: Exibição dos bytes recebidos
            if configuracao["Exibicao"].get("mostrarDuracao", "True") == "True":
                partes_mensagem.append(_("Duração do Teste: {:.2f} segundos").format(duracao))  # Tradutores: Exibição da duração do teste
            if configuracao["Exibicao"].get("mostrarShareUrl", "True") == "True":
                partes_mensagem.append(_("Link de Compartilhamento: {}").format(share_url or 'N/A'))  # Tradutores: Exibição do link de compartilhamento
            mensagem = ", ".join(partes_mensagem) if partes_mensagem else _("Nenhum dado configurado para exibição.")  # Tradutores: Mensagem quando nenhum dado está configurado
            ui.message(mensagem)
            self._resultado = None