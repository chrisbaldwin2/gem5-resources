#!/usr/bin/python3
import os
import functools
import getopt
import sys
import re

TEST = False

benchmarks = [
    "500.perlbench_r",
    "502.gcc_r",
    "503.bwaves_r",
    "505.mcf_r",
    "507.cactusBSSN_r",
    "508.namd_r",
    "510.parest_r",
    "511.povray_r",
    "519.lbm_r",
    "520.omnetpp_r",
    "521.wrf_r",
    "523.xalancbmk_r",
    "525.x264_r",
    "527.cam4_r",
    "531.deepsjeng_r",
    "538.imagick_r",
    "541.leela_r",
    "544.nab_r",
    "548.exchange2_r",
    "549.fotonik3d_r",
    "554.roms_r",
    "557.xz_r",
    "600.perlbench_s",
    "602.gcc_s",
    "603.bwaves_s",
    "605.mcf_s",
    "607.cactusBSSN_s",
    "608.namd_s",
    "610.parest_s",
    "611.povray_s",
    "619.lbm_s",
    "620.omnetpp_s",
    "621.wrf_s",
    "623.xalancbmk_s",
    "625.x264_s",
    "627.cam4_s",
    "631.deepsjeng_s",
    "638.imagick_s",
    "641.leela_s",
    "644.nab_s",
    "648.exchange2_s",
    "649.fotonik3d_s",
    "654.roms_s",
    "996.specrand_fs",
    "997.specrand_fr",
    "998.specrand_is",
    "999.specrand_ir",
]

# Create contex manager to change directory
class cd:
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)

class TestResult:
    stats = ['simTicks']

    def __init__(self, address_type: str, test: str):
        self.address_type = address_type
        self.test = test

    def stats_path(self) -> str:
        return f'{self.address_type.upper()}/{self.test}/stats.txt'
    
    def process_line(self, line: str) -> str:
        pattern = re.compile('\\D+(\\d+.?\\d*)')
        match = re.match(pattern, line)
        if match == None:
            return ''
        # print(match.groups())
        return match.group(1)

    def parse_stats(self):
        self.stats_dict = {}
        stats_set = set(self.stats)
        with open(self.stats_path(), 'r') as f:
            nextline = f.readline()
            while(len(stats_set) and len(nextline)):
                for stat in stats_set:
                    if stat in nextline:
                        self.stats_dict[stat] = self.stats_dict.get(stat, '') + self.process_line(nextline)
                nextline = f.readline()
    
    def print_stats(self):
        print(self.address_type, self.test)
        for key, value in self.stats_dict.items():
            # print('\t',key, value)
            print(value)

def cmdArgs() -> dict:
    def print_help():
        print('spec_parser.py -v,--virtual-address -p,--physical-address -s,--size=[test,train,ref]')
    va = False
    pa = False
    no = False
    size = 'test'
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hvps:",["virtual-address","physical-address", "size="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-v", "--virtual-address"):
            va = True
            if pa == True:
                print('Either va or pa must be chosen, not both')
                sys.exit(2)
        elif opt in ("-p", "--physical-address"):
            pa = True
            if va == True:
                print('Either va or pa must be chosen, not both')
                sys.exit(2)
        elif opt in ("-s", "--size"):
            if arg not in ('test','train','ref'):
                print('Size must be [test,train,ref] not', arg)
                sys.exit(2)
            size = arg
    address = 'VA' if va and not pa else 'PA'
    print('Address is', address)
    return {
        'va_or_pa': address,
        'size': size,
        }

def main():
    # Get command line args
    cmdDict = cmdArgs()
    # Run testbenchs
    for benchmark in benchmarks:
        vaResult = TestResult('va', benchmark)
        paResult = TestResult('pa', benchmark)
        noResult = TestResult('no', benchmark)
        vaResult.parse_stats()
        vaResult.print_stats()
        paResult.parse_stats()
        paResult.print_stats()
        noResult.parse_stats()
        noResult.print_stats()



if __name__ == '__main__':
    main()