# Copyright (C) 2025 Wallan
# Este código é distribuído sob a licença GNU GPL 2.0

import os
import configobj

PASTA_CONFIG_USUARIO = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "nvda")
ARQUIVO_CONFIG = os.path.join(PASTA_CONFIG_USUARIO, "contadorVelocidadeRede.ini")

if not os.path.exists(PASTA_CONFIG_USUARIO):
    os.makedirs(PASTA_CONFIG_USUARIO)
if not os.path.exists(ARQUIVO_CONFIG):
    config = configobj.ConfigObj()
    config["Geral"] = {"servidorSelecionado": ""}
    config["Exibicao"] = {
        "mostrarDownload": "True",
        "mostrarUpload": "True",
        "mostrarPing": "True"
    }
    config.filename = ARQUIVO_CONFIG
    config.write()

configuracao = configobj.ConfigObj(ARQUIVO_CONFIG)