import argparse
import sys
from lux import app

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('port',help='the port at which the server should listen')
    args = parser.parse_args()

    try:
        port = int(args.port)
        if (type(port) != int) or (port < 0):
            raise Exception
    except Exception:
        print('Port must be a positive integer', file=sys.stderr)
        sys.exit(1)

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()