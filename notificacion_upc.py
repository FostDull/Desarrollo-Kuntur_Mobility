import requests

def notificacion_a_upc():
    payload = {

    }
    if url_evidencia:
        payload["url"] = url_evidencia

    
    try:
        respuesta = requests.post(
            "http://localhost:8000/api/denuncias",
            jsson=payload,
            timeovt=10
        )

        print("====================")
        print(payload)
        print("====================")
        print(f"Notificación enviada a UPC. Codigo: {respuesta.status_code}")
        return respuesta.status_code == 200

    except Exception as e:
        print(f"Error notificación a UPC: {e}")
        return False