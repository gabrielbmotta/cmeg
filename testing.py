from fieldline_api.fieldline_service import FieldLineService

import logging
import argparse
import queue
import time
import sys

if __name__ == "__main__":

    print("Hello there")

    ip_list = ['172.21.16.205', '172.21.16.237']

    fl = FieldLineService(ip_list)
    fl.open()

    sensors = fl.load_sensors()

    print(sensors)

    
