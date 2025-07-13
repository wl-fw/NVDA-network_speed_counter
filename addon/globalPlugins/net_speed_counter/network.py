# Copyright (C) 2025 Wallan
# Autor: Wallan 
# Este código é distribuído sob a licença GNU GPL 2.0

from . import speedtest
import threading
import time
import datetime
import requests

historico_memoria = []
_esta_terminado = False

def obter_servidores_disponiveis():
    global _esta_terminado
    if _esta_terminado:
        return []
    try:
        st = speedtest.Speedtest()
        try:
            st.get_servers()
            servidores = st.get_closest_servers()
            lista_servidores = []
            for servidor in servidores[:10]:
                lista_servidores.append({
                    'nome': f"{servidor['sponsor']} ({servidor['name']})",
                    'id': servidor['id']
                })
            return lista_servidores
        finally:
            st.close()
            del st
    except Exception as e:
        raise RuntimeError(_("Erro ao carregar servidores: {}").format(e))  # Tradutores: Mensagem de erro ao carregar servidores

def medir_velocidade(servidor_id=None, callback_progresso=None):
    global _esta_terminado
    if _esta_terminado:
        raise RuntimeError(_("Operação cancelada: addon está sendo finalizado."))  # Tradutores: Mensagem de operação cancelada
    try:
        st = speedtest.Speedtest()
        try:
            if servidor_id:
                st.get_servers([servidor_id])
            else:
                st.get_closest_servers()
                st.get_best_server()
            if callback_progresso:
                callback_progresso(10)
            download = st.download() / 1_000_000
            if callback_progresso:
                callback_progresso(50)
            upload = st.upload() / 1_000_000
            if callback_progresso:
                callback_progresso(75)
            ping = st.results.ping
            server_info = st.results.server
            client_info = st.results.client
            bytes_sent = st.results.bytes_sent
            bytes_received = st.results.bytes_received
            duracao = st.results.test_duration if hasattr(st.results, 'test_duration') else 0
            share_url = st.results.share() or 'N/A'
            if callback_progresso:
                callback_progresso(100)
            resultado = {
                'Data': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Download': f"{download:.2f}",
                'Upload': f"{upload:.2f}",
                'Ping': f"{ping:.2f}",
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
                'ShareUrl': share_url,
                'ThreadsDownload': st.config['threads']['download'],
                'ThreadsUpload': st.config['threads']['upload'],
                'TamanhosDownload': st.config['sizes']['download'],
                'TamanhosUpload': st.config['sizes']['upload']
            }
            if not _esta_terminado:
                historico_memoria.append(resultado)
            return (download, upload, ping, server_info, client_info, bytes_sent, bytes_received, duracao, share_url)
        finally:
            st.close()
            del st
    except Exception as e:
        raise RuntimeError(_("Erro ao medir a velocidade: {}").format(e))  # Tradutores: Mensagem de erro ao medir velocidade

def obter_historico():
    global _esta_terminado
    if _esta_terminado:
        return []
    return historico_memoria

def terminar():
    global _esta_terminado
    _esta_terminado = True
    historico_memoria.clear()