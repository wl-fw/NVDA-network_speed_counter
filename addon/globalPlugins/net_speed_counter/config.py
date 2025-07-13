# Copyright (C) 2025 Wallan
# Autor: Wallan 
# Este código é distribuído sob a licença GNU GPL 2.0

import os
import configparser
import addonHandler
import logging

addonHandler.initTranslation()

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "net_speed_counter.ini")

configuracao = {
    "Geral": {
        "servidorSelecionado": ""
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
        "mostrarTamanhosUpload": "True",
        "mostrarDialogoErros": "True"
    }
}

def carregar_configuracao():
    global configuracao
    try:
        config_parser = configparser.ConfigParser()
        if os.path.exists(CONFIG_PATH):
            config_parser.read(CONFIG_PATH, encoding='utf-8')
            for secao, valores in configuracao.items():
                if secao in config_parser:
                    for chave, valor_padrao in valores.items():
                        configuracao[secao][chave] = config_parser[secao].get(chave, valor_padrao)
        else:
            salvar_configuracao()
    except Exception as e:
        logging.error(f"Erro ao carregar configurações: {e}")
        salvar_configuracao()

def salvar_configuracao():
    try:
        config_parser = configparser.ConfigParser()
        for secao, valores in configuracao.items():
            config_parser[secao] = {chave: str(valor) for chave, valor in valores.items()}
        with open(CONFIG_PATH, 'w', encoding='utf-8') as config_file:
            config_parser.write(config_file)
    except Exception as e:
        logging.error(f"Erro ao salvar configurações: {e}")