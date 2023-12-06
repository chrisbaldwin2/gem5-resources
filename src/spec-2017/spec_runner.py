#!/usr/bin/python3
import os
import functools
import getopt
import sys

TEST = False
'build/X86/gem5.opt configs/example/gem5_library/x86-parsec-benchmarks --benchmark blackscholes --size simsmall'
'build/X86/gem5.opt configs/example/gem5_library/x86-spec-cpu2017-benchmarks.py --image /home/chris/Programs/gem5-resources/src/spec-2017/disk-image/spec-2017/spec-2017-image/spec-2017 --partition 1 --benchmark 500.perlbench_r --size test'

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

def runGem5Test(benchmark: str, args: dict):
    cmd = f'build/X86/gem5.opt  --debug-flags="HWPrefetch" --debug-file="debug.log" --outdir="../{args["va_or_pa"]}/{benchmark}" configs/example/gem5_library/x86-spec-cpu2017-benchmarks.py --image /home/chris/Programs/gem5-resources/src/spec-2017/disk-image/spec-2017/spec-2017-image/spec-2017 --partition 1 --benchmark {benchmark} --size {args["size"]}'
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
        print('spec_runner.py -v,--virtual-address -p,--physical-address -s,--size=[test,train,ref]')
    va = False
    pa = False
    no = False
    size = 'test'
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
            if arg not in ('test','train','ref'):
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