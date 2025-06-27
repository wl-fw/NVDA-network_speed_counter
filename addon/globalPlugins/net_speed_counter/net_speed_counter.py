# Copyright (C) 2025 Wallan
# Autor: Wallan 
# Este código é distribuído sob a licença GNU GPL 2.0

import wx
import gui
from gui import guiHelper
import addonHandler
from .network import obter_servidores_disponiveis, medir_velocidade, obter_historico
from .config import configuracao
from .  import pyperclip
import threading
import ui

addonHandler.initTranslation()

class DetalhesTesteDialog(wx.Dialog):
    def __init__(self, parent, entrada):
        super().__init__(parent, title=_("Detalhes do Teste de Velocidade"))

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        ajudante_sizer = guiHelper.BoxSizerHelper(self, sizer=main_sizer)

        detalhes = []
        if configuracao["Exibicao"].get("mostrarData", "True") == "True":
            detalhes.append(_("Data: {}").format(entrada['Data']))
        if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
            detalhes.append(_("Download: {} Mbps").format(entrada['Download']))
        if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
            detalhes.append(_("Upload: {} Mbps").format(entrada['Upload']))
        if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
            detalhes.append(_("Ping: {} ms").format(entrada['Ping']))
        if configuracao["Exibicao"].get("mostrarServidor", "True") == "True":
            detalhes.append(_("Servidor: {}").format(entrada['Servidor']))
        if configuracao["Exibicao"].get("mostrarServidorID", "True") == "True":
            detalhes.append(_("ID do Servidor: {}").format(entrada['ServidorID']))
        if configuracao["Exibicao"].get("mostrarServidorIP", "True") == "True":
            detalhes.append(_("IP do Servidor: {}").format(entrada['ServidorIP']))
        if configuracao["Exibicao"].get("mostrarServidorPatrocinador", "True") == "True":
            detalhes.append(_("Patrocinador do Servidor: {}").format(entrada['ServidorPatrocinador']))
        if configuracao["Exibicao"].get("mostrarServidorLocalizacao", "True") == "True":
            detalhes.append(_("Localização do Servidor: Lat {} / Lon {}").format(entrada['ServidorLat'], entrada['ServidorLon']))
        if configuracao["Exibicao"].get("mostrarServidorDistancia", "True") == "True":
            detalhes.append(_("Distância do Servidor: {:.2f} km ({:.0f} metros)").format(
                float(entrada['ServidorDistanciaKm']), float(entrada['ServidorDistanciaM'])))
        if configuracao["Exibicao"].get("mostrarServidorUrl", "True") == "True":
            detalhes.append(_("URL do Servidor: {}").format(entrada['ServidorUrl']))
        if configuracao["Exibicao"].get("mostrarIPCliente", "True") == "True":
            detalhes.append(_("IP do Cliente: {}").format(entrada['IP']))
        if configuracao["Exibicao"].get("mostrarISPCliente", "True") == "True":
            detalhes.append(_("ISP do Cliente: {}").format(entrada['ISP']))
        if configuracao["Exibicao"].get("mostrarClienteLocalizacao", "True") == "True":
            detalhes.append(_("Localização do Cliente: Lat {} / Lon {}").format(entrada['ClientLat'], entrada['ClientLon']))
        if configuracao["Exibicao"].get("mostrarBytesEnviados", "True") == "True":
            detalhes.append(_("Bytes Enviados: {} bytes ({:.2f} MB)").format(
                entrada['BytesEnviados'], int(entrada['BytesEnviados']) / 1_000_000))
        if configuracao["Exibicao"].get("mostrarBytesRecebidos", "True") == "True":
            detalhes.append(_("Bytes Recebidos: {} bytes ({:.2f} MB)").format(
                entrada['BytesRecebidos'], int(entrada['BytesRecebidos']) / 1_000_000))
        if configuracao["Exibicao"].get("mostrarDuracao", "True") == "True":
            detalhes.append(_("Duração do Teste: {} segundos").format(entrada['Duracao']))
        if configuracao["Exibicao"].get("mostrarShareUrl", "True") == "True":
            detalhes.append(_("Link de Compartilhamento: {}").format(entrada['ShareUrl']))
        if configuracao["Exibicao"].get("mostrarThreadsDownload", "True") == "True":
            detalhes.append(_("Threads de Download: {}").format(entrada['ThreadsDownload']))
        if configuracao["Exibicao"].get("mostrarThreadsUpload", "True") == "True":
            detalhes.append(_("Threads de Upload: {}").format(entrada['ThreadsUpload']))
        if configuracao["Exibicao"].get("mostrarTamanhosDownload", "True") == "True":
            detalhes.append(_("Tamanhos de Download: {} bytes").format(entrada['TamanhosDownload']))
        if configuracao["Exibicao"].get("mostrarTamanhosUpload", "True") == "True":
            detalhes.append(_("Tamanhos de Upload: {} bytes").format(entrada['TamanhosUpload']))

        self.texto_detalhes = ajudante_sizer.addItem(wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 300)))
        self.texto_detalhes.SetValue("\n".join(detalhes) if detalhes else _("Nenhum dado configurado para exibição."))

        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)
        self.botao_novo_teste = wx.Button(self, label=_("Novo Teste"))
        self.botao_novo_teste.Bind(wx.EVT_BUTTON, self.on_novo_teste)
        sizer_botoes.Add(self.botao_novo_teste, 0, wx.ALL, 5)

        self.botao_copiar = wx.Button(self, label=_("Copiar Informações"))
        self.botao_copiar.Bind(wx.EVT_BUTTON, lambda evt: self.on_copiar(entrada))
        sizer_botoes.Add(self.botao_copiar, 0, wx.ALL, 5)

        self.botao_fechar = wx.Button(self, label=_("Fechar"))
        self.botao_fechar.Bind(wx.EVT_BUTTON, self.on_fechar)
        sizer_botoes.Add(self.botao_fechar, 0, wx.ALL, 5)

        ajudante_sizer.addItem(sizer_botoes, flag=wx.ALIGN_RIGHT)

        self.SetSizer(main_sizer)
        self.Fit()
        self.botao_novo_teste.SetFocus()

        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

    def on_novo_teste(self, evt):
        self.Close()
        wx.CallAfter(self.GetParent().on_testar, None)

    def on_copiar(self, entrada):
        detalhes = []
        if configuracao["Exibicao"].get("mostrarData", "True") == "True":
            detalhes.append(_("Data: {}").format(entrada['Data']))
        if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
            detalhes.append(_("Download: {} Mbps").format(entrada['Download']))
        if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
            detalhes.append(_("Upload: {} Mbps").format(entrada['Upload']))
        if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
            detalhes.append(_("Ping: {} ms").format(entrada['Ping']))
        if configuracao["Exibicao"].get("mostrarServidor", "True") == "True":
            detalhes.append(_("Servidor: {}").format(entrada['Servidor']))
        if configuracao["Exibicao"].get("mostrarServidorID", "True") == "True":
            detalhes.append(_("ID do Servidor: {}").format(entrada['ServidorID']))
        if configuracao["Exibicao"].get("mostrarServidorIP", "True") == "True":
            detalhes.append(_("IP do Servidor: {}").format(entrada['ServidorIP']))
        if configuracao["Exibicao"].get("mostrarServidorPatrocinador", "True") == "True":
            detalhes.append(_("Patrocinador do Servidor: {}").format(entrada['ServidorPatrocinador']))
        if configuracao["Exibicao"].get("mostrarServidorLocalizacao", "True") == "True":
            detalhes.append(_("Localização do Servidor: Lat {} / Lon {}").format(entrada['ServidorLat'], entrada['ServidorLon']))
        if configuracao["Exibicao"].get("mostrarServidorDistancia", "True") == "True":
            detalhes.append(_("Distância do Servidor: {:.2f} km ({:.0f} metros)").format(
                float(entrada['ServidorDistanciaKm']), float(entrada['ServidorDistanciaM'])))
        if configuracao["Exibicao"].get("mostrarServidorUrl", "True") == "True":
            detalhes.append(_("URL do Servidor: {}").format(entrada['ServidorUrl']))
        if configuracao["Exibicao"].get("mostrarIPCliente", "True") == "True":
            detalhes.append(_("IP do Cliente: {}").format(entrada['IP']))
        if configuracao["Exibicao"].get("mostrarISPCliente", "True") == "True":
            detalhes.append(_("ISP do Cliente: {}").format(entrada['ISP']))
        if configuracao["Exibicao"].get("mostrarClienteLocalizacao", "True") == "True":
            detalhes.append(_("Localização do Cliente: Lat {} / Lon {}").format(entrada['ClientLat'], entrada['ClientLon']))
        if configuracao["Exibicao"].get("mostrarBytesEnviados", "True") == "True":
            detalhes.append(_("Bytes Enviados: {} bytes ({:.2f} MB)").format(
                entrada['BytesEnviados'], int(entrada['BytesEnviados']) / 1_000_000))
        if configuracao["Exibicao"].get("mostrarBytesRecebidos", "True") == "True":
            detalhes.append(_("Bytes Recebidos: {} bytes ({:.2f} MB)").format(
                entrada['BytesRecebidos'], int(entrada['BytesRecebidos']) / 1_000_000))
        if configuracao["Exibicao"].get("mostrarDuracao", "True") == "True":
            detalhes.append(_("Duração do Teste: {} segundos").format(entrada['Duracao']))
        if configuracao["Exibicao"].get("mostrarShareUrl", "True") == "True":
            detalhes.append(_("Link de Compartilhamento: {}").format(entrada['ShareUrl']))
        if configuracao["Exibicao"].get("mostrarThreadsDownload", "True") == "True":
            detalhes.append(_("Threads de Download: {}").format(entrada['ThreadsDownload']))
        if configuracao["Exibicao"].get("mostrarThreadsUpload", "True") == "True":
            detalhes.append(_("Threads de Upload: {}").format(entrada['ThreadsUpload']))
        if configuracao["Exibicao"].get("mostrarTamanhosDownload", "True") == "True":
            detalhes.append(_("Tamanhos de Download: {} bytes").format(entrada['TamanhosDownload']))
        if configuracao["Exibicao"].get("mostrarTamanhosUpload", "True") == "True":
            detalhes.append(_("Tamanhos de Upload: {} bytes").format(entrada['TamanhosUpload']))
        
        texto = "\n".join(detalhes) if detalhes else _("Nenhum dado configurado para exibição.")
        pyperclip.copy(texto)
        ui.message(_("Informações copiadas para a área de transferência."))

    def on_fechar(self, evt):
        self.Close()

    def on_key_press(self, evt):
        if evt.GetKeyCode() == wx.WXK_ESCAPE or (evt.AltDown() and evt.GetKeyCode() == wx.WXK_F4):
            self.Close()
        else:
            evt.Skip()

class NetSpeedCounterDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title=_("Contador de Velocidade da Rede"))

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        ajudante_sizer = guiHelper.BoxSizerHelper(self, sizer=main_sizer)

        self.botao_testar = ajudante_sizer.addItem(wx.Button(self, label=_("Testar Velocidade")))
        self.botao_testar.Bind(wx.EVT_BUTTON, self.on_testar)
        self.botao_testar.SetDefault()

        self.progresso = ajudante_sizer.addItem(wx.Gauge(self, range=100, size=(-1, 20)))
        self.progresso.SetValue(0)

        sizer_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        
        self.rotulo_servidor = wx.StaticText(self, label=_("Selecionar servidor:"))
        self.escolha_servidor = wx.Choice(self, choices=[])
        sizer_horizontal.Add(self.rotulo_servidor, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_horizontal.Add(self.escolha_servidor, 1, wx.ALL | wx.EXPAND, 5)

        self.botao_atualizar = wx.Button(self, label=_("Atualizar Servidores"))
        self.botao_atualizar.Bind(wx.EVT_BUTTON, self.on_atualizar)
        sizer_horizontal.Add(self.botao_atualizar, 0, wx.ALL, 5)

        ajudante_sizer.addItem(sizer_horizontal, proportion=1, flag=wx.EXPAND)

        self.rotulo_historico = ajudante_sizer.addItem(wx.StaticText(self, label=_("Histórico de Testes:")))
        self.lista_historico = ajudante_sizer.addItem(wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL))

        self.botao_copiar = wx.Button(self, label=_("Copiar Informações"))
        self.botao_copiar.Bind(wx.EVT_BUTTON, self.on_copiar)
        
        self.botao_copiar_historico = wx.Button(self, label=_("Copiar Histórico"))
        self.botao_copiar_historico.Bind(wx.EVT_BUTTON, self.on_copiar_historico)
        
        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)
        sizer_botoes.Add(self.botao_copiar, 0, wx.ALL, 5)
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

        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

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
            self.botao_copiar.Disable()
            self.botao_copiar_historico.Disable()
        else:
            self.rotulo_historico.Show()
            self.lista_historico.Show()
            self.botao_copiar.Enable()
            self.botao_copiar_historico.Enable()
            for i, (titulo, largura) in enumerate(colunas):
                self.lista_historico.InsertColumn(i, titulo, width=largura)

    def atualizar_lista_servidores(self):
        try:
            servidores = obter_servidores_disponiveis()
            self.escolha_servidor.Clear()
            self.escolha_servidor.Append(_("(Automático)"), "")
            for servidor in servidores[:10]:
                self.escolha_servidor.Append(f"{servidor['nome']} - {servidor['pais']} ({servidor['distancia']:.2f} km)", servidor['id'])
            servidor_salvo = configuracao["Geral"].get("servidorSelecionado", "")
            indice = self.escolha_servidor.FindString(servidor_salvo) if servidor_salvo else 0
            self.escolha_servidor.SetSelection(indice if indice != wx.NOT_FOUND else 0)
        except Exception as e:
            ui.message(_("Erro ao carregar a lista de servidores: {}").format(e))

    def atualizar_historico(self):
        self.atualizar_colunas_historico()
        historico = obter_historico()
        self.lista_historico.DeleteAllItems()
        if not historico:
            return
        for i, entrada in enumerate(historico):
            col_index = 0
            if configuracao["Exibicao"].get("mostrarData", "True") == "True":
                self.lista_historico.InsertItem(i, entrada['Data'])
                col_index += 1
            else:
                self.lista_historico.InsertItem(i, "")
            if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
                self.lista_historico.SetItem(i, col_index, entrada['Download'])
                col_index += 1
            if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
                self.lista_historico.SetItem(i, col_index, entrada['Upload'])
                col_index += 1
            if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
                self.lista_historico.SetItem(i, col_index, entrada['Ping'])

    def on_lista_foco(self, evt):
        if self.lista_historico.GetItemCount() == 0:
            self.botao_testar.SetFocus()
        else:
            evt.Skip()

    def on_testar(self, evt):
        servidor_id = self.escolha_servidor.GetClientData(self.escolha_servidor.GetSelection())
        self.botao_testar.Disable()
        self.botao_copiar.Disable()
        self.botao_copiar_historico.Disable()
        self.progresso.SetValue(0)
        ui.message(_("Testando a velocidade da internet, por favor aguarde..."))
        
        def testar():
            try:
                def callback_progresso(valor):
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
                
                wx.CallAfter(self.atualizar_historico)
                wx.CallAfter(ui.message, mensagem_final)
                wx.CallAfter(self.botao_testar.Enable)
                wx.CallAfter(self.botao_copiar.Enable)
                wx.CallAfter(self.botao_copiar_historico.Enable)
                wx.CallAfter(self.progresso.SetValue, 0)
                wx.CallAfter(self.botao_testar.SetFocus)
            except Exception as e:
                wx.CallAfter(ui.message, _("Erro ao testar a velocidade: {}").format(e))
                wx.CallAfter(self.botao_testar.Enable)
                wx.CallAfter(self.botao_copiar.Enable)
                wx.CallAfter(self.botao_copiar_historico.Enable)
                wx.CallAfter(self.progresso.SetValue, 0)
                wx.CallAfter(self.botao_testar.SetFocus)

        thread = threading.Thread(target=testar)
        thread.daemon = True
        thread.start()

    def on_selecionar_historico(self, evt):
        indice = self.lista_historico.GetFirstSelected()
        if indice >= 0:
            historico = obter_historico()
            entrada = historico[indice]
            detalhes_dialog = DetalhesTesteDialog(self, entrada)
            detalhes_dialog.ShowModal()
            detalhes_dialog.Destroy()
            self.botao_testar.SetFocus()

    def on_copiar(self, evt):
        indice = self.lista_historico.GetFirstSelected()
        if indice >= 0:
            historico = obter_historico()
            entrada = historico[indice]
            detalhes = []
            if configuracao["Exibicao"].get("mostrarData", "True") == "True":
                detalhes.append(_("Data: {}").format(entrada['Data']))
            if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
                detalhes.append(_("Download: {} Mbps").format(entrada['Download']))
            if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
                detalhes.append(_("Upload: {} Mbps").format(entrada['Upload']))
            if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
                detalhes.append(_("Ping: {} ms").format(entrada['Ping']))
            if configuracao["Exibicao"].get("mostrarServidor", "True") == "True":
                detalhes.append(_("Servidor: {}").format(entrada['Servidor']))
            if configuracao["Exibicao"].get("mostrarServidorID", "True") == "True":
                detalhes.append(_("ID do Servidor: {}").format(entrada['ServidorID']))
            if configuracao["Exibicao"].get("mostrarServidorIP", "True") == "True":
                detalhes.append(_("IP do Servidor: {}").format(entrada['ServidorIP']))
            if configuracao["Exibicao"].get("mostrarServidorPatrocinador", "True") == "True":
                detalhes.append(_("Patrocinador do Servidor: {}").format(entrada['ServidorPatrocinador']))
            if configuracao["Exibicao"].get("mostrarServidorLocalizacao", "True") == "True":
                detalhes.append(_("Localização do Servidor: Lat {} / Lon {}").format(entrada['ServidorLat'], entrada['ServidorLon']))
            if configuracao["Exibicao"].get("mostrarServidorDistancia", "True") == "True":
                detalhes.append(_("Distância do Servidor: {:.2f} km ({:.0f} metros)").format(
                    float(entrada['ServidorDistanciaKm']), float(entrada['ServidorDistanciaM'])))
            if configuracao["Exibicao"].get("mostrarServidorUrl", "True") == "True":
                detalhes.append(_("URL do Servidor: {}").format(entrada['ServidorUrl']))
            if configuracao["Exibicao"].get("mostrarIPCliente", "True") == "True":
                detalhes.append(_("IP do Cliente: {}").format(entrada['IP']))
            if configuracao["Exibicao"].get("mostrarISPCliente", "True") == "True":
                detalhes.append(_("ISP do Cliente: {}").format(entrada['ISP']))
            if configuracao["Exibicao"].get("mostrarClienteLocalizacao", "True") == "True":
                detalhes.append(_("Localização do Cliente: Lat {} / Lon {}").format(entrada['ClientLat'], entrada['ClientLon']))
            if configuracao["Exibicao"].get("mostrarBytesEnviados", "True") == "True":
                detalhes.append(_("Bytes Enviados: {} bytes ({:.2f} MB)").format(
                    entrada['BytesEnviados'], int(entrada['BytesEnviados']) / 1_000_000))
            if configuracao["Exibicao"].get("mostrarBytesRecebidos", "True") == "True":
                detalhes.append(_("Bytes Recebidos: {} bytes ({:.2f} MB)").format(
                    entrada['BytesRecebidos'], int(entrada['BytesRecebidos']) / 1_000_000))
            if configuracao["Exibicao"].get("mostrarDuracao", "True") == "True":
                detalhes.append(_("Duração do Teste: {} segundos").format(entrada['Duracao']))
            if configuracao["Exibicao"].get("mostrarShareUrl", "True") == "True":
                detalhes.append(_("Link de Compartilhamento: {}").format(entrada['ShareUrl']))
            if configuracao["Exibicao"].get("mostrarThreadsDownload", "True") == "True":
                detalhes.append(_("Threads de Download: {}").format(entrada['ThreadsDownload']))
            if configuracao["Exibicao"].get("mostrarThreadsUpload", "True") == "True":
                detalhes.append(_("Threads de Upload: {}").format(entrada['ThreadsUpload']))
            if configuracao["Exibicao"].get("mostrarTamanhosDownload", "True") == "True":
                detalhes.append(_("Tamanhos de Download: {} bytes").format(entrada['TamanhosDownload']))
            if configuracao["Exibicao"].get("mostrarTamanhosUpload", "True") == "True":
                detalhes.append(_("Tamanhos de Upload: {} bytes").format(entrada['TamanhosUpload']))
            
            texto = "\n".join(detalhes) if detalhes else _("Nenhum dado configurado para exibição.")
            pyperclip.copy(texto)
            ui.message(_("Informações copiadas para a área de transferência."))
        else:
            ui.message(_("Nenhum teste selecionado para copiar."))
        self.botao_testar.SetFocus()

    def on_copiar_historico(self, evt):
        historico = obter_historico()
        if not historico:
            ui.message(_("Nenhum histórico disponível para copiar."))
            self.botao_testar.SetFocus()
            return
        
        texto_historico = []
        for entrada in historico:
            detalhes = []
            if configuracao["Exibicao"].get("mostrarData", "True") == "True":
                detalhes.append(_("Data: {}").format(entrada['Data']))
            if configuracao["Exibicao"].get("mostrarDownload", "True") == "True":
                detalhes.append(_("Download: {} Mbps").format(entrada['Download']))
            if configuracao["Exibicao"].get("mostrarUpload", "True") == "True":
                detalhes.append(_("Upload: {} Mbps").format(entrada['Upload']))
            if configuracao["Exibicao"].get("mostrarPing", "True") == "True":
                detalhes.append(_("Ping: {} ms").format(entrada['Ping']))
            if configuracao["Exibicao"].get("mostrarServidor", "True") == "True":
                detalhes.append(_("Servidor: {}").format(entrada['Servidor']))
            if configuracao["Exibicao"].get("mostrarServidorID", "True") == "True":
                detalhes.append(_("ID do Servidor: {}").format(entrada['ServidorID']))
            if configuracao["Exibicao"].get("mostrarServidorIP", "True") == "True":
                detalhes.append(_("IP do Servidor: {}").format(entrada['ServidorIP']))
            if configuracao["Exibicao"].get("mostrarServidorPatrocinador", "True") == "True":
                detalhes.append(_("Patrocinador do Servidor: {}").format(entrada['ServidorPatrocinador']))
            if configuracao["Exibicao"].get("mostrarServidorLocalizacao", "True") == "True":
                detalhes.append(_("Localização do Servidor: Lat {} / Lon {}").format(entrada['ServidorLat'], entrada['ServidorLon']))
            if configuracao["Exibicao"].get("mostrarServidorDistancia", "True") == "True":
                detalhes.append(_("Distância do Servidor: {:.2f} km ({:.0f} metros)").format(
                    float(entrada['ServidorDistanciaKm']), float(entrada['ServidorDistanciaM'])))
            if configuracao["Exibicao"].get("mostrarServidorUrl", "True") == "True":
                detalhes.append(_("URL do Servidor: {}").format(entrada['ServidorUrl']))
            if configuracao["Exibicao"].get("mostrarIPCliente", "True") == "True":
                detalhes.append(_("IP do Cliente: {}").format(entrada['IP']))
            if configuracao["Exibicao"].get("mostrarISPCliente", "True") == "True":
                detalhes.append(_("ISP do Cliente: {}").format(entrada['ISP']))
            if configuracao["Exibicao"].get("mostrarClienteLocalizacao", "True") == "True":
                detalhes.append(_("Localização do Cliente: Lat {} / Lon {}").format(entrada['ClientLat'], entrada['ClientLon']))
            if configuracao["Exibicao"].get("mostrarBytesEnviados", "True") == "True":
                detalhes.append(_("Bytes Enviados: {} bytes ({:.2f} MB)").format(
                    entrada['BytesEnviados'], int(entrada['BytesEnviados']) / 1_000_000))
            if configuracao["Exibicao"].get("mostrarBytesRecebidos", "True") == "True":
                detalhes.append(_("Bytes Recebidos: {} bytes ({:.2f} MB)").format(
                    entrada['BytesRecebidos'], int(entrada['BytesRecebidos']) / 1_000_000))
            if configuracao["Exibicao"].get("mostrarDuracao", "True") == "True":
                detalhes.append(_("Duração do Teste: {} segundos").format(entrada['Duracao']))
            if configuracao["Exibicao"].get("mostrarShareUrl", "True") == "True":
                detalhes.append(_("Link de Compartilhamento: {}").format(entrada['ShareUrl']))
            if configuracao["Exibicao"].get("mostrarThreadsDownload", "True") == "True":
                detalhes.append(_("Threads de Download: {}").format(entrada['ThreadsDownload']))
            if configuracao["Exibicao"].get("mostrarThreadsUpload", "True") == "True":
                detalhes.append(_("Threads de Upload: {}").format(entrada['ThreadsUpload']))
            if configuracao["Exibicao"].get("mostrarTamanhosDownload", "True") == "True":
                detalhes.append(_("Tamanhos de Download: {} bytes").format(entrada['TamanhosDownload']))
            if configuracao["Exibicao"].get("mostrarTamanhosUpload", "True") == "True":
                detalhes.append(_("Tamanhos de Upload: {} bytes").format(entrada['TamanhosUpload']))
            texto_historico.append("\n".join(detalhes) if detalhes else _("Nenhum dado configurado para exibição."))
        
        texto_final = "\n\n".join(texto_historico)
        pyperclip.copy(texto_final)
        ui.message(_("Histórico copiado para a área de transferência."))
        self.botao_testar.SetFocus()

    def on_atualizar(self, evt):
        self.atualizar_lista_servidores()
        self.botao_testar.SetFocus()

    def on_fechar(self, evt):
        self.Close()

    def on_key_press(self, evt):
        if evt.GetKeyCode() == wx.WXK_ESCAPE or (evt.AltDown() and evt.GetKeyCode() == wx.WXK_F4):
            self.Close()
        else:
            evt.Skip()