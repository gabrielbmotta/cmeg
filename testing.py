import os

from fieldline_api.fieldline_service import FieldLineService

import logging
import argparse
import queue
import time
import sys
import re

chassis_mac_addrs = ['00:0e:c6:5b:65:ab', '00:0e:c6:73:c7:31']

class Device:
    ip = ''
    name = ''
    mac_addr = ''

    def __init__(self, new_ip, new_name, new_mac):
        self.ip = new_ip
        self.name = new_name
        self.mac_addr = new_mac

def get_device_from_host_string(host_string):
    parsed_host_fields = re.search("(?P<name>^[^.]*).*\((?P<ip>[0-9.]*)\)\sat\s(?P<mac>[^ ]+)", host_string)
    return Device(parsed_host_fields.group('ip'), parsed_host_fields.group('name'), parsed_host_fields.group('mac'))

def get_fieldline_chassis_ip():
    hosts = []
    for host in os.popen("arp -a"):
        hosts.append(host)

    devices = []
    for host in hosts:
        device = get_device_from_host_string(host)
        if device.mac_addr in chassis_mac_addrs:
            devices.append(device)

    ip_list = []

    for chassis_mac in chassis_mac_addrs:
        for dev in devices:
            if dev.mac_addr == chassis_mac:
                ip_list.append(dev.ip)

    return ip_list


def restart_sensors(service):
    done = False
    def call_done():
        nonlocal done
        done = True

    sensors = service.load_sensors()
    service.set_closed_loop(True)
    service.restart_sensors(sensors,\
        on_next=lambda c_id,\
        s_id: print(f'sensor {c_id}:{s_id} finished restart'),\
        on_error=lambda c_id,\
        s_id,\
        err: print(f'sensor {c_id}:{s_id} failed with {hex(err)}'),\
        on_completed=lambda: call_done())
    
    while not done:
        time.sleep(0.5)

def coarse_zero_sensors(service):
    done = False
    def call_done():
        nonlocal done
        done = True

    sensors = service.load_sensors()
    service.coarse_zero_sensors(sensors,\
        on_next=lambda c_id,\
        s_id: print(f'sensor {c_id}:{s_id} finished coarse zero'),\
        on_error=lambda c_id,\
        s_id,\
        err: print(f'sensor {c_id}:{s_id} failed with {hex(err)}'),\
        on_completed=lambda: call_done())
    
    while not done:
        time.sleep(0.5)

def fine_zero_sensors(service):
    done = False
    def call_done():
        nonlocal done
        done = True

    sensors = service.load_sensors()
    service.fine_zero_sensors(sensors,\
        on_next=lambda c_id,\
        s_id: print(f'sensor {c_id}:{s_id} finished fine zero'),\
        on_error=lambda c_id,\
        s_id,\
        err: print(f'sensor {c_id}:{s_id} failed with {hex(err)}'),\
        on_completed=lambda: call_done())
    
    while not done:
        time.sleep(0.5)    

if __name__ == "__main__":

    print("Hello there")

    ip_list = get_fieldline_chassis_ip()
    print(ip_list)

    if len(ip_list) == 0:
        sys.exit("No devices found")

    fl = FieldLineService(ip_list)
    fl.open()

    restart_sensors(fl)
    coarse_zero_sensors(fl)
    fine_zero_sensors(fl)

    # sensors = fl.load_sensors()

    # print(sensors)

