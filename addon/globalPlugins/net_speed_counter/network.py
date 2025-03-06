# Copyright (C) 2025 Wallan
# Este código é distribuído sob a licença GNU GPL 2.0

from . import speedtest
import threading
import time
from .config import configuracao

def obter_servidores_disponiveis():
    st = speedtest.Speedtest()
    try:
        servidores = st.get_closest_servers(5)
        lista_servidores = []
        for servidor in servidores:
            lista_servidores.append({
                'id': str(servidor['id']),
                'nome': servidor['name'],
                'pais': servidor['country'],
                'distancia': float(servidor['d'])
            })
        return lista_servidores
    except Exception:
        servidores = st.get_servers()
        lista_servidores = []
        contador = 0
        for grupo_servidores in servidores.values():
            for servidor in grupo_servidores:
                if contador >= 5:
                    break
                lista_servidores.append({
                    'id': str(servidor['id']),
                    'nome': servidor['name'],
                    'pais': servidor['country'],
                    'distancia': float(servidor.get('d', 0))
                })
                contador += 1
            if contador >= 5:
                break
        return lista_servidores

def medir_velocidade():
    def medir():
        st = speedtest.Speedtest()
        try:
            servidor_selecionado = configuracao["Geral"]["servidorSelecionado"]
            if servidor_selecionado:
                st.get_servers([servidor_selecionado])
            else:
                st.get_best_server()
            
            downloads = []
            uploads = []
            pings = []
            for _ in range(2):
                download = st.download() / 1_000_000
                upload = st.upload() / 1_000_000
                ping = st.results.ping
                downloads.append(download)
                uploads.append(upload)
                pings.append(ping)
                time.sleep(1)
            
            download_final = sum(downloads) / len(downloads)
            upload_final = sum(uploads) / len(uploads)
            ping_final = sum(pings) / len(pings)
            return download_final, upload_final, ping_final
        except Exception as e:
            raise RuntimeError(_("Erro ao medir a velocidade: {}").format(e))

    resultado = None

    def trabalhador():
        nonlocal resultado
        resultado = medir()

    thread = threading.Thread(target=trabalhador)
    thread.start()
    thread.join()

    if resultado is None:
        raise RuntimeError(_("Falha ao medir a velocidade da internet. Por favor, tente novamente."))
    
    return resultado