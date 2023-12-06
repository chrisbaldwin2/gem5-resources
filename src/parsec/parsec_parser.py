#!/usr/bin/python3
import os
import functools
import getopt
import sys
import re

TEST = False

benchmarks = [
    "blackscholes", 
    "bodytrack", 
    "canneal", 
    "dedup", 
    "facesim", 
    "ferret", 
    "fluidanimate", 
    "freqmine", 
    "raytrace", 
    "streamcluster", 
    "swaptions", 
    "vips", 
    "x264"
]

sizes = [
    "simsmall",
    "simmedium",
    "simlarge"
]

class Logger:
    def __init__(self):
        self.file = open('./results.txt', 'w')

    def log(self, *args, **kwargs):
        # print(*args, **kwargs)
        string = format(' '.join(args))
        if(kwargs.get('sep', None)):
            string = format(kwargs['sep'].join(args))
        self.file.write(string + '\n')

    def exit(self):
        self.file.close()

logger = Logger()

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
    stats = [('simTicks',), ('board.cache_hierarchy.l1dcaches','prefetcher.prefetchers')]
    stats_dict = {}
    prefetcher_dict = {
        'prefetchers0': 'BOPPrefetcher',
        'prefetchers1': 'IrregularStreamBufferPrefetcher',
        'prefetchers2': 'SignaturePathPrefetcher',
        'prefetchers3': 'StridePrefetcher',
    }

    def __init__(self, address_type: str, test: str):
        self.address_type = address_type
        self.test = test

    def stats_path(self) -> str:
        return f'parsec_{self.address_type.upper()}/{self.test}/stats.txt'

    def process_line(self, line: str) -> str:
        pattern = re.compile('([\\w.]+)\\D+(\\d+\\.?\\d*)')
        match = re.match(pattern, line)
        if match == None:
            return ''
        # print(match.groups())
        return (match.group(1), match.group(2))

    def parse_stats(self):
        self.stats_dict = {}
        stats_set = set(self.stats)
        try:
            with open(self.stats_path(), 'r') as f:
                nextline = f.readline()
                while(len(stats_set) and len(nextline)):
                    for stat_group in stats_set:
                        if functools.reduce(lambda a, b: a and b, [stat in nextline for stat in stat_group]):
                            # print('stat', stat_group[-1], nextline, stat_group[-1] in nextline)
                            key, value = self.process_line(nextline)
                            if(stat_group[-1] not in key):
                                continue
                            for k,v in self.prefetcher_dict.items():
                                key = key.replace(k, v)
                            self.stats_dict[key] = self.stats_dict.get(key, '') + value
                    nextline = f.readline()
        except FileNotFoundError:
            pass
    
    def print_ticks(self):
        value = self.stats_dict.get('simTicks', None)
        if value != None:
            print(self.address_type, self.test, value, sep=', ')

    def print_all(self):
        for key, value in self.stats_dict.items():
            logger.log(self.address_type, self.test, key, value, sep=', ')

def cmdArgs() -> dict:
    def print_help():
        print('spec_parser.py -v,--virtual-address -p,--physical-address -s,--size=[test,train,ref]')
    va = False
    pa = False
    no = False
    size = 'simsmall'
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hvpns:",["virtual-address","physical-address", "no-prefetch", "size="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-v", "--virtual-address"):
            va = True
        elif opt in ("-p", "--physical-address"):
            pa = True
        elif opt in ("-n", "--no-prefetch"):
            no = True
        elif opt in ("-s", "--size"):
            if arg not in sizes:
                print(f'Size must be {sizes} not', arg)
                sys.exit(2)
            size = arg
    if not va and not pa and not no:
        va = True
        pa = True
        no = True
    return {
        'parse_va': va,
        'parse_pa': pa,
        'parse_no': no,
        'size': size,
        }

def main():
    # Get command line args
    cmdDict = cmdArgs()
    # Run testbenchs
    for benchmark in benchmarks:
        if cmdDict['parse_va']:
            vaResult = TestResult('va', benchmark)
            vaResult.parse_stats()
        if cmdDict['parse_pa']:
            paResult = TestResult('pa', benchmark)
            paResult.parse_stats()
        if cmdDict['parse_no']:
            noResult = TestResult('no', benchmark)
            noResult.parse_stats()
        if cmdDict['parse_va']:
            vaResult.print_ticks()
        if cmdDict['parse_pa']:
            paResult.print_ticks()
        if cmdDict['parse_no']:
            noResult.print_ticks()
        if cmdDict['parse_va']:
            vaResult.print_all()
        if cmdDict['parse_pa']:
            paResult.print_all()
        if cmdDict['parse_no']:
            noResult.print_all()
    logger.exit()



if __name__ == '__main__':
    main()