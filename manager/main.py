import builtins
import argparse
from manager import DeviceManager

parser = argparse.ArgumentParser(description='Start a new Device Simulator')
parser.add_argument('--broker', type=str, help='Broker Host to connect to', required=True)

args = parser.parse_args()
manager = DeviceManager(args.broker)

builtins.manager = manager
from app import app

if __name__ == "__main__":
    manager.client.loop_start()
    app.run(debug=True)

