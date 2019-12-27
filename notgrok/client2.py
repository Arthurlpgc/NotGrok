#!/usr/bin/env python3

import argparse
import json
import random
import requests
import subprocess
import sys
import time

class NullDevice():
    def write(self, s):
        pass

def main():
    # Discard stderr output
    # sys.stderr = NullDevice()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Does not grok.')

    subparsers = parser.add_subparsers(help='Functions')
    http_parser = subparsers.add_parser('http', help='Set up a subdomain in the remote server.')
    http_parser.add_argument('-c', '--controllerHostname', help='Hostname of the controller server.', required=True)
    http_parser.add_argument('-l', '--localPort', type=int, help='Number of the local port.', default=80)
    http_parser.add_argument('-r', '--remotePort', type=int, help='Number of the remote port.', default=random.randint(10000,60000))
    http_parser.add_argument('-s', '--subdomain', help='Name of the remote subdomain.', required=True)
    http_parser.set_defaults(command='http')


    tcp_parser = subparsers.add_parser('tcp', help='Set up a subdomain in the remote server.')
    tcp_parser.add_argument('-c', '--controllerHostname', help='Hostname of the controller server.', required=True)
    tcp_parser.add_argument('-l', '--localPort', type=int, help='Number of the local port.', required=True)
    tcp_parser.add_argument('-r', '--remotePort', type=int, help='Number of the remote port.', required=True)
    tcp_parser.set_defaults(command='tcp')

    arguments = parser.parse_args(sys.argv[1:])

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
            time.sleep(1000)
    except KeyboardInterrupt as e:
        print("Exiting...")

if __name__ == '__main__':
    main()
