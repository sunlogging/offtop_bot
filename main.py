import argparse
import asyncio

from _tools.commands import parser_command
from dotenv import dotenv_values

if __name__ == '__main__':

    parser = argparse.ArgumentParser('Guide for usage this script')
    parser.add_argument("--mode")
    args = parser.parse_args()
    if not parser_command(args.mode):
        exit()

    from _module.app import start_bot

    start_bot(dotenv_values(".env"))


