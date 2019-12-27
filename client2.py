#!/usr/bin/env python3

import argparse
import json
import requests
import subprocess
import sys

class NullDevice():
    def write(self, s):
        pass

def main():
    # Discard stderr output
    # sys.stderr = NullDevice()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Does not grok.')
    parser.add_argument('--controllerHostname', help='Hostname of the controller server.')
    parser.add_argument('--localPort', help='Number of the local port.')
    parser.add_argument('--remotePort', help='Number of the remote port.')
    parser.add_argument('--subdomain', help='Name of the remote subdomain (for http tunneling only).')
    arguments = parser.parse_args(sys.argv[1:])

    if arguments.controllerHostname is None:
        print("error: controllerHostname must be specified")
        return 1
    if arguments.localPort is None:
        print("error: localPort must be specified")
        return 1
    if arguments.remotePort is None:
        print("error: remotePort must be specified")
        return 1

    # Register subdomains (for http tunneling only)
    if arguments.subdomain is not None:
        requests.get(
            'http://{}/{}/{}'.format(arguments.controllerHostname, arguments.subdomain, arguments.remotePort))

    # Start port forwarding
    ssh_target = "{user}@{host}".format_map({
        "host": arguments.controllerHostname,
        "user": "portforwarding",
    })
    ssh_binding = "{remote_port}:localhost:{local_port}".format_map({
        "local_port": arguments.localPort,
        "remote_port": arguments.remotePort,
    })
    try:
        while True:
            print("Starting connection...")
            process = subprocess.run(
                ["ssh", "-p", "722", "-o", "StrictHostKeyChecking=accept-new", "-i", "./id_rsa", "-R", ssh_binding, ssh_target, "-N", "-T", "0.0.0.0"])
    except KeyboardInterrupt as e:
        print("Exiting...")

if __name__ == '__main__':
    main()
