# Copyright (C) 2025 Wallan
# Autor: Wallan
# Este código é distribuído sob a licença GNU GPL 2.0
import wx
import gui
from gui import guiHelper
import addonHandler
from .network import obter_servidores_disponiveis, medir_velocidade, obter_historico, terminar, reiniciar
from .config import configuracao
import ui
import sys
import os
import threading
addonHandler.initTranslation()
try:
    sys.path.insert(0, os.path.dirname(__file__))
    import pyperclip
except ImportError:
    try:
        import pyperclip as external_pyperclip
        pyperclip = external_pyperclip
    except ImportError:
        pyperclip = None
class ErroDialog(wx.Dialog):
    def __init__(self, parent, mensagem_erro):
        super().__init__(parent, title=_("Erro no Net Speed Counter"))
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        ajudante_sizer = guiHelper.BoxSizerHelper(self, sizer=main_sizer)
        self.texto_erro = ajudante_sizer.addItem(wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 150)))
        self.texto_erro.SetValue(mensagem_erro)
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)
        self.botao_copiar = wx.Button(self, label=_("Copiar Erro"))
        self.botao_copiar.Bind(wx.EVT_BUTTON, self.on_copiar)
        sizer_botoes.Add(self.botao_copiar, 0, wx.ALL, 5)
        self.botao_fechar = wx.Button(self, label=_("Fechar"))
        self.botao_fechar.Bind(wx.EVT_BUTTON, self.on_fechar)
        sizer_botoes.Add(self.botao_fechar, 0, wx.ALL, 5)
        ajudante_sizer.addItem(sizer_botoes, flag=wx.ALIGN_RIGHT)
        self.SetSizer(main_sizer)
        self.Fit()
        self.botao_fechar.SetFocus()
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)
    def on_copiar(self, evt):
        if pyperclip:
            pyperclip.copy(self.texto_erro.GetValue())
            ui.message(_("Erro copiado para a área de transferência."))
        else:
            ui.message(_("Erro: Pyperclip não encontrado."))
    def on_fechar(self, evt):
        self.Close()
    def on_key_press(self, evt):
        if evt.GetKeyCode() == wx.WXK_ESCAPE or (evt.AltDown() and evt.GetKeyCode() == wx.WXK_F4):
            self.Close()
        else:
            evt.Skip()
