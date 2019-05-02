# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main File.
Read data base file path in arguments and start app.
"""
import os
import argparse
import application


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-dataFilePath", help="file path of the data base file")
    args = parser.parse_args()
    dataFilePath = args.dataFilePath

    if os.path.exists(dataFilePath):
        app = application.Application(dataFilePath)
        app.startApp()
    else:
        print "The path of the data base file is wrong.\nPlease, enter a good one in order to start the application."


if __name__ == "__main__":
    main()
