#!/usr/bin/python
# Project: wifi_test
# Description: iperf (client) test sequence for wireless testing
__author__ = "Adrian Wong"
import os, subprocess, argparse, logging, time

class myConfig(object):
    # default values, these values can be overwritten by command line args
    address = '192.168.1.1'
    interface = 'wlan0'
    windowSize = '320K'
    buffer = '50M'
    cycle = '1'
    linuxPath = os.path.dirname(__file__)
    logPath = '/log/'  # log files storage path
    sysPath = '/system/'  # system required storage path
    log = 'example.log'
    filename = linuxPath + logPath + log

def argSetup(config):
    parser = argparse.ArgumentParser(description='iperf test sequence')
    parser.add_argument('-a', dest='address', nargs='?', default=config.address, type=str,
                        help='IP address or name of server')
    parser.add_argument('-i', dest='interface', nargs='?', default=config.interface, type=str,
                        help='wlan interface (default: wlan0)')
    parser.add_argument('-w', action='store', dest='window', nargs='?', default=config.windowSize, type=str,
                        help='TCP window size')
    parser.add_argument('-n', action='store', dest='buffer', nargs='?', default=config.buffer, type=str,
                        help='Transfer file size')
    parser.add_argument('-c', action='store', dest='cycle', nargs='?', default=config.cycle, type=int,
                        help='number of cycles')

    return parser

def signalStrength(wifiConfig):
    sigCmd = subprocess.Popen(['iwconfig', wifiConfig.interface], stdout=subprocess.PIPE)
    with sigCmd.stdout:
        for line in iter(sigCmd.stdout.readline, b''):
            print line,
        sigCmd.wait()  # wait for the subprocess to exit

def main():
    # main starts here
    wifiConfig = myConfig()
    parser = argSetup(wifiConfig)
    settings = parser.parse_args()
    logging.basicConfig(filename=wifiConfig.filename, level=logging.DEBUG)

    signalStrength(wifiConfig)

    cmd = subprocess.Popen(['iperf', '-c', settings.address, '-w', settings.window, '-n', settings.buffer], stdout=subprocess.PIPE)
    with cmd.stdout:
        for line in iter(cmd.stdout.readline, b''):
            print line,
    cmd.wait()  # wait for the subprocess to exit

    signalStrength(wifiConfig)

if __name__ == "__main__":
    main()
