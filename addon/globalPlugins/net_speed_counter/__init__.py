# Copyright (C) 2025 Wallan
# Este código é distribuído sob a licença GNU GPL 2.0

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
        
        # Tradutores: Mensagem registrada no log quando o complemento inicia com sucesso
        logHandler.log.info(_("Complemento Teste de Velocidade da Internet inicializado com sucesso. Versão 2025.5.0"))

    def terminate(self):
        try:
            gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(PainelConfiguracoesVelocidadeRede)
        except:
            pass
        super().terminate()

    @script(
        # Tradutores: Descrição do atalho que relata a velocidade da internet
        description=_("Relata a velocidade da internet."),
        gesture="kb:NVDA+shift+x",
        category=CATEGORIA_VELOCIDADE_REDE
    )
    def script_testar_velocidade_internet(self, gesture):
        with self._bloqueio_scripts:
            try:
                if self._resultado is None:
                    # Tradutores: Mensagem falada enquanto testa a velocidade da internet
                    ui.message(_("Testando a velocidade da internet, por favor aguarde..."))
                    thread = threading.Thread(target=self._medir_velocidade)
                    thread.daemon = True
                    thread.start()
                else:
                    self._exibir_resultado_dialogo()

            except Exception as e:
                # Tradutores: Mensagem de erro falada quando o teste de velocidade falha
                ui.message(_("Erro ao testar a velocidade da internet: {}").format(e))

    def _medir_velocidade(self):
        try:
            download, upload, ping = medir_velocidade()
            with self._bloqueio_resultado:
                self._resultado = (download, upload, ping)
            self._exibir_resultado_dialogo()
        except Exception as e:
            # Tradutores: Mensagem de erro falada quando a medição de velocidade falha
            ui.message(_("Erro ao medir a velocidade: {}").format(e))

    def _exibir_resultado_dialogo(self):
        from .config import configuracao
        if self._resultado:
            download, upload, ping = self._resultado
            partes_mensagem = []
            if configuracao["Exibicao"]["mostrarDownload"] == "True":
                # Tradutores: Parte da mensagem com a velocidade de download
                partes_mensagem.append(_("Download: {:.2f} Mbps").format(download))
            if configuracao["Exibicao"]["mostrarUpload"] == "True":
                # Tradutores: Parte da mensagem com a velocidade de upload
                partes_mensagem.append(_("Upload: {:.2f} Mbps").format(upload))
            if configuracao["Exibicao"]["mostrarPing"] == "True":
                # Tradutores: Parte da mensagem com o ping
                partes_mensagem.append(_("Ping: {:.2f} ms").format(ping))
            mensagem = ", ".join(partes_mensagem) if partes_mensagem else _("Nenhum dado configurado para exibição.")
            ui.message(mensagem)
            self._resultado = None