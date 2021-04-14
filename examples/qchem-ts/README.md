1. After you have the trimmed pdb file `res_9.pdb`, and h added pdb file `res_9_h.pdb` (using the pymol script), you run
```bash
python3 write_input.py -noh res_9.pdb -adh res_9_h.pdb -intmp qcinput_temp -c 2
```
This will generate a `template.pdb` and `1.inp` file. The `1.inp` file will need to be revised for the method, solvation, and second jobtype setting.
Or you can help revise the qcinput_temp and the write_input.py to make it more generalized.

2. If you want to make a input file for TS search directly from the crystal structure (`template.pdb`), you run
``` bash
python3 write_input.py -step 3 -pdb1 template.pdb -pdb2 met.pdb -intmp qcinput_temp -c 2
```
The `met.pdb` is a flat methyl that is inbetween substrate SAM and CAT which is closer to the true methyl group in TS in larger models

3. If you want to make a input file for TS search from the optimized reactant (`reactant.pdb`), you run
```bash
python3 write_input.py -step 3 -pdb1 reactant.pdb -pdb2 met.pdb -intmp qcinput_temp -c 2
```
The `qcinput_temp` is set for opt not ts, please revise the input file before you run a ts search.
Several things also need to be revised/added such as solvation, basis set, freq.
