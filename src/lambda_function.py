import os,json,re,time
import boto3
import login

#Boot up AWS
cloudformation = boto3.client('cloudformation')

#Boot up tests
login = login.Login()

#Activate Scobot
def lambda_handler(event, context):

    print("Hello.  I am Scobot. 1.3")
    # print(message['Event'])

    # Notification types
    env_notification_types = os.getenv("NOTIFICATION_TYPES", None)
    notification_types = env_notification_types.split(",") if env_notification_types else None
    if not notification_types:
        print("Scobot says: At least one CloudFormation notification type needs to be specified")
        return
    
    #Test Message Type
    try:
        print("Test if this was called from SQS or SNS message")
        print(str(event))
        try:
            print("Test for SQS event")
            message=json.loads(event['Records'][0]['body']['Message'])
            sqs_handler(message)
            print("This is a SQS message")           
        except BaseException as e:
            print("This is a SNS message")
            print(str(e))
            message = event['Records'][0]['Sns']['Message']
            sns_handler(message)
    except BaseException as e:
        print("Scobot says: Message could not be parsed. Event: %s" % (event))
        return

def cloudformation_handler(stackId):
    stackResponse = cloudformation.describe_stacks(StackName=stackId)
    stack = stackResponse['Stacks']
    outputs = stack['Outputs']

    out = {}
    for o in outputs:
        key = _to_env(o['OutputKey'])
        out[key] = o['OutputValue']
    print(json.dumps(out, indent=2))
    print("Scobot says: Wow, nice output")

    print("Scobot says: Dispatching URL to Selenium Tests")
    dispatcher(out['SOLODEV_IP'])

def sqs_handler(message):
    #Check Status from Cloudformation Stack
    resourceStatus = message['ResourceStatus']
    print("Scobot says: Cloudformation Status: ", resourceStatus)

    if message['ResourceType'] != 'AWS::CloudFormation::Stack':
        return

    if message['ResourceStatus'] == 'CREATE_COMPLETE':
        print(message)
        print("Scobot says: Wow, that is a lot of data")
        stackId = message['StackId']
        cloudformation_handler(stackId)
    else:
        print("Scobot Out.")
        return True

def sns_handler(message):
    #Check SNS Status from Cloudformation Stack
    i = message.index("ResourceStatus='") + len("ResourceStatus='")
    j = message.index("'", i)
    resourceStatus = message[i:j]
    print("Scobot says: Cloudformation Status: ", resourceStatus)

    if "ResourceType='AWS::CloudFormation::Stack'" not in message:
        return

    if "ResourceStatus='CREATE_COMPLETE'" in message:
        print(message)
        print("Scobot says: Wow, that is a lot of data")

        i = message.index("StackId='") + len("StackId='")
        j = message.index("'", i)
        stackId = message[i:j]
        
        cloudformation_handler(stackId)
    else:
        print("Scobot Out.")
        return True


def dispatcher(url):
    login.test(url)
    print("Scobot says: That does it. See you next time.")
    return True


def _to_env(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()