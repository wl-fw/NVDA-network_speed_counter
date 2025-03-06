# Copyright (C) 2025 Wallan
# Este código é distribuído sob a licença GNU GPL 2.0

import wx
import gui
from gui import guiHelper
from gui.settingsDialogs import SettingsPanel
import addonHandler
from .config import configuracao, ARQUIVO_CONFIG
from .network import obter_servidores_disponiveis

addonHandler.initTranslation()

class PainelConfiguracoesVelocidadeRede(SettingsPanel):
    title = _("Teste de Velocidade da Internet")

    def makeSettings(self, settingsSizer):
        ajudante_sizer = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
        
        # Tradutores: Rótulo para a lista suspensa de seleção de servidor
        self.rotulo_servidor = ajudante_sizer.addItem(wx.StaticText(self, label=_("Selecionar servidor de teste:")))
        self.escolha_servidor = ajudante_sizer.addLabeledControl("", wx.Choice, choices=[])
        self.atualizar_lista_servidores()
        
        # Tradutores: Rótulo para o botão de atualização da lista de servidores
        self.botao_atualizar = ajudante_sizer.addItem(wx.Button(self, label=_("Atualizar lista de servidores")))
        self.botao_atualizar.Bind(wx.EVT_BUTTON, self.ao_atualizar)

        # Tradutores: Rótulo para as opções de exibição dos resultados
        ajudante_sizer.addItem(wx.StaticText(self, label=_("Exibir nos resultados:")))
        self.mostrar_download = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Download")))
        self.mostrar_upload = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Upload")))
        self.mostrar_ping = ajudante_sizer.addItem(wx.CheckBox(self, label=_("Ping")))
        
        self.mostrar_download.SetValue(configuracao["Exibicao"]["mostrarDownload"] == "True")
        self.mostrar_upload.SetValue(configuracao["Exibicao"]["mostrarUpload"] == "True")
        self.mostrar_ping.SetValue(configuracao["Exibicao"]["mostrarPing"] == "True")

    def atualizar_lista_servidores(self):
        try:
            servidores = obter_servidores_disponiveis()
            self.escolha_servidor.Clear()
            for servidor in servidores:
                self.escolha_servidor.Append(f"{servidor['nome']} - {servidor['pais']} ({servidor['distancia']:.2f} km)", servidor['id'])
            servidor_salvo = configuracao["Geral"]["servidorSelecionado"]
            indice = self.escolha_servidor.FindString(servidor_salvo) if servidor_salvo else 0
            self.escolha_servidor.SetSelection(indice if indice != wx.NOT_FOUND else 0)
        except Exception as e:
            # Tradutores: Mensagem de erro exibida quando a lista de servidores não pôde ser carregada
            gui.messageBox(
                _("Erro ao carregar a lista de servidores: {}").format(e),
                # Tradutores: Título do diálogo de erro
                _("Erro"), wx.OK | wx.ICON_ERROR,
                parent=self
            )

    def ao_atualizar(self, evt):
        self.atualizar_lista_servidores()

    def onSave(self):
        try:
            selecionado = self.escolha_servidor.GetClientData(self.escolha_servidor.GetSelection())
            configuracao["Geral"]["servidorSelecionado"] = selecionado
            configuracao["Exibicao"]["mostrarDownload"] = str(self.mostrar_download.GetValue())
            configuracao["Exibicao"]["mostrarUpload"] = str(self.mostrar_upload.GetValue())
            configuracao["Exibicao"]["mostrarPing"] = str(self.mostrar_ping.GetValue())
            configuracao.write()
        except Exception as e:
            # Tradutores: Mensagem de erro exibida quando as configurações não puderam ser salvas
            gui.messageBox(
                _("Erro ao salvar configurações: {}").format(e),
                # Tradutores: Título do diálogo de erro
                _("Erro"), wx.OK | wx.ICON_ERROR,
                parent=self
            )