#!/usr/bin/env python3

import sys
import girder_client as gc


def main():
    if len(sys.argv) != 3:
        print("Veuillez préciser un nom d'utilisateur et un mot de passe")
        sys.exit(1)

    client = gc.GirderClient(apiUrl="http://34.76.208.101:8080/api/v1")
    client.authenticate(sys.argv[1], sys.argv[2])

    return 0

if __name__ == "__main__":
    main()
