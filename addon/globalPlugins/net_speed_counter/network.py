from . import speedtest
import threading

def medir_velocidade():
    def medir():
        st = speedtest.Speedtest()
        try:
            st.get_best_server()
            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000
            ping = st.results.ping
            return download, upload, ping
        except Exception as e:
            print(f"Erro ao medir velocidade: {e}")
            return None

    resultado = None

    def worker():
        nonlocal resultado
        resultado = medir()

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()

    if resultado is None:
        raise Exception("Falha ao medir a velocidade da internet. Tente novamente.")
    
    return resultado
