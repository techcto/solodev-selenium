import os,json,time
import paramiko
import boto3
import login

#Boot up AWS
cloudformation = boto3.client('cloudformation')

#Boot up tests
login = login.Login()

def lambda_handler(event, context):

    print("Run App")

    # Notification types
    env_notification_types = os.getenv("NOTIFICATION_TYPES", None)
    notification_types = env_notification_types.split(",") if env_notification_types else None
    if not notification_types:
        print("At least one CloudFormation notification type needs to be specified")
        return

    try:
        message = str(event["Records"][0]["Sns"]["Message"]).replace("\n", ",")
    except Exception:
        print("Message could not be parsed. Event: %s" % (event))
        return

    print(message)

    if "ResourceType='AWS::CloudFormation::Stack'" not in message:
        return

    print("Test type")

    if "ResourceStatus='CREATE_COMPLETE'" in message:
        print(event)
        print(context)

        if isinstance(message, str):
            try:
                snsMessage = json.loads(message)
            except Exception as e:
                print(e)
        elif isinstance(message, list):
            snsMessage = message[0]

        print(snsMessage)

        stackId = snsMessage["StackId"]
        physicalResourceId = snsMessage["PhysicalResourceId"]
        print(stackId)
        print(physicalResourceId)

        if stackId == physicalResourceId:
            stackResponse = cloudformation.describe_stacks(StackName=stackId)
            print(stackResponse)

        dispatcher()
    else:
        return True


def dispatcher():
    login.test()
    return True