from wsgiref.simple_server import make_server
import json

def app(environ, start_response):
  if environ["REQUEST_METHOD"] == "POST":
    length = int(environ.get("CONTENT_LENGTH", 0))
    body = environ["wsgi.input"].read(length)
    data = json.loads(body)

    respuesta = {"suma": data["a"] + data["b"]}

    start_response("200 OK", [("Content-Type", "application/json")])
    return [json.dumps(respuesta).encode()]

  start_response("200 OK", [("Content-Type", "text/plain")])
  return [b"Envia un POST"]
  
server = make_server("localhost", 8000, app)
print("Servidor corriendo en http://localhost:8000/")
server.serve_forever()