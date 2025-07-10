# Copyright (C) 2025 Wallan
# Autor: Wallan 
# Este código é distribuído sob a licença GNU GPL 2.0

from . import speedtest
import threading
import time
import datetime
import requests

historico_memoria = []

def obter_servidores_disponiveis():
    st = speedtest.Speedtest()
    tentativas = 3
    for tentativa in range(tentativas):
        try:
            st.get_config()  # Força a atualização da configuração
            servidores = st.get_closest_servers(10)
            lista_servidores = []
            nome_contagem = {}
            for servidor in servidores[:10]:
                nome = f"{servidor['name']} ({servidor['d']:.2f} km)"
                if nome in nome_contagem:
                    nome_contagem[nome] += 1
                    nome_exibicao = f"{servidor['name']} ({servidor['sponsor']})"
                else:
                    nome_contagem[nome] = 1
                    nome_exibicao = nome
                lista_servidores.append({
                    'id': str(servidor['id']),
                    'nome': nome_exibicao,
                    'pais': servidor['country'],
                    'distancia': float(servidor['d'])
                })
            return lista_servidores
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                if tentativa < tentativas - 1:
                    time.sleep(2 ** tentativa)
                    continue
                else:
                    raise RuntimeError(_("Erro ao carregar servidores: acesso negado (HTTP 403). Verifique sua conexão ou tente novamente mais tarde."))
            else:
                raise RuntimeError(_("Erro ao carregar servidores: {}").format(e))
        except Exception as e:
            servidores = st.get_servers()
            lista_servidores = []
            contador = 0
            nome_contagem = {}
            for grupo_servidores in servidores.values():
                for servidor in grupo_servidores:
                    if contador >= 10:
                        break
                    nome = f"{servidor['name']} ({servidor.get('d', 0):.2f} km)"
                    if nome in nome_contagem:
                        nome_contagem[nome] += 1
                        nome_exibicao = f"{servidor['name']} ({servidor['sponsor']})"
                    else:
                        nome_contagem[nome] = 1
                        nome_exibicao = nome
                    lista_servidores.append({
                        'id': str(servidor['id']),
                        'nome': nome_exibicao,
                        'pais': servidor['country'],
                        'distancia': float(servidor.get('d', 0))
                    })
                    contador += 1
                if contador >= 10:
                    break
            return lista_servidores
    raise RuntimeError(_("Falha ao carregar servidores após várias tentativas."))

def medir_velocidade(servidor_id=None, callback_progresso=None):
    def medir():
        st = speedtest.Speedtest()
        try:
            inicio = time.time()
            if callback_progresso is not None:
                callback_progresso(10)
            
            if servidor_id:
                st.get_servers([servidor_id])
            else:
                st.get_best_server()
            
            if callback_progresso is not None:
                callback_progresso(33)
            
            downloads = []
            uploads = []
            pings = []
            for _ in range(2):
                download = st.download(
                    callback=lambda i, total, **kwargs: callback_progresso(33 + (i + 1) * 17 / total) if callback_progresso is not None else None
                ) / 1_000_000
                downloads.append(download)
                upload = st.upload(
                    callback=lambda i, total, **kwargs: callback_progresso(50 + (i + 1) * 17 / total) if callback_progresso is not None else None
                ) / 1_000_000
                uploads.append(upload)
                ping = st.results.ping
                pings.append(ping)
            
            download_final = sum(downloads) / len(downloads)
            upload_final = sum(uploads) / len(uploads)
            ping_final = sum(pings) / len(pings)
            
            fim = time.time()
            duracao = fim - inicio
            
            if callback_progresso is not None:
                callback_progresso(100)
            
            server_info = st.results.server
            client_info = st.config['client']
            bytes_sent = st.results.bytes_sent
            bytes_received = st.results.bytes_received
            share_url = st.results.share() if st.results.download and st.results.upload else None
            
            resultado = {
                'Data': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Download': f"{download_final:.2f}",
                'Upload': f"{upload_final:.2f}",
                'Ping': f"{ping_final:.2f}",
                'Servidor': f"{server_info['name']} ({server_info['country']})",
                'ServidorID': server_info['id'],
                'ServidorIP': server_info.get('host', 'N/A').split(':')[0],
                'ServidorLat': server_info.get('lat', 'N/A'),
                'ServidorLon': server_info.get('lon', 'N/A'),
                'ServidorDistanciaKm': server_info.get('d', 0),
                'ServidorDistanciaM': server_info.get('d', 0) * 1000,
                'ServidorUrl': server_info.get('url', 'N/A'),
                'ServidorPatrocinador': server_info.get('sponsor', 'N/A'),
                'IP': client_info.get('ip', 'N/A'),
                'ISP': client_info.get('isp', 'N/A'),
                'ClientLat': client_info.get('lat', 'N/A'),
                'ClientLon': client_info.get('lon', 'N/A'),
                'BytesEnviados': bytes_sent,
                'BytesRecebidos': bytes_received,
                'Duracao': f"{duracao:.2f}",
                'ShareUrl': share_url or 'N/A',
                'ThreadsDownload': st.config['threads']['download'],
                'ThreadsUpload': st.config['threads']['upload'],
                'TamanhosDownload': st.config['sizes']['download'],
                'TamanhosUpload': st.config['sizes']['upload']
            }
            
            historico_memoria.append(resultado)
            return (download_final, upload_final, ping_final, server_info, client_info,
                    bytes_sent, bytes_received, duracao, share_url)
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

def obter_historico():
    return historico_memoria