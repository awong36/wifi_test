#!/usr/bin/python
# Project: wifi_test
# Description: iperf (client) test sequence for wireless testing
__author__ = "Adrian Wong"
import os, subprocess, argparse, logging


def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


class myConfig(object):
    # default values, these values can be overwritten by command line args
    address = '192.168.1.1'
    interface = 'wlan0'
    windowSize = '320K'
    buffer = '50M'
    cycle = 1
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


def signalStrength(wifiConfig, logger):
    sigCmd, err = subprocess.Popen(['iwconfig', wifiConfig.interface], stdout=subprocess.PIPE).communicate()
    test = reformatMsg(sigCmd)
    print test[2], ", ", test[6]
    logger.info(str(test[2]) + ", " + str(test[6]))


def main():
    # main starts here
    wifiConfig = myConfig()
    parser = argSetup(wifiConfig)
    settings = parser.parse_args()
    logger = setup_logger('event_log', wifiConfig.filename)

    sigCmd, err = subprocess.Popen(['iwconfig', wifiConfig.interface], stdout=subprocess.PIPE).communicate()
    test = reformatMsg(sigCmd)
    Freq = test[1].split(' ', 3)

    x = 1
    while x <= settings.cycle:
        print "================== Test %r Begins ==================\n" % x
        logger.info("================== Test %r Begins ==================" % x)
        print Freq[1], Freq[2]
        logger.info(str(Freq[1] + Freq[2]))
        signalStrength(wifiConfig, logger)

        cmd, err = subprocess.Popen(['iperf', '-c', settings.address, '-w', settings.window, '-n', settings.buffer],
                                    stdout=subprocess.PIPE).communicate()
        test = reformatMsg(cmd)

        print test[2]
        print test[4].split('] ', 1)[1]
        print "Interval     | Transfer  | Bandwidth"
        print test[6].split('] ', 1)[1]

        logger.info(str(test[2]))
        logger.info(str(test[4].split('] ', 1)[1]))
        logger.info("Interval     | Transfer  | Bandwidth")
        logger.info(str(test[6].split('] ', 1)[1]))

        x += 1
    print "================== Test Completed =================="
    logger.info("================== Test Completed ==================")


if __name__ == "__main__":
    main()
