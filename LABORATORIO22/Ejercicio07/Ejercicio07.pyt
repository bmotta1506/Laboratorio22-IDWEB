from wsgiref.simple_server import make_server

def app(environ, start_response):
    path = environ["PATH_INFO"]

    if path == "/":
        respuesta = b"Inicio"
        headers = [("Content-Type", "text/plain")]
        status = "200 OK"
    elif path == "/saludo":
        respuesta = b"Hola mundo desde WSGI"
        headers = [("Content-Type", "text/plain")]
        status = "200 OK"
    else:
        respuesta = b"404"
        headers = [("Content-Type", "text/plain")]
        status = "404 Not Found"

    start_response(status, headers)
    return [respuesta]

server = make_server("localhost", 8000, app)
print("Servidor corriendo en http://localhost:8000/")
server.serve_forever()