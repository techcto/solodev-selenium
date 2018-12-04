import boto3,json,os,subprocess,base64,time,shutil
from botocore.vendored import requests
import paramiko

import login

#Boot up tests
login = login.Login()

def lambda_handler(event, context):

    print("Run App")
    print(event)
    print(context)


def dispatcher():
    login.test()
    return True