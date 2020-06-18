# Check if Covid – Data Science (Experiments)
This repository contains Experimental _(non-production)_ Data Science work.

The `archive` directory contains code from previous contributors aimed at exploring data science solutions for predicting COVID-19. Data for that directory can be found in `archive/data`.

**05/05/2020:** Current working code can be found in `v2`. Operate inside that directory as if you were at the root of working project.

## On startu of EC2 (linux)
Run the following bash commands:
```
sudo yum update -y
sudo yum install python36
sudo yum install python36-pip
sudo yum install git -y
```
Then install the app
```
git clone https://github.com/checkifcovid/data-science-experiments.git
```
Then locate the project directory:
```
cd data-science-experiments/v2/
```
Make a virtual environment
```
python3 -m venv venv
```
Activate it:
```
source venv/bin/activate
```
Install the requirements:
```
pip3 install -r requirements.txt
```
Finally, launch the app!
```
python3 app.py
```
