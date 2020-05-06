# Data Science – V2
_Find the Cluster – Data Science Workflow_

**05/05/2020:** Operate as if you're at the root of working project.

## Getting started:
1. set working directory to `v2`:
```
cd v2
```
2. create a virtual environment _(only do 1st time)_
```
python3 -m venv venv
```
3. activate the virtual environment
```
source venv/bin/activate
```
4. install requirements _(only do 1st time)_
```
pip install -r requirements.txt
```
5. run the code!
```
python3 main.py
```

**Note:** Make sure you have `aws credentials` either as environmental variables _or_ in a `secret` directory. Additionally, your bucket name should be stored in a file `aws_bucket_path.json` containing the key `"BUCKET_NAME"`. _(modification to this will be forthcoming)_
