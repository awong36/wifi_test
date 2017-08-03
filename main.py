#Project: wifi_test
#Description: iperf test sequence for wireless testing
__author__ = "Adrian Wong"
import subprocess, time, argparse


def main():
    #main starts here
    parser = argparse.ArgumentParser(description='iperf test sequence')
    parser.add_argument(dest='interface', nargs='?', default='wlan0', help='wlan interface (default: wlan0)')
    


if __name__ == "__main__":
    main()