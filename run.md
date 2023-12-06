To run go to the `gem5-resources/src/parsec` folder and run the `./parsec_runner.py` script with the appropriate flag for virtual `-v` physical `-p` or no prefetcher `-n`
The `./parsec_parser.py <flags>` will show which runs are done and dump the results in the results.txt 
which can be pasted into excel
For a progress bar, you can use the `./run_progress.py` script which monitors all of the current gem5 runs

### Gem5 Resources

[upstream](git@github.com:gem5/gem5-resources.git)

### Gem5 Branches
- p_pa : physical address prefetching
- p_va : virtual address prefetching
- p_stride : only stride prefetching pa (base config)

[origin](git@github.com:chrisbaldwin2/gem5.git)
[upstream](git@github.com:gem5/gem5.git)