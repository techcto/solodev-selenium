import os,json,time
import boto3
import login

#Boot up AWS
cloudformation = boto3.client('cloudformation')

#Boot up tests
login = login.Login()

#Activate Scobot
def lambda_handler(event, context):

    print("Hello.  I am Scobot. 1.1")

    # Notification types
    env_notification_types = os.getenv("NOTIFICATION_TYPES", None)
    notification_types = env_notification_types.split(",") if env_notification_types else None
    if not notification_types:
        print("Scobot says: At least one CloudFormation notification type needs to be specified")
        return
    try:
        message = json.loads(event['Records'][0]['Sns']['Message'])
    except Exception:
        print("Scobot says: Message could not be parsed. Event: %s" % (event))
        return

    print(message)

    if "ResourceType='AWS::CloudFormation::Stack'" not in message:
        return

    if "ResourceStatus='CREATE_COMPLETE'" in message:
        print(event)
        print(context)

        stackId = message['StackId']
        physicalResourceId = message['PhysicalResourceId']
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