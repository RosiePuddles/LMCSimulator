# LMC Simulator
> An LMC simulator and translator writen in python. faster than the actual LMC because of course it is

**Please be aware,this is written in and requires Python 3.9 to run (uses the walrus `:=` operator)** 

## Usage
### Batch tests
```shell
python main.py -b path/to/assembly/file.txt path/to/tests.txt raw_bool
```
If the `raw_bool` is either `true` or `yes`, all the raw data from the tests will be returned to you. Useful if you have lots of tests and just want averages

The returns the following:

- Number of passed and failed tests
- Number of mailboxes used
- Average time per test in nanoseconds
- Minimum and maximum number of cycles
- Mean average number of cycles
- Root mean squared (RMS) number of cycles

### Run a file
```shell
python main.py -r path/to/assembly/file.txt
```

Runs an assembly file. what else do you want?

### Translator
```shell
python main.py -t path/to/lmc/file.txt
```

## Possible future additions
- Output CSV file for test results
- Add in an optimiser? maybe