import globalPluginHandler
import ui
import threading
import addonHandler
from scriptHandler import script
from .network import medir_velocidade

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    
    CATEGORIA_NET_SPEED = _("Teste de Velocidade da Internet")

    def __init__(self):
        super().__init__()
        self._lock_scripts = threading.Lock()
        self._resultado = None
        self._lock_resultado = threading.Lock()

    @script(
        description=_("Relata a velocidade da internet."),
        gesture="kb:insert+shift+x",
        category=CATEGORIA_NET_SPEED
    )
    def script_testar_velocidade_internet(self, gesture):
        with self._lock_scripts:
            try:
                if self._resultado is None:
                    ui.message(_("Testando a velocidade da internet, aguarde..."))
                    thread = threading.Thread(target=self._medir_velocidade)
                    thread.daemon = True
                    thread.start()
                else:
                    self._mostrar_resultado_dialogo()

            except Exception as e:
                ui.message(_("Erro ao testar a velocidade da internet: {}").format(e))

    def _medir_velocidade(self):
        try:
            download, upload, ping = medir_velocidade()
            with self._lock_resultado:
                self._resultado = (download, upload, ping)
            self._mostrar_resultado_dialogo()
        except Exception as e:
            ui.message(_("Erro ao medir a velocidade: {}").format(e))

    def _mostrar_resultado_dialogo(self):
        if self._resultado:
            download, upload, ping = self._resultado
            mensagem = _(
                "Velocidade da internet: Download: {:.2f} Mbps, Upload: {:.2f} Mbps, Ping: {:.2f} ms."
            ).format(download, upload, ping)
            ui.message(mensagem)
            self._resultado = None
