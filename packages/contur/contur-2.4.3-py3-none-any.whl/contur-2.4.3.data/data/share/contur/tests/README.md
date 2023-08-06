To run the python tests, do `make check` in the top contur directory.

How to update the reference data
================================

If the regressions tests are failing because of a change which means
the reference data need updating, here's how to do that.

First run `make check-keep`. This will build a test directory under $CONTUR_USER_DIR and will not delete it once the tests are done. 

The commands below assume you are in your local contur repository top directory.

In the `$CONTUR_USER_DIR/tests` you'll see the files `contur_run.db`, `contur.map` and `Summary.txt`. Copy these to your `test/sources` 
directory in your contur area. Rename `Summary.txt` to `single_yoda_run.txt`.

Likewise, for the yodastream test:

```
cp $CONTUR_USER_DIR/tests/yodastream_results.pkl tests/sources/yodastream_results_dict.pkl
```

For the contur-export test, currently this exports the existing source `contur.map`, so you need to rerun `make check-keep`, then copy the `contur.csv` from `$CONTUR_USER_DIR/tests` to `test/sources`.
