import os,json,time
import paramiko
import boto3
import login

#Boot up AWS
cloudformation = boto3.client('cloudformation')

#Boot up tests
login = login.Login()

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

#Activate Scobot
def lambda_handler(event, context):

    print("Hello.  I am Scobot.")

    # Notification types
    env_notification_types = os.getenv("NOTIFICATION_TYPES", None)
    notification_types = env_notification_types.split(",") if env_notification_types else None
    if not notification_types:
        print("Scobot says: At least one CloudFormation notification type needs to be specified")
        return
    try:
        message = json2obj(event['Records'][0]['Sns']['Message'][0])
    except Exception:
        print("Scobot says: Message could not be parsed. Event: %s" % (event))
        return

    print(message)

    if "ResourceType='AWS::CloudFormation::Stack'" not in message:
        return

    if "ResourceStatus='CREATE_COMPLETE'" in message:
        print(event)
        print(context)

        stackName = message['StackName']
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