from flask import Flask, abort

app = Flask(__name__)


@app.route("/<subdomain>/<port>")
def register(subdomain, port):
    port = int(str(port))
    if port < 1000 or port > 60000:
        abort(403)
    return "{}, {}!".format(port, subdomain)


app.run(host='0.0.0.0', port=81)
