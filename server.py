from flask import Flask, abort, request
import os

app = Flask(__name__)

controller_subdomain = 'ngcontrol'
port_to_host = {81: controller_subdomain}
nginx_path = '/etc/nginx/conf.d'
domain = 'arthurlpgc.com'


def set_from_maps():
    os.system('sudo rm -f {}/*'.format(nginx_path))
    for port in port_to_host.keys():
        subdomain = port_to_host[port]
        with open('{}/{}.conf'.format(nginx_path, str(port)), 'w') as file:
            file.write("""server {{
  server_name   {}.{};

  location / {{
    proxy_pass        http://127.0.0.1:{};
    proxy_set_header  X-Real-IP  $remote_addr;
    proxy_set_header  Host $host;
  }}
}}""".format(subdomain, domain, str(port)))
    os.system("/etc/init.d/nginx reload")


def add_route(port, subdomain):
    if port < 1000 and subdomain != controller_subdomain:
        return
    for dport in range(1, 60001):
        if dport in port_to_host.keys():
            dsubdomain = port_to_host[dport]
            if dsubdomain == subdomain:
                port_to_host.pop(dport, None)
    port_to_host[port] = subdomain


add_route(81, controller_subdomain)
set_from_maps()


@app.route("/<subdomain>/<port>")
def register(subdomain, port):
    port = int(str(port))
    if port < 1000 or port > 60000:
        abort(403)
    add_route(port, subdomain)
    set_from_maps()
    return "{}, {}!".format(port, subdomain)


app.run(host='0.0.0.0', port=81)
