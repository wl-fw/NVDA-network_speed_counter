# Copyright (C) 2025 Wallan
# Autor: Wallan
# Este código é distribuído sob a licença GNU GPL 2.0

import wx
import gui
from gui import guiHelper
import addonHandler
from .config import configuracao, salvar_configuracao, carregar_configuracao
import logging
addonHandler.initTranslation()
class PainelConfiguracoesNetSpeedCounter(gui.settingsDialogs.SettingsPanel):
    title = _("Configurações do Net Speed Counter")
    def makeSettings(self, settingsSizer):
        try:
            carregar_configuracao()
            ajudante_sizer = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
           
            self.mostrar_data = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Data")))
            self.mostrar_data.SetValue(configuracao["Exibicao"].get("mostrarData", "True") == "True")
           
            self.mostrar_download = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Download")))
            self.mostrar_download.SetValue(configuracao["Exibicao"].get("mostrarDownload", "True") == "True")
           
            self.mostrar_upload = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Upload")))
            self.mostrar_upload.SetValue(configuracao["Exibicao"].get("mostrarUpload", "True") == "True")
           
            self.mostrar_ping = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Ping")))
            self.mostrar_ping.SetValue(configuracao["Exibicao"].get("mostrarPing", "True") == "True")
           
            self.mostrar_servidor = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Servidor")))
            self.mostrar_servidor.SetValue(configuracao["Exibicao"].get("mostrarServidor", "True") == "True")
           
            self.mostrar_servidor_id = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar ID do Servidor")))
            self.mostrar_servidor_id.SetValue(configuracao["Exibicao"].get("mostrarServidorID", "True") == "True")
           
            self.mostrar_servidor_ip = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar IP do Servidor")))
            self.mostrar_servidor_ip.SetValue(configuracao["Exibicao"].get("mostrarServidorIP", "True") == "True")
           
            self.mostrar_servidor_patrocinador = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Patrocinador do Servidor")))
            self.mostrar_servidor_patrocinador.SetValue(configuracao["Exibicao"].get("mostrarServidorPatrocinador", "True") == "True")
           
            self.mostrar_servidor_localizacao = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Localização do Servidor")))
            self.mostrar_servidor_localizacao.SetValue(configuracao["Exibicao"].get("mostrarServidorLocalizacao", "True") == "True")
           
            self.mostrar_servidor_distancia = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Distância do Servidor")))
            self.mostrar_servidor_distancia.SetValue(configuracao["Exibicao"].get("mostrarServidorDistancia", "True") == "True")
           
            self.mostrar_servidor_url = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar URL do Servidor")))
            self.mostrar_servidor_url.SetValue(configuracao["Exibicao"].get("mostrarServidorUrl", "True") == "True")
           
            self.mostrar_ip_cliente = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar IP do Cliente")))
            self.mostrar_ip_cliente.SetValue(configuracao["Exibicao"].get("mostrarIPCliente", "True") == "True")
           
            self.mostrar_isp_cliente = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar ISP do Cliente")))
            self.mostrar_isp_cliente.SetValue(configuracao["Exibicao"].get("mostrarISPCliente", "True") == "True")
           
            self.mostrar_cliente_localizacao = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Localização do Cliente")))
            self.mostrar_cliente_localizacao.SetValue(configuracao["Exibicao"].get("mostrarClienteLocalizacao", "True") == "True")
           
            self.mostrar_bytes_enviados = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Bytes Enviados")))
            self.mostrar_bytes_enviados.SetValue(configuracao["Exibicao"].get("mostrarBytesEnviados", "True") == "True")
           
            self.mostrar_bytes_recebidos = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Bytes Recebidos")))
            self.mostrar_bytes_recebidos.SetValue(configuracao["Exibicao"].get("mostrarBytesRecebidos", "True") == "True")
           
            self.mostrar_duracao = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Duração do Teste")))
            self.mostrar_duracao.SetValue(configuracao["Exibicao"].get("mostrarDuracao", "True") == "True")
           
            self.mostrar_share_url = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Link de Compartilhamento")))
            self.mostrar_share_url.SetValue(configuracao["Exibicao"].get("mostrarShareUrl", "True") == "True")
           
            self.mostrar_threads_download = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Threads de Download")))
            self.mostrar_threads_download.SetValue(configuracao["Exibicao"].get("mostrarThreadsDownload", "True") == "True")
           
            self.mostrar_threads_upload = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Threads de Upload")))
            self.mostrar_threads_upload.SetValue(configuracao["Exibicao"].get("mostrarThreadsUpload", "True") == "True")
           
            self.mostrar_tamanhos_download = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Tamanhos de Download")))
            self.mostrar_tamanhos_download.SetValue(configuracao["Exibicao"].get("mostrarTamanhosDownload", "True") == "True")
           
            self.mostrar_tamanhos_upload = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Mostrar Tamanhos de Upload")))
            self.mostrar_tamanhos_upload.SetValue(configuracao["Exibicao"].get("mostrarTamanhosUpload", "True") == "True")
            self.mostrar_dialogo_erros = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Exibir diálogo em caso de erros")))
            self.mostrar_dialogo_erros.SetValue(configuracao["Exibicao"].get("mostrarDialogoErros", "True") == "True")
        except Exception as e:
            logging.error(f"Erro ao inicializar painel de configurações: {e}")
    def onSave(self):
        try:
            configuracao["Exibicao"]["mostrarData"] = str(self.mostrar_data.GetValue())
            configuracao["Exibicao"]["mostrarDownload"] = str(self.mostrar_download.GetValue())
            configuracao["Exibicao"]["mostrarUpload"] = str(self.mostrar_upload.GetValue())
            configuracao["Exibicao"]["mostrarPing"] = str(self.mostrar_ping.GetValue())
            configuracao["Exibicao"]["mostrarServidor"] = str(self.mostrar_servidor.GetValue())
            configuracao["Exibicao"]["mostrarServidorID"] = str(self.mostrar_servidor_id.GetValue())
            configuracao["Exibicao"]["mostrarServidorIP"] = str(self.mostrar_servidor_ip.GetValue())
            configuracao["Exibicao"]["mostrarServidorPatrocinador"] = str(self.mostrar_servidor_patrocinador.GetValue())
            configuracao["Exibicao"]["mostrarServidorLocalizacao"] = str(self.mostrar_servidor_localizacao.GetValue())
            configuracao["Exibicao"]["mostrarServidorDistancia"] = str(self.mostrar_servidor_distancia.GetValue())
            configuracao["Exibicao"]["mostrarServidorUrl"] = str(self.mostrar_servidor_url.GetValue())
            configuracao["Exibicao"]["mostrarIPCliente"] = str(self.mostrar_ip_cliente.GetValue())
            configuracao["Exibicao"]["mostrarISPCliente"] = str(self.mostrar_isp_cliente.GetValue())
            configuracao["Exibicao"]["mostrarClienteLocalizacao"] = str(self.mostrar_cliente_localizacao.GetValue())
            configuracao["Exibicao"]["mostrarBytesEnviados"] = str(self.mostrar_bytes_enviados.GetValue())
            configuracao["Exibicao"]["mostrarBytesRecebidos"] = str(self.mostrar_bytes_recebidos.GetValue())
            configuracao["Exibicao"]["mostrarDuracao"] = str(self.mostrar_duracao.GetValue())
            configuracao["Exibicao"]["mostrarShareUrl"] = str(self.mostrar_share_url.GetValue())
            configuracao["Exibicao"]["mostrarThreadsDownload"] = str(self.mostrar_threads_download.GetValue())
            configuracao["Exibicao"]["mostrarThreadsUpload"] = str(self.mostrar_threads_upload.GetValue())
            configuracao["Exibicao"]["mostrarTamanhosDownload"] = str(self.mostrar_tamanhos_download.GetValue())
            configuracao["Exibicao"]["mostrarTamanhosUpload"] = str(self.mostrar_tamanhos_upload.GetValue())
            configuracao["Exibicao"]["mostrarDialogoErros"] = str(self.mostrar_dialogo_erros.GetValue())
           
            if not any(configuracao["Exibicao"].get(key, "False") == "True" for key in configuracao["Exibicao"] if key != "mostrarDialogoErros"):
                gui.messageBox(_("Pelo menos uma opção de exibição deve ser selecionada."), _("Erro"), wx.OK | wx.ICON_ERROR)
                return
            salvar_configuracao()
        except Exception as e:
            logging.error(f"Erro ao salvar configurações do painel: {e}")