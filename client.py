
import json
import requests
import subprocess
import sys


class NullDevice():
    def write(self, s):
        pass


sys.stderr = NullDevice()

with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())
    host_config = "{user}@{host}".format_map({
        "host": config["host"],
        "user": config["user"],
    })
    processes = []
    for entry in config['routes']:
        print(entry)
        requests.get(
            'http://{}/{}/{}'.format(config["host"], entry["subdomain"], entry["remote"]))
        remote_config = "{remote_port}:localhost:{local_port}".format_map({
            "local_port": entry["local"],
            "remote_port": entry["remote"],
        })
        process = subprocess.Popen(
            ["ssh", "-o", "StrictHostKeyChecking=accept-new", "-i", "./id_rsa", "-R", remote_config, host_config, "-N", "-T", "0.0.0.0"])
        processes.append(process)
    try:
        for process in processes:
            process.wait()
    finally:
        for process in processes:
            process.terminate()
