from wsgiref.simple_server import make_server
import json

libros = []

def app(environ, start_response):
  path = environ["PATH_INFO"]
  metodo = environ["REQUEST_METHOD"]

  if path == "/libros" and metodo == "GET":
    respuesta = json.dumps(libros).encode()
    headers = [("Content-Type", "application/json")]
    status = "200 OK"
    
  elif path == "/libros" and metodo == "POST":
    length = int(environ.get("CONTENT_LENGTH", 0))
    body = environ["wsgi.input"].read(length)
    data = json.loads(body)

    data["id"] = len(libros) + 1
    libros.append(data)

    respuesta = f"Libro agregado con id {data['id']}".encode()
    headers = [("Content-Type", "text/plain")]
    status = "201 Created"

  elif path.startswith("/libros/") and metodo == "GET":
    libro_id = int(path.split("/")[-1])
    libro = None
    for libroPrueba in libros:
      if libroPrueba["id"] == libro_id:
        libro = libroPrueba
        break

    print(libro)

    if libro:
      respuesta = json.dumps(libro).encode()
      headers = [("Content-Type", "application/json")]
      status = "200 OK"
    else:
      respuesta = b"Error: Libro no encontrado"
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