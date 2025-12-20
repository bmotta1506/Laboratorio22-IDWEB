from wsgiref.simple_server import make_server
import json, os
from urllib.parse import unquote

STATIC_DIR = "static"

equipos = []

def servir_estatico(path):
  file_path = path.lstrip("/")
  full_path = os.path.join(STATIC_DIR, file_path.replace("static/", ""))

    
  if not os.path.isfile(full_path):
    return None, None
  
  if full_path.endswith(".html"):
    content_type = "text/html; charset=utf-8"
  elif full_path.endswith(".css"):
    content_type = "text/css"
  elif full_path.endswith(".js"):
    content_type = "application/javascript"
  elif full_path.endswith(".png"):
    content_type = "image/png"
  elif full_path.endswith(".jpg") or full_path.endswith(".jpeg"):
    content_type = "image/jpeg"
  else:
    content_type = "application/octet-stream"

  with open(full_path, "rb") as f:
    return f.read(), content_type  
  
def app(environ, start_response):
  metodo = environ["REQUEST_METHOD"]
  path = unquote(environ["PATH_INFO"])

  if path.startswith("/static/"):
    contenido, tipo = servir_estatico(path)

    if contenido is None:
      start_response("404 Not Found", [("Content-Type", "text/plain")])
      return [b"Archivo no encontrado"]
    
    start_response("200 OK", [("Content-Type", tipo)])
    return [contenido]
  
  elif metodo == "GET" and path == "/":
    contenido, tipo = servir_estatico("/static/index.html")
    start_response("200 OK", [("Content-Type", tipo)])
    return [contenido]
  
  elif metodo == "GET" and path == "/equipos":
    respuesta = json.dumps(equipos).encode()
    headers = [("Content-Type", "application/json")]
    status = "200 OK"

  elif metodo == "POST" and path == "/equipos":
    length = int(environ.get("CONTENT_LENGTH", 0))
    body = environ["wsgi.input"].read(length).decode()

    pares = [x.split("=") for x in body.split("&")]
    data = {"id": len(equipos) + 1}
    for k, v in pares:
      try:
        valor = int(v)
      except ValueError:
        valor = v.replace("+", " ")
      data[k] = valor
      
    equipos.append(data)

    respuesta = f"Equipo {data["nombre"]} agregado.".encode()
    headers = [("Content-Type", "text/plain")]
    status = "201 Created"

  elif metodo == "GET" and path.startswith("/equipos/"):
    equipo_id = int(path.split("/")[-1])
    equipo = None
    for equipoPrueba in equipos:
      if equipoPrueba["id"] == equipo_id:
        equipo = equipoPrueba
        break

    if equipo:
      respuesta = json.dumps(equipo).encode()
      headers = [("Content-Type", "application/json")]
      status = "200 OK"
    else:
      respuesta = b"Error: Equipo no encontrado"
      headers = [("Content-Type", "text/plain")]
      status = "404 Not Found"

  else:
    respuesta = b"Ruta no encontrada"
    headers = [("Content-Type", "text/plain")]
    status = "404 Not Found"

  start_response(status, headers)
  return [respuesta]

server = make_server("localhost", 8000, app)
print("Servidor corriendo en http://localhost:8000/")
server.serve_forever()