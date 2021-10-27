# LMC Simulator
> An LMC simulator and translator writen in python. faster than the actual LMC because of course it is

**Please be aware,this is written in and requires Python 3.9 to run (uses the walrus `:=` operator)** 

## Usage
### Batch tests
```shell
python main.py -r path/to/assembly/file.txt path/to/tests.txt raw_bool
```
If the `raw_bool` is either `true` or `yes`, all the raw data from the tests will be returned to you. Useful if you have lots of tests and just want averages

### Translator
```shell
python main.py -t path/to/lmc/file.txt
```

## Possible future additions
- Output CSV file for test results
- Add in an optimiser? maybe