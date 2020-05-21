# properties-dataflow

In Cloud Shell, clone this repo

```
cd properties-dataflow
virtualenv -p python3.7 venv
source venv/bin/activate

pip install requirements.txt
```

To run locally (replacing the values in <>, i.e. `--output test_project:mydata:output`)

```
python process.py --output <your project>:<your dataset>.<output_table_name> --project <your project> --gmaps_key <your API key>
```
