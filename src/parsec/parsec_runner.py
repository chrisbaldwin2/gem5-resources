#!/usr/bin/python3
import os
import functools
import getopt
import sys

TEST = False
'build/X86/gem5.opt configs/example/gem5_library/x86-parsec-benchmarks --benchmark blackscholes --size simsmall'
'build/X86/gem5.opt configs/example/gem5_library/x86-spec-cpu2017-benchmarks.py --image /home/chris/Programs/gem5-resources/src/spec-2017/disk-image/spec-2017/spec-2017-image/spec-2017 --partition 1 --benchmark 500.perlbench_r --size test'

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

# Create contex manager to change directory
class cd:
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)

def runGem5Test(benchmark: str, args: dict):
    # cmd = f'build/X86/gem5.opt  --debug-flags="HWPrefetch" --debug-file="debug.log" --outdir="../{args["va_or_pa"]}/{benchmark}" configs/example/gem5_library/x86-spec-cpu2017-benchmarks.py --image /home/chris/Programs/gem5-resources/src/spec-2017/disk-image/spec-2017/spec-2017-image/spec-2017 --partition 1 --benchmark {benchmark} --size {args["size"]}'
    cmd = f'build/X86/gem5.opt --outdir="../parsec_{args["va_or_pa"]}/{benchmark}" configs/example/gem5_library/x86-parsec-benchmarks.py --benchmark {benchmark} --size {args["size"]} &'
    if not TEST:
        with cd('gem5'):
            ret = os.system(cmd)
    else:
        print(cmd)
        ret = 0
    # if ret != 0:
    #     raise Exception("Gem5 test failed with", ret)

def compileGem5():
    with cd("gem5"):
        ret = os.system("scons build/X86/gem5.opt -j32")
    if ret != 0:
        raise Exception("Scons build failed with", ret)

def cmdArgs() -> dict:
    def print_help():
        print('spec_runner.py -v,--virtual-address -p,--physical-address -n,--no-prefetch -s,--size=[test,train,ref]')
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
            if pa == True or no == True:
                print('Either no, va, or pa must be chosen, not more than one')
                sys.exit(2)
        elif opt in ("-p", "--physical-address"):
            pa = True
            if va == True or no == True:
                print('Either no, va, or pa must be chosen, not more than one')
                sys.exit(2)
        elif opt in ("-n", "--no-prefetch"):
            no = True
            if va == True or pa == True:
                print('Either no, va, or pa must be chosen, not more than one')
                sys.exit(2)
        elif opt in ("-s", "--size"):
            if arg not in sizes:
                print('Size must be [test,train,ref] not', arg)
                sys.exit(2)
            size = arg
    if va:
        address = 'VA'
    elif no:
        address = 'NO'
    else: #pa
        address = 'PA'
    print('Address is', address)
    return {
        'va_or_pa': address,
        'size': size,
        }

def main():
    # Get command line args
    cmdDict = cmdArgs()
    # Compile gem5 w/ scons
    compileGem5()
    # Run testbenchs
    for benchmark in benchmarks:
        runGem5Test(benchmark, cmdDict)



if __name__ == '__main__':
    main()