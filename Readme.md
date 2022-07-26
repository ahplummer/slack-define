# Instructions

* Get an API key from [Merriam Webster](https://www.dictionaryapi.com/).
* Clone this repo into a clean directory. 
* Set environment variable for APIKEY
```
export APIKEY=<YOUR KEY>
```
* Build docker image:
```
docker-compose up -d --build
```
* Run docker image via docker-compose:
```
docker-compose exec defineword python3 flaskdriver.py
```
* Test with curl
```
curl --data "text=mytest=super awesome definition" http://127.0.0.1:8511/addspecial
```
* Output should look like:
`You've added that definition now, so feel free to do '/definespecial mytest' in Slack.`

* Test retrieval
```
curl --data "text=mytest" http://127.0.0.1:8511/definespecial
```
* Output should look like: `The special definition for mytest is: super awesome definition.`

## Local execution
* Build up Venv:
```
python3 -m venv .venv3
```
* Activate virtual env:
```
source .venv3/bin/activate
```
* Install requirements:
```
pip3 install -r defineword/requirements.txt
```
* Run:
```
cd defineword
python3 flaskdriver.py
```
* Test:
```
curl --data "text=mytest=super awesome definition" http://127.0.0.1:8511/addspecialword
```
* Validate:
```
curl --data "text=mytest" http://127.0.0.1:8511/getspecialword
```