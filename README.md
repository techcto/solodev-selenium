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

Install dependencies:

* Via terminal `make fetch-dependencies`
* PyCharm will prompt you to install dependencies when opening the project

Set your PATH

This project contains the windows exe's for chromedriver and geckodriver in the drivers/ folder, 
add this folder to your path or download your own drivers separately and add them to your path independent of this project.
If you are on Linux or Mac OS, this is the route you will have to take.

IDE Note
If you plan on using an IDE for developing tests, PyCharm is recommended, it is "more compatible" with the unittest
framework. Even with the unittest plugin installed for Visual Studio Code, I ran into issues with it not running 
one off tests properly during development. PyCharm recognizes them inherently, and works out of the box.

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

## Running in Browserstack

Running in Browserstack against an AWS Cloudformation can also be done in a few different ways.

* The first method is driven by your local machine. If you did the `make fetch-dependencies` above, then a simple `make run`
will build the test suite and execute the lambda function. Currently, the tests that run when you do this are the ones called in the
`try` statement of the `dispatcher` method in `lambda_function.py`. Eventually, entire test suites will be called, 
and which test suite you want to run can be an environment variable. 

* The second method is as the final step in the CI/CD pipeline when a new Solodev build happens. After builds are completed and deployed into
AWS, this project is rebuilt, the lambda function is executed, and just as above, the tests that run when you do this are the ones called in the
`try` statement of the `dispatcher` method in `lambda_function.py`. Eventually, entire test suites will be called, 
and which test suite you want to run can be an environment variable.

* Lastly, this repo is also configured to be built in AWS CodeBuild every time code is pushed to the master branch. When the build is complete
 it's copied to an S3 bucket. This kicks off a test against a Solodev Lite Cloudformation instance.


## Building and uploading the distributable package

This is done automatically in AWS Codebuild for Solodev, but if you would like to do it manually:

* Everything is summarized into a simple Makefile
* `make build-lambda-package`
* Upload the `build.zip` resulting file to your AWS Lambda function
* Set Lambda environment variables (same values as in docker-compose.yml)
    * `PYTHONPATH=/var/task/src:/var/task/lib`
    * `PATH=/var/task/bin`
* Adjust lambda function parameters to match your necessities, for the given example:
    * Timeout: +10 seconds
    * Memory: + 250MB 