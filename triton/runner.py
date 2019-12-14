#  Copyright (c) Yurzs 2020.
import argparse

from triton.server.glob import global_loop
from triton.server import Server

parser = argparse.ArgumentParser()
parser.add_argument("config", help="path to config file", type=str)

parser.add_argument("--log", help="level of logging", type=str, choices=["DEBUG", "INFO"])

args = parser.parse_args()


server = Server(args.config, host="0.0.0.0", loop=global_loop, )
server.start()
