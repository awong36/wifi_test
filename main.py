#!/usr/bin/python
# Project: wifi_test
# Description: iperf (client) test sequence for wireless testing
__author__ = "Adrian Wong"
import os, subprocess, argparse, logging, re, time


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


def normalize_space(s):
    """Return s stripped of leading/trailing whitespace
    and with internal runs of whitespace replaced by a single SPACE"""
    # This should be a str method :-(
    return ' '.join(s.split())


def reformatMsg(input):
    output = input.splitlines()
    removeSpace = [x for x in output if not x.isspace()]
    result = [normalize_space(i) for i in removeSpace]
    return result


def signalStrength(wifiConfig):
    pattern = re.compile("^\s+|\s*,\s*|\s+$")
    sigCmd, err = subprocess.Popen(['iwconfig', wifiConfig.interface], stdout=subprocess.PIPE).communicate()
    test = reformatMsg(sigCmd)
    print test[2], ", ", test[6]


def main():
    # main starts here
    wifiConfig = myConfig()
    parser = argSetup(wifiConfig)
    settings = parser.parse_args()
    logging.basicConfig(filename=wifiConfig.filename, level=logging.INFO)

    signalStrength(wifiConfig)

    cmd, err = subprocess.Popen(['iperf', '-c', settings.address, '-w', settings.window, '-n', settings.buffer],
                                stdout=subprocess.PIPE).communicate()
    test = reformatMsg(cmd)

    print test[2], ", ", test[4], ", ", test[5]
    # with cmd.stdout:
    #     for line in iter(cmd.stdout.readline, b''):
    #         print line,
    # cmd.wait()  # wait for the subprocess to exit

    signalStrength(wifiConfig)


if __name__ == "__main__":
    main()