class DetalhesTesteDialog(wx.Dialog):
    def __init__(self, parent, entrada):
        super().__init__(parent, title=_("Detalhes do Teste - Net Speed Counter"))
        self.entrada = entrada
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        ajudante_sizer = guiHelper.BoxSizerHelper(self, sizer=main_sizer)
        detalhes = []
        if configuracao["Exibicao"].get("mostrarData", "True") == "True":
            detalhes.append(_("Data: {}").format(entrada.get('Data', 'N/A')))
        if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
            detalhes.append(_("Download: {} Mbps").format(entrada.get('Download', 'N/A')))
        if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
            detalhes.append(_("Upload: {} Mbps").format(entrada.get('Upload', 'N/A')))
        if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
            detalhes.append(_("Ping: {} ms").format(entrada.get('Ping', 'N/A')))
        if configuracao["Exibicao"].get("mostrarServidor", "True") == "True":
            detalhes.append(_("Servidor: {}").format(entrada.get('Servidor', 'N/A')))
        if configuracao["Exibicao"].get("mostrarServidorID", "True") == "True":
            detalhes.append(_("ID do Servidor: {}").format(entrada.get('ServidorID', 'N/A')))
        if configuracao["Exibicao"].get("mostrarServidorIP", "True") == "True":
            detalhes.append(_("IP do Servidor: {}").format(entrada.get('ServidorIP', 'N/A')))
        if configuracao["Exibicao"].get("mostrarServidorPatrocinador", "True") == "True":
            detalhes.append(_("Patrocinador do Servidor: {}").format(entrada.get('ServidorPatrocinador', 'N/A')))
        if configuracao["Exibicao"].get("mostrarServidorLocalizacao", "True") == "True":
            detalhes.append(_("Localização do Servidor: Lat {} / Lon {}").format(entrada.get('ServidorLat', 'N/A'), entrada.get('ServidorLon', 'N/A')))
        if configuracao["Exibicao"].get("mostrarServidorDistancia", "True") == "True":
            detalhes.append(_("Distância do Servidor: {:.2f} km ({:.0f} metros)").format(float(entrada.get('ServidorDistanciaKm', 0)), float(entrada.get('ServidorDistanciaM', 0))))
        if configuracao["Exibicao"].get("mostrarServidorUrl", "True") == "True":
            detalhes.append(_("URL do Servidor: {}").format(entrada.get('ServidorUrl', 'N/A')))
        if configuracao["Exibicao"].get("mostrarIPCliente", "True") == "True":
            detalhes.append(_("IP do Cliente: {}").format(entrada.get('IP', 'N/A')))
        if configuracao["Exibicao"].get("mostrarISPCliente", "True") == "True":
            detalhes.append(_("ISP do Cliente: {}").format(entrada.get('ISP', 'N/A')))
        if configuracao["Exibicao"].get("mostrarClienteLocalizacao", "True") == "True":
            detalhes.append(_("Localização do Cliente: Lat {} / Lon {}").format(entrada.get('ClientLat', 'N/A'), entrada.get('ClientLon', 'N/A')))
        if configuracao["Exibicao"].get("mostrarBytesEnviados", "True") == "True":
            detalhes.append(_("Bytes Enviados: {} bytes ({:.2f} MB)").format(entrada.get('BytesEnviados', 0), float(entrada.get('BytesEnviados', 0)) / 1_000_000))
        if configuracao["Exibicao"].get("mostrarBytesRecebidos", "True") == "True":
            detalhes.append(_("Bytes Recebidos: {} bytes ({:.2f} MB)").format(entrada.get('BytesRecebidos', 0), float(entrada.get('BytesRecebidos', 0)) / 1_000_000))
        if configuracao["Exibicao"].get("mostrarDuracao", "True") == "True":
            detalhes.append(_("Duração do Teste: {} segundos").format(entrada.get('Duracao', 'N/A')))
        if configuracao["Exibicao"].get("mostrarShareUrl", "True") == "True":
            detalhes.append(_("Link de Compartilhamento: {}").format(entrada.get('ShareUrl', 'N/A')))
        if configuracao["Exibicao"].get("mostrarThreadsDownload", "True") == "True":
            detalhes.append(_("Threads de Download: {}").format(entrada.get('ThreadsDownload', 'N/A')))
        if configuracao["Exibicao"].get("mostrarThreadsUpload", "True") == "True":
            detalhes.append(_("Threads de Upload: {}").format(entrada.get('ThreadsUpload', 'N/A')))
        if configuracao["Exibicao"].get("mostrarTamanhosDownload", "True") == "True":
            detalhes.append(_("Tamanhos de Download: {} bytes").format(entrada.get('TamanhosDownload', 'N/A')))
        if configuracao["Exibicao"].get("mostrarTamanhosUpload", "True") == "True":
            detalhes.append(_("Tamanhos de Upload: {} bytes").format(entrada.get('TamanhosUpload', 'N/A')))
        self.texto_detalhes = ajudante_sizer.addItem(wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, size=(-1, 300)))
        self.texto_detalhes.SetValue("\n".join(detalhes) if detalhes else _("Nenhum dado configurado para exibição."))
        self.texto_detalhes.SetInsertionPoint(0)
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)
        self.botao_novo_teste = wx.Button(self, label=_("Novo Teste"))
        self.botao_novo_teste.Bind(wx.EVT_BUTTON, self.on_novo_teste)
        sizer_botoes.Add(self.botao_novo_teste, 0, wx.ALL, 5)
        self.botao_copiar = wx.Button(self, label=_("Copiar Informações"))
        self.botao_copiar.Bind(wx.EVT_BUTTON, self.on_copiar)
        sizer_botoes.Add(self.botao_copiar, 0, wx.ALL, 5)
        self.botao_fechar = wx.Button(self, label=_("Fechar"))
        self.botao_fechar.Bind(wx.EVT_BUTTON, self.on_fechar)
        sizer_botoes.Add(self.botao_fechar, 0, wx.ALL, 5)
        ajudante_sizer.addItem(sizer_botoes, flag=wx.ALIGN_RIGHT)
        self.SetSizer(main_sizer)
        self.Fit()
        self.botao_novo_teste.SetFocus()
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)
        self.Bind(wx.EVT_CLOSE, self.on_fechar)
    def on_novo_teste(self, evt):
        self.Close()
        wx.CallAfter(self.GetParent().on_testar, None)
    def on_copiar(self, evt):
        entrada = self.entrada
        detalhes = []
        if configuracao["Exibicao"].get("mostrarData", "True") == "True":
            detalhes.append(_("Data: {}").format(entrada.get('Data', 'N/A')))
        if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
            detalhes.append(_("Download: {} Mbps").format(entrada.get('Download', 'N/A')))
        if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
            detalhes.append(_("Upload: {} Mbps").format(entrada.get('Upload', 'N/A')))
        if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
            detalhes.append(_("Ping: {} ms").format(entrada.get('Ping', 'N/A')))
        if configuracao["Exibicao"].get("mostrarServidor", "True") == "True":
            detalhes.append(_("Servidor: {}").format(entrada.get('Servidor', 'N/A')))
        if configuracao["Exibicao"].get("mostrarServidorID", "True") == "True":
            detalhes.append(_("ID do Servidor: {}").format(entrada.get('ServidorID', 'N/A')))
        if configuracao["Exibicao"].get("mostrarServidorIP", "True") == "True":
            detalhes.append(_("IP do Servidor: {}").format(entrada.get('ServidorIP', 'N/A')))
        if configuracao["Exibicao"].get("mostrarServidorPatrocinador", "True") == "True":
            detalhes.append(_("Patrocinador do Servidor: {}").format(entrada.get('ServidorPatrocinador', 'N/A')))
        if configuracao["Exibicao"].get("mostrarServidorLocalizacao", "True") == "True":
            detalhes.append(_("Localização do Servidor: Lat {} / Lon {}").format(entrada.get('ServidorLat', 'N/A'), entrada.get('ServidorLon', 'N/A')))
        if configuracao["Exibicao"].get("mostrarServidorDistancia", "True") == "True":
            detalhes.append(_("Distância do Servidor: {:.2f} km ({:.0f} metros)").format(float(entrada.get('ServidorDistanciaKm', 0)), float(entrada.get('ServidorDistanciaM', 0))))
        if configuracao["Exibicao"].get("mostrarServidorUrl", "True") == "True":
            detalhes.append(_("URL do Servidor: {}").format(entrada.get('ServidorUrl', 'N/A')))
        if configuracao["Exibicao"].get("mostrarIPCliente", "True") == "True":
            detalhes.append(_("IP do Cliente: {}").format(entrada.get('IP', 'N/A')))
        if configuracao["Exibicao"].get("mostrarISPCliente", "True") == "True":
            detalhes.append(_("ISP do Cliente: {}").format(entrada.get('ISP', 'N/A')))
        if configuracao["Exibicao"].get("mostrarClienteLocalizacao", "True") == "True":
            detalhes.append(_("Localização do Cliente: Lat {} / Lon {}").format(entrada.get('ClientLat', 'N/A'), entrada.get('ClientLon', 'N/A')))
        if configuracao["Exibicao"].get("mostrarBytesEnviados", "True") == "True":
            detalhes.append(_("Bytes Enviados: {} bytes ({:.2f} MB)").format(entrada.get('BytesEnviados', 0), float(entrada.get('BytesEnviados', 0)) / 1_000_000))
        if configuracao["Exibicao"].get("mostrarBytesRecebidos", "True") == "True":
            detalhes.append(_("Bytes Recebidos: {} bytes ({:.2f} MB)").format(entrada.get('BytesRecebidos', 0), float(entrada.get('BytesRecebidos', 0)) / 1_000_000))
        if configuracao["Exibicao"].get("mostrarDuracao", "True") == "True":
            detalhes.append(_("Duração do Teste: {} segundos").format(entrada.get('Duracao', 'N/A')))
        if configuracao["Exibicao"].get("mostrarShareUrl", "True") == "True":
            detalhes.append(_("Link de Compartilhamento: {}").format(entrada.get('ShareUrl', 'N/A')))
        if configuracao["Exibicao"].get("mostrarThreadsDownload", "True") == "True":
            detalhes.append(_("Threads de Download: {}").format(entrada.get('ThreadsDownload', 'N/A')))
        if configuracao["Exibicao"].get("mostrarThreadsUpload", "True") == "True":
            detalhes.append(_("Threads de Upload: {}").format(entrada.get('ThreadsUpload', 'N/A')))
        if configuracao["Exibicao"].get("mostrarTamanhosDownload", "True") == "True":
            detalhes.append(_("Tamanhos de Download: {} bytes").format(entrada.get('TamanhosDownload', 'N/A')))
        if configuracao["Exibicao"].get("mostrarTamanhosUpload", "True") == "True":
            detalhes.append(_("Tamanhos de Upload: {} bytes").format(entrada.get('TamanhosUpload', 'N/A')))
        if pyperclip:
            texto = "\n".join(detalhes) if detalhes else _("Nenhum dado configurado para exibição.")
            pyperclip.copy(texto)
            ui.message(_("Informações copiadas para a área de transferência."))
    def on_fechar(self, evt):
        self.Destroy()
    def on_key_press(self, evt):
        if evt.GetKeyCode() == wx.WXK_ESCAPE or (evt.AltDown() and evt.GetKeyCode() == wx.WXK_F4):
            self.Close()
        else:
            evt.Skip()
class NetSpeedCounterDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title=_("Net Speed Counter"), size=(600, 400))
        reiniciar()
        self._esta_terminado = False
        self.pyperclip = pyperclip
        if not pyperclip:
            if configuracao["Exibicao"].get("mostrarDialogoErros", "True") == "True":
                wx.CallAfter(self.mostrar_erro, _("Erro: Pyperclip não encontrado."))
            else:
                ui.message(_("Erro: Pyperclip não encontrado."))
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        ajudante_sizer = guiHelper.BoxSizerHelper(self, sizer=main_sizer)
        sizer_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        self.botao_testar = wx.Button(self, label=_("Testar Velocidade"))
        self.botao_testar.Bind(wx.EVT_BUTTON, self.on_testar)
        self.botao_testar.SetDefault()
        self.botao_testar.SetToolTip(_("Inicia o teste de velocidade da internet"))
        sizer_horizontal.Add(self.botao_testar, 0, wx.ALL, 5)
        self.progresso = wx.Gauge(self, range=100, size=(200, 20))
        self.progresso.SetValue(0)
        sizer_horizontal.Add(self.progresso, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        ajudante_sizer.addItem(sizer_horizontal, proportion=0, flag=wx.EXPAND)
        sizer_servidor = wx.BoxSizer(wx.HORIZONTAL)
        self.rotulo_servidor = wx.StaticText(self, label=_("Selecionar servidor:"))
        sizer_servidor.Add(self.rotulo_servidor, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.escolha_servidor = wx.Choice(self, choices=[])
        sizer_servidor.Add(self.escolha_servidor, 1, wx.ALL | wx.EXPAND, 5)
        self.botao_atualizar = wx.Button(self, label=_("Atualizar Servidores"))
        self.botao_atualizar.Bind(wx.EVT_BUTTON, self.on_atualizar)
        self.botao_atualizar.SetToolTip(_("Atualiza a lista de servidores disponíveis"))
        sizer_servidor.Add(self.botao_atualizar, 0, wx.ALL, 5)
        ajudante_sizer.addItem(sizer_servidor, proportion=0, flag=wx.EXPAND)
        self.rotulo_historico = ajudante_sizer.addItem(wx.StaticText(self, label=_("Histórico de Testes:")))
        self.lista_historico = ajudante_sizer.addItem(wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL, size=(-1, 200)))
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)
        self.botao_copiar = wx.Button(self, label=_("Copiar Informações"))
        self.botao_copiar.Bind(wx.EVT_BUTTON, self.on_copiar)
        self.botao_copiar.SetToolTip(_("Copia as informações do teste selecionado"))
        sizer_botoes.Add(self.botao_copiar, 0, wx.ALL, 5)
        self.botao_copiar_historico = wx.Button(self, label=_("Copiar Histórico"))
        self.botao_copiar_historico.Bind(wx.EVT_BUTTON, self.on_copiar_historico)
        self.botao_copiar_historico.SetToolTip(_("Copia todo o histórico de testes"))
        sizer_botoes.Add(self.botao_copiar_historico, 0, wx.ALL, 5)
        self.botao_fechar = wx.Button(self, label=_("Fechar"))
        self.botao_fechar.Bind(wx.EVT_BUTTON, self.on_fechar)
        sizer_botoes.Add(self.botao_fechar, 0, wx.ALL, 5)
        ajudante_sizer.addItem(sizer_botoes, flag=wx.ALIGN_RIGHT)
        self.atualizar_lista_servidores()
        self.atualizar_colunas_historico()
        self.atualizar_historico()
        self.lista_historico.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_selecionar_historico)
        self.lista_historico.Bind(wx.EVT_SET_FOCUS, self.on_lista_foco)
        self.SetSizer(main_sizer)
        self.Fit()
        self.botao_testar.SetFocus()
        self.SetEscapeId(self.botao_fechar.GetId())
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)
        self.Bind(wx.EVT_CLOSE, self.on_fechar)
    def atualizar_colunas_historico(self):
        self.lista_historico.ClearAll()
        colunas = []
        if configuracao["Exibicao"].get("mostrarData", "True") == "True":
            colunas.append((_("Data"), 150))
        if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
            colunas.append((_("Download (Mbps)"), 100))
        if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
            colunas.append((_("Upload (Mbps)"), 100))
        if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
            colunas.append((_("Ping (ms)"), 80))
        if not colunas:
            self.rotulo_historico.Hide()
            self.lista_historico.Hide()
        else:
            self.rotulo_historico.Show()
            self.lista_historico.Show()
            for i, (titulo, largura) in enumerate(colunas):
                self.lista_historico.InsertColumn(i, titulo, width=largura)
        self.botao_copiar.Enable()
        self.botao_copiar_historico.Enable()
    def atualizar_lista_servidores(self):
        if self._esta_terminado:
            return
        try:
            servidores = obter_servidores_disponiveis()
            self.escolha_servidor.Clear()
            self.escolha_servidor.Append(_(" (Automático)"), "")
            for servidor in servidores[:10]:
                self.escolha_servidor.Append(servidor['nome'], servidor['id'])
            servidor_salvo = configuracao["Geral"].get("servidorSelecionado", "")
            indice = self.escolha_servidor.FindString(servidor_salvo) if servidor_salvo else 0
            self.escolha_servidor.SetSelection(indice if indice != wx.NOT_FOUND else 0)
        except Exception as e:
            self.mostrar_erro(_("Erro ao carregar a lista de servidores: {}").format(e))
    def atualizar_historico(self):
        if self._esta_terminado:
            return
        self.atualizar_colunas_historico()
        historico = obter_historico()
        self.lista_historico.DeleteAllItems()
        if not historico:
            return
        for i, entrada in enumerate(historico):
            col_index = 0
            try:
                if configuracao["Exibicao"].get("mostrarData", "True") == "True":
                    self.lista_historico.InsertItem(i, entrada.get('Data', 'N/A'))
                    col_index += 1
                else:
                    self.lista_historico.InsertItem(i, "")
                if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
                    self.lista_historico.SetItem(i, col_index, entrada.get('Download', 'N/A'))
                    col_index += 1
                if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
                    self.lista_historico.SetItem(i, col_index, entrada.get('Upload', 'N/A'))
                    col_index += 1
                if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
                    self.lista_historico.SetItem(i, col_index, entrada.get('Ping', 'N/A'))
            except Exception as e:
                self.mostrar_erro(_("Erro ao carregar histórico: {}").format(e))
    def on_lista_foco(self, evt):
        if self._esta_terminado:
            return
        evt.Skip()
    def on_testar(self, evt):
        if self._esta_terminado:
            return
        servidor_id = self.escolha_servidor.GetClientData(self.escolha_servidor.GetSelection())
        self.botao_testar.Disable()
        self.botao_copiar.Disable()
        self.botao_copiar_historico.Disable()
        self.botao_atualizar.Disable()
        self.progresso.SetValue(0)
        ui.message(_("Testando a velocidade da internet, por favor aguarde..."))
        def testar():
            try:
                def callback_progresso(valor):
                    if not self._esta_terminado:
                        wx.CallAfter(self.progresso.SetValue, int(valor))
                resultado = medir_velocidade(servidor_id, callback_progresso)
                download, upload, ping, server_info, client_info, bytes_sent, bytes_received, duracao, share_url = resultado
                mensagem = []
                if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
                    mensagem.append(_("Download: {:.2f} Mbps").format(download))
                if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
                    mensagem.append(_("Upload: {:.2f} Mbps").format(upload))
                if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
                    mensagem.append(_("Ping: {:.2f} ms").format(ping))
                if configuracao["Exibicao"].get("mostrarServidor", "True") == "True":
                    mensagem.append(_("Servidor: {}").format(server_info['name']))
                if configuracao["Exibicao"].get("mostrarServidorIP", "True") == "True":
                    mensagem.append(_("IP do Servidor: {}").format(server_info.get('host', 'N/A').split(':')[0]))
                if configuracao["Exibicao"].get("mostrarIPCliente", "True") == "True":
                    mensagem.append(_("IP do Cliente: {}").format(client_info['ip']))
                if configuracao["Exibicao"].get("mostrarBytesEnviados", "True") == "True":
                    mensagem.append(_("Bytes Enviados: {}").format(bytes_sent))
                if configuracao["Exibicao"].get("mostrarBytesRecebidos", "True") == "True":
                    mensagem.append(_("Bytes Recebidos: {}").format(bytes_received))
                if configuracao["Exibicao"].get("mostrarDuracao", "True") == "True":
                    mensagem.append(_("Duração do Teste: {:.2f} segundos").format(duracao))
                if configuracao["Exibicao"].get("mostrarShareUrl", "True") == "True":
                    mensagem.append(_("Link de Compartilhamento: {}").format(share_url or 'N/A'))
                mensagem_final = ", ".join(mensagem) if mensagem else _("Nenhum dado configurado para exibição.")
                if not self._esta_terminado:
                    wx.CallAfter(self.atualizar_historico)
                    wx.CallAfter(ui.message, mensagem_final)
                    wx.CallAfter(self.botao_testar.Enable)
                    wx.CallAfter(self.botao_copiar.Enable)
                    wx.CallAfter(self.botao_copiar_historico.Enable)
                    wx.CallAfter(self.botao_atualizar.Enable)
                    wx.CallAfter(self.progresso.SetValue, 0)
                    wx.CallAfter(self.botao_testar.SetFocus)
            except Exception as e:
                if not self._esta_terminado:
                    wx.CallAfter(self.mostrar_erro, _("Erro ao testar a velocidade: {}").format(e))
                    wx.CallAfter(self.botao_testar.Enable)
                    wx.CallAfter(self.botao_copiar.Enable)
                    wx.CallAfter(self.botao_copiar_historico.Enable)
                    wx.CallAfter(self.botao_atualizar.Enable)
                    wx.CallAfter(self.progresso.SetValue, 0)
                    wx.CallAfter(self.botao_testar.SetFocus)
        thread = threading.Thread(target=testar)
        thread.daemon = True
        thread.start()
    def on_selecionar_historico(self, evt):
        if self._esta_terminado:
            return
        indice = self.lista_historico.GetFirstSelected()
        if indice >= 0:
            historico = obter_historico()
            entrada = historico[indice]
            detalhes_dialog = DetalhesTesteDialog(self, entrada)
            detalhes_dialog.ShowModal()
            detalhes_dialog.Destroy()
            self.botao_testar.SetFocus()
    def on_copiar(self, evt):
        if self._esta_terminado:
            return
        indice = self.lista_historico.GetFirstSelected()
        if indice >= 0:
            historico = obter_historico()
            entrada = historico[indice]
            detalhes = []
            if configuracao["Exibicao"].get("mostrarData", "True") == "True":
                detalhes.append(_("Data: {}").format(entrada.get('Data', 'N/A')))
            if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
                detalhes.append(_("Download: {} Mbps").format(entrada.get('Download', 'N/A')))
            if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
                detalhes.append(_("Upload: {} Mbps").format(entrada.get('Upload', 'N/A')))
            if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
                detalhes.append(_("Ping: {} ms").format(entrada.get('Ping', 'N/A')))
            if configuracao["Exibicao"].get("mostrarServidor", "True") == "True":
                detalhes.append(_("Servidor: {}").format(entrada.get('Servidor', 'N/A')))
            if configuracao["Exibicao"].get("mostrarServidorID", "True") == "True":
                detalhes.append(_("ID do Servidor: {}").format(entrada.get('ServidorID', 'N/A')))
            if configuracao["Exibicao"].get("mostrarServidorIP", "True") == "True":
                detalhes.append(_("IP do Servidor: {}").format(entrada.get('ServidorIP', 'N/A')))
            if configuracao["Exibicao"].get("mostrarServidorPatrocinador", "True") == "True":
                detalhes.append(_("Patrocinador do Servidor: {}").format(entrada.get('ServidorPatrocinador', 'N/A')))
            if configuracao["Exibicao"].get("mostrarServidorLocalizacao", "True") == "True":
                detalhes.append(_("Localização do Servidor: Lat {} / Lon {}").format(entrada.get('ServidorLat', 'N/A'), entrada.get('ServidorLon', 'N/A')))
            if configuracao["Exibicao"].get("mostrarServidorDistancia", "True") == "True":
                detalhes.append(_("Distância do Servidor: {:.2f} km ({:.0f} metros)").format(float(entrada.get('ServidorDistanciaKm', 0)), float(entrada.get('ServidorDistanciaM', 0))))
            if configuracao["Exibicao"].get("mostrarServidorUrl", "True") == "True":
                detalhes.append(_("URL do Servidor: {}").format(entrada.get('ServidorUrl', 'N/A')))
            if configuracao["Exibicao"].get("mostrarIPCliente", "True") == "True":
                detalhes.append(_("IP do Cliente: {}").format(entrada.get('IP', 'N/A')))
            if configuracao["Exibicao"].get("mostrarISPCliente", "True") == "True":
                detalhes.append(_("ISP do Cliente: {}").format(entrada.get('ISP', 'N/A')))
            if configuracao["Exibicao"].get("mostrarClienteLocalizacao", "True") == "True":
                detalhes.append(_("Localização do Cliente: Lat {} / Lon {}").format(entrada.get('ClientLat', 'N/A'), entrada.get('ClientLon', 'N/A')))
            if configuracao["Exibicao"].get("mostrarBytesEnviados", "True") == "True":
                detalhes.append(_("Bytes Enviados: {} bytes ({:.2f} MB)").format(entrada.get('BytesEnviados', 0), float(entrada.get('BytesEnviados', 0)) / 1_000_000))
            if configuracao["Exibicao"].get("mostrarBytesRecebidos", "True") == "True":
                detalhes.append(_("Bytes Recebidos: {} bytes ({:.2f} MB)").format(entrada.get('BytesRecebidos', 0), float(entrada.get('BytesRecebidos', 0)) / 1_000_000))
            if configuracao["Exibicao"].get("mostrarDuracao", "True") == "True":
                detalhes.append(_("Duração do Teste: {} segundos").format(entrada.get('Duracao', 'N/A')))
            if configuracao["Exibicao"].get("mostrarShareUrl", "True") == "True":
                detalhes.append(_("Link de Compartilhamento: {}").format(entrada.get('ShareUrl', 'N/A')))
            if configuracao["Exibicao"].get("mostrarThreadsDownload", "True") == "True":
                detalhes.append(_("Threads de Download: {}").format(entrada.get('ThreadsDownload', 'N/A')))
            if configuracao["Exibicao"].get("mostrarThreadsUpload", "True") == "True":
                detalhes.append(_("Threads de Upload: {}").format(entrada.get('ThreadsUpload', 'N/A')))
            if configuracao["Exibicao"].get("mostrarTamanhosDownload", "True") == "True":
                detalhes.append(_("Tamanhos de Download: {} bytes").format(entrada.get('TamanhosDownload', 'N/A')))
            if configuracao["Exibicao"].get("mostrarTamanhosUpload", "True") == "True":
                detalhes.append(_("Tamanhos de Upload: {} bytes").format(entrada.get('TamanhosUpload', 'N/A')))
            if self.pyperclip:
                texto = "\n".join(detalhes) if detalhes else _("Nenhum dado configurado para exibição.")
                self.pyperclip.copy(texto)
                ui.message(_("Informações copiadas para a área de transferência."))
            else:
                self.mostrar_erro(_("Erro: pyperclip não encontrado."))
        else:
            ui.message(_("Nenhum teste selecionado para copiar."))
        self.botao_testar.SetFocus()
    def on_copiar_historico(self, evt):
        if self._esta_terminado:
            return
        historico = obter_historico()
        if not historico:
            if self.pyperclip:
                self.pyperclip.copy(_("Nenhum histórico disponível."))
                ui.message(_("Nenhum histórico disponível, texto copiado para a área de transferência."))
            else:
                self.mostrar_erro(_("Erro: pyperclip não encontrado."))
            self.botao_testar.SetFocus()
            return
        texto_historico = []
        for entrada in historico:
            detalhes = []
            if configuracao["Exibicao"].get("mostrarData", "True") == "True":
                detalhes.append(_("Data: {}").format(entrada.get('Data', 'N/A')))
            if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
                detalhes.append(_("Download: {} Mbps").format(entrada.get('Download', 'N/A')))
            if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
                detalhes.append(_("Upload: {} Mbps").format(entrada.get('Upload', 'N/A')))
            if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
                detalhes.append(_("Ping: {} ms").format(entrada.get('Ping', 'N/A')))
            if configuracao["Exibicao"].get("mostrarServidor", "True") == "True":
                detalhes.append(_("Servidor: {}").format(entrada.get('Servidor', 'N/A')))
            if configuracao["Exibicao"].get("mostrarServidorID", "True") == "True":
                detalhes.append(_("ID do Servidor: {}").format(entrada.get('ServidorID', 'N/A')))
            if configuracao["Exibicao"].get("mostrarServidorIP", "True") == "True":
                detalhes.append(_("IP do Servidor: {}").format(entrada.get('ServidorIP', 'N/A')))
            if configuracao["Exibicao"].get("mostrarServidorPatrocinador", "True") == "True":
                detalhes.append(_("Patrocinador do Servidor: {}").format(entrada.get('ServidorPatrocinador', 'N/A')))
            if configuracao["Exibicao"].get("mostrarServidorLocalizacao", "True") == "True":
                detalhes.append(_("Localização do Servidor: Lat {} / Lon {}").format(entrada.get('ServidorLat', 'N/A'), entrada.get('ServidorLon', 'N/A')))
            if configuracao["Exibicao"].get("mostrarServidorDistancia", "True") == "True":
                detalhes.append(_("Distância do Servidor: {:.2f} km ({:.0f} metros)").format(float(entrada.get('ServidorDistanciaKm', 0)), float(entrada.get('ServidorDistanciaM', 0))))
            if configuracao["Exibicao"].get("mostrarServidorUrl", "True") == "True":
                detalhes.append(_("URL do Servidor: {}").format(entrada.get('ServidorUrl', 'N/A')))
            if configuracao["Exibicao"].get("mostrarIPCliente", "True") == "True":
                detalhes.append(_("IP do Cliente: {}").format(entrada.get('IP', 'N/A')))
            if configuracao["Exibicao"].get("mostrarISPCliente", "True") == "True":
                detalhes.append(_("ISP do Cliente: {}").format(entrada.get('ISP', 'N/A')))
            if configuracao["Exibicao"].get("mostrarClienteLocalizacao", "True") == "True":
                detalhes.append(_("Localização do Cliente: Lat {} / Lon {}").format(entrada.get('ClientLat', 'N/A'), entrada.get('ClientLon', 'N/A')))
            if configuracao["Exibicao"].get("mostrarBytesEnviados", "True") == "True":
                detalhes.append(_("Bytes Enviados: {} bytes ({:.2f} MB)").format(entrada.get('BytesEnviados', 0), float(entrada.get('BytesEnviados', 0)) / 1_000_000))
            if configuracao["Exibicao"].get("mostrarBytesRecebidos", "True") == "True":
                detalhes.append(_("Bytes Recebidos: {} bytes ({:.2f} MB)").format(entrada.get('BytesRecebidos', 0), float(entrada.get('BytesRecebidos', 0)) / 1_000_000))
            if configuracao["Exibicao"].get("mostrarDuracao", "True") == "True":
                detalhes.append(_("Duração do Teste: {} segundos").format(entrada.get('Duracao', 'N/A')))
            if configuracao["Exibicao"].get("mostrarShareUrl", "True") == "True":
                detalhes.append(_("Link de Compartilhamento: {}").format(entrada.get('ShareUrl', 'N/A')))
            if configuracao["Exibicao"].get("mostrarThreadsDownload", "True") == "True":
                detalhes.append(_("Threads de Download: {}").format(entrada.get('ThreadsDownload', 'N/A')))
            if configuracao["Exibicao"].get("mostrarThreadsUpload", "True") == "True":
                detalhes.append(_("Threads de Upload: {}").format(entrada.get('ThreadsUpload', 'N/A')))
            if configuracao["Exibicao"].get("mostrarTamanhosDownload", "True") == "True":
                detalhes.append(_("Tamanhos de Download: {} bytes").format(entrada.get('TamanhosDownload', 'N/A')))
            if configuracao["Exibicao"].get("mostrarTamanhosUpload", "True") == "True":
                detalhes.append(_("Tamanhos de Upload: {} bytes").format(entrada.get('TamanhosUpload', 'N/A')))
            texto_historico.append("\n".join(detalhes) if detalhes else _("Nenhum dado configurado para exibição."))
        if self.pyperclip:
            texto_final = "\n\n".join(texto_historico)
            self.pyperclip.copy(texto_final)
            ui.message(_("Histórico copiado para a área de transferência."))
        else:
            self.mostrar_erro(_("Erro: pyperclip não encontrado."))
        self.botao_testar.SetFocus()
    def on_atualizar(self, evt):
        if self._esta_terminado:
            return
        self.atualizar_lista_servidores()
        self.botao_testar.SetFocus()
    def on_fechar(self, evt):
        self._esta_terminado = True
        terminar()
        self.Destroy()
    def on_key_press(self, evt):
        if evt.GetKeyCode() == wx.WXK_ESCAPE or (evt.AltDown() and evt.GetKeyCode() == wx.WXK_F4):
            self.Close()
        else:
            evt.Skip()
    def mostrar_erro(self, mensagem):
        if self._esta_terminado:
            return
        if configuracao["Exibicao"].get("mostrarDialogoErros", "True") == "True":
            erro_dialog = ErroDialog(self, mensagem)
            erro_dialog.ShowModal()
            erro_dialog.Destroy()
        else:
            ui.message(mensagem)