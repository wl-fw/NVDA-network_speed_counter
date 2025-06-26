#Copyright (C) 2025 Wallan
#Este código é distribuído sob a licença GNU GPL 2.0
import config
import addonHandler

addonHandler.initTranslation()

configuracao = {
    "Geral": {
        "servidorSelecionado": "",
    },
    "Exibicao": {
        "mostrarData": "True",
        "mostrarDownload": "True",
        "mostrarUpload": "True",
        "mostrarPing": "True",
        "mostrarServidor": "True",
        "mostrarServidorID": "True",
        "mostrarServidorIP": "True",
        "mostrarServidorPatrocinador": "True",
        "mostrarServidorLocalizacao": "True",
        "mostrarServidorDistancia": "True",
        "mostrarServidorUrl": "True",
        "mostrarIPCliente": "True",
        "mostrarISPCliente": "True",
        "mostrarClienteLocalizacao": "True",
        "mostrarBytesEnviados": "True",
        "mostrarBytesRecebidos": "True",
        "mostrarDuracao": "True",
        "mostrarShareUrl": "True",
        "mostrarThreadsDownload": "True",
        "mostrarThreadsUpload": "True",
        "mostrarTamanhosDownload": "True",
        "mostrarTamanhosUpload": "True"
    }
}

def carregar_configuracao():
    global configuracao
    conf = config.conf.get("netSpeedCounter", {})
    for secao, valores in configuracao.items():
        if secao in conf:
            for chave, valor in valores.items():
                if chave in conf[secao]:
                    configuracao[secao][chave] = conf[secao][chave]

def salvar_configuracao():
    config.conf["netSpeedCounter"] = configuracao