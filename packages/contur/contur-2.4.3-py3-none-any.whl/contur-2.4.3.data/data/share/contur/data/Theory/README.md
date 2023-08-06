 ###  SM theory predictions

To add new SM theory predictions to the contur release, you need to

   * Get them into YODA file format and put them in your local copy of this directory. The histogram path names should start with ``/THY/`` and otherwise
match the histograms they are intended to be compared to. 
   * The details of what the prediction is and where it comes from should then be added to the ``theory_predictions`` table in the analysis database [here](../DB/analyses.sql).
   * Any original data (e.g. CSV files from a theorist etc) should be archived in [``TheoryRaw`` directory](../TheoryRaw), and any code used to build the Theory.yoda file from these should be implemented in [``sm_theory_builders.py``](../../contur/data/sm_theory_builders.py) and hooked in to [``run_mkthy.py``](../../contur/run/run_mkthy.py) so that it can be redone if necessary using `contur-mkthy`.

There are lots of examples in [``sm_theory_builders.py``](../../contur/data/sm_theory_builders.py) of standard or semi-standard ways of building Theory yodas from various sources.

Several predictions for the same cross section may be stored here, but the one that is used is the one which has ID "A" in the table. In future
users will be able to select which predictions to use, probably with a config file, but at the moment the simplest way to do this is probably to either change
the ID in the DB and rebuild the DB, or else add a special conditional when `load_bg_data` is called in [``yoda_factory``](../../contur/factories/yoda_factories.py).




