#Copyright (C) 2025 Wallan
#Este código é distribuído sob a licença GNU GPL 2.0
import globalPluginHandler
import globalVars
import ui
import threading
import addonHandler
import gui
import logHandler
from scriptHandler import script
from .network import medir_velocidade
from .settings import PainelConfiguracoesVelocidadeRede
from .net_speed_counter import NetSpeedCounterDialog
from .config import configuracao

addonHandler.initTranslation()

if globalVars.appArgs.secure:
    raise RuntimeError(_("Este complemento não pode ser executado em telas seguras."))

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    
    CATEGORIA_VELOCIDADE_REDE = _("Teste de Velocidade da Internet")

    def __init__(self):
        super().__init__()
        self._bloqueio_scripts = threading.Lock()
        self._resultado = None
        self._bloqueio_resultado = threading.Lock()
        
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(PainelConfiguracoesVelocidadeRede)
        
        logHandler.log.info(_("Complemento Teste de Velocidade da Internet inicializado com sucesso. Versão 2025.7.0"))

    def terminate(self):
        try:
            gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(PainelConfiguracoesVelocidadeRede)
        except:
            pass
        super().terminate()

    @script(
        description=_("Relata a velocidade da internet."),
        gesture="kb:NVDA+shift+x",
        category=CATEGORIA_VELOCIDADE_REDE
    )
    def script_testar_velocidade_internet(self, gesture):
        with self._bloqueio_scripts:
            try:
                if self._resultado is None:
                    ui.message(_("Testando a velocidade da internet, por favor aguarde..."))
                    thread = threading.Thread(target=self._medir_velocidade)
                    thread.daemon = True
                    thread.start()
                else:
                    self._exibir_resultado_dialogo()
            except Exception as e:
                ui.message(_("Erro ao testar a velocidade da internet: {}").format(e))

    @script(
        description=_("Abre a interface gráfica do Contador de Velocidade da Rede."),
        gesture="kb:NVDA+shift+z",
        category=CATEGORIA_VELOCIDADE_REDE
    )
    def script_abrir_interface_grafica(self, gesture):
        gui.mainFrame.popupSettingsDialog(NetSpeedCounterDialog)

    def _medir_velocidade(self):
        try:
            download, upload, ping, server_info, client_info, bytes_sent, bytes_received, duracao, share_url = medir_velocidade()
            with self._bloqueio_resultado:
                self._resultado = (download, upload, ping, server_info, client_info, bytes_sent, bytes_received, duracao, share_url)
            self._exibir_resultado_dialogo()
        except Exception as e:
            ui.message(_("Erro ao medir a velocidade: {}").format(e))

    def _exibir_resultado_dialogo(self):
        if self._resultado:
            download, upload, ping, server_info, client_info, bytes_sent, bytes_received, duracao, share_url = self._resultado
            partes_mensagem = []
            if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
                partes_mensagem.append(_("Download: {:.2f} Mbps").format(download))
            if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
                partes_mensagem.append(_("Upload: {:.2f} Mbps").format(upload))
            if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
                partes_mensagem.append(_("Ping: {:.2f} ms").format(ping))
            if configuracao["Exibicao"].get("mostrarServidor", "True") == "True":
                partes_mensagem.append(_("Servidor: {}").format(server_info['name']))
            if configuracao["Exibicao"].get("mostrarServidorIP", "True") == "True":
                partes_mensagem.append(_("IP do Servidor: {}").format(server_info.get('host', 'N/A').split(':')[0]))
            if configuracao["Exibicao"].get("mostrarIPCliente", "True") == "True":
                partes_mensagem.append(_("IP do Cliente: {}").format(client_info['ip']))
            if configuracao["Exibicao"].get("mostrarBytesEnviados", "True") == "True":
                partes_mensagem.append(_("Bytes Enviados: {}").format(bytes_sent))
            if configuracao["Exibicao"].get("mostrarBytesRecebidos", "True") == "True":
                partes_mensagem.append(_("Bytes Recebidos: {}").format(bytes_received))
            if configuracao["Exibicao"].get("mostrarDuracao", "True") == "True":
                partes_mensagem.append(_("Duração do Teste: {:.2f} segundos").format(duracao))
            if configuracao["Exibicao"].get("mostrarShareUrl", "True") == "True":
                partes_mensagem.append(_("Link de Compartilhamento: {}").format(share_url or 'N/A'))
            mensagem = ", ".join(partes_mensagem) if partes_mensagem else _("Nenhum dado configurado para exibição.")
            ui.message(mensagem)
            self._resultado = None