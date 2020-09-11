# Script to parse outlook entries of a timesheet for given month

How to use:

```
python3 main.py <filename> <M> <yyyy>
```

Example:

``` 
python3 main.py noi-kalender.csv 4 2020
```

NB: It will skip all lines that start with a `*`.

The output will be written to the same location of the input file. The filename is `<filename>.out`.
