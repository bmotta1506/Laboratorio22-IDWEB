from wsgiref.simple_server import make_server
import json

def app(environ, start_response):
    path = environ["PATH_INFO"]

    if path == "/":
        respuesta = b"Hola, bienvenido a la pagina principal"
        status = "200 OK"
        headers = [("Content-Type", "text/plain")]

    elif path == "/saludo":
        respuesta = json.dumps({"msg": "Hola"}).encode("utf-8")
        status = "200 OK"
        headers = [("Content-Type", "application/json")]

    else:
        respuesta = b"No encontrado"
        status = "404 Not Found"
        headers = [("Content-Type", "text/plain")]

    start_response(status, headers)
    return [respuesta]

server = make_server("localhost", 8000, app)
print("Servidor corriendo en http://localhost:8000/")
server.serve_forever()
