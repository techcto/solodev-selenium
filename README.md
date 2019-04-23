# Lambda Selenium For Solodev

Project for running tests on cloudformation templates using:

Selenium Python Bindings and the Selenium Webdriver

## Requirements

The project this is based on is explained [here](https://engineering.21buttons.com/crawling-thousands-of-products-using-aws-lambda-80332e259de1). 

Dependencies:
* Python 3.6
* Selenium 3.14.0
* boto3
* paramiko
* python-dotenv
* unittest
* [Chrome driver](https://sites.google.com/a/chromium.org/chromedriver/)
* [Gecko driver](https://github.com/mozilla/geckodriver/releases) (Firefox)
* [Small chromium binary](https://github.com/adieuadieu/serverless-chrome/releases)

Install docker and dependencies:

* `make fetch-dependencies`
* [Installing Docker](https://docs.docker.com/engine/installation/#get-started)
* [Installing Docker compose](https://docs.docker.com/compose/install/#install-compose)

Set your PATH

This project contains the windows exe's for chromedriver and geckodriver in the drivers/ folder, 
add this folder to your path or download your own drivers separately and add them to your path independent of this project.
If you are on Linux or Mac OS, this is the route you will have to take.

## Working locally

The original project, linked above, has an example running on docker locally, for the curious.

This project has 2 different methods of running tests locally. One for development, one for running complete tests.

The easiest way to run a single test is to run that test as a python unittest. 
If each test is set up according to the template (in the testcases folder), it should have everything it needs to run on its own, without the lambda function.
* In an IDE like PyCharm, just right click and select ` Run Unittests for test_name.TestClass`. 
* On the command line, it is very similar, `python test_name.py TestClass.test_name`, but the class and name are swapped.

Running the tests in the method described above relies on a check at the beginning of each test to determine if we are running locally or not
and the data stored in strings.py for all the localhost information. These strings are passed in as default values which are
overwritten when run as a lambda function. The webdriver is then built with whichever set of data is passed in. 

## Running in AWS

Running in AWS can also been done 2 different ways. 

* Placeholder for driving browserstack locally
* Placeholder for driving browserstack from lambda function 

## Building and uploading the distributable package

Everything is summarized into a simple Makefile so use:

* `make build-lambda-package`
* Upload the `build.zip` resulting file to your AWS Lambda function
* Set Lambda environment variables (same values as in docker-compose.yml)
    * `PYTHONPATH=/var/task/src:/var/task/lib`
    * `PATH=/var/task/bin`
* Adjust lambda function parameters to match your necessities, for the given example:
    * Timeout: +10 seconds
    * Memory: + 250MB 