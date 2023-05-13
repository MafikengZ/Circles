
init:
	C:\Users\SelloMaf\Desktop\Devops\circles\.venv\Scripts\python.exe -m pip install --upgrade pip
	pip install -r requirements.txt

install:
	#Used for packaging and publishing
	#pip install setuptools wheel twine
	#Used for linting
	pip install flake8 
	# Used for testing 
	pip install pytest

test:
	echo "Test not Implemented yet!"
	#python3 -m pytest -vv tests/*.py

format:
	black *.py loggins/*.py
	black *.py models/*.py 
	black *.py routes/*.py 
	black *.py schema/*.py 
	black *.py tests/*.py 

lint:
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --statistics

refactor: format lint


all: init install refactor test