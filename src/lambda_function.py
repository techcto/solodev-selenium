import os,json,re,time
import boto3
import login

#Boot up AWS
cloudformation = boto3.client('cloudformation')

#Boot up tests
login = login.Login()

#Activate Scobot
def lambda_handler(event, context):

    print("Hello.  I am Scobot. 1.6")
    # print(message['Event'])

    # Notification types
    env_notification_types = os.getenv("NOTIFICATION_TYPES", None)
    notification_types = env_notification_types.split(",") if env_notification_types else None
    if not notification_types:
        print("Scobot says: At least one CloudFormation notification type needs to be specified")
        return
    
    #Test Message Type
    try:
        print("Test if this was called from SQS or SNS message!")
        try:
            message=json.loads(event['Records'][0]['body'])
            print(str(message))
            message = message['Message']
            print("This is a SQS message")           
        except BaseException as e:
            message = event['Records'][0]['Sns']['Message']
            print("This is a SNS message")
            print(str(message))
            print(str(e))
    except BaseException as e:
        print("Scobot says: Message could not be parsed. Event: %s" % (event))
        return

    message_handler(message)
    return True


def cloudformation_handler(stackId):
    stackResponse = cloudformation.describe_stacks(StackName=stackId)
    print(str(stackResponse))
    stack, = stackResponse['Stacks']
    outputs = stack['Outputs']

    out = {}
    for o in outputs:
        key = _to_env(o['OutputKey'])
        out[key] = o['OutputValue']
    print(json.dumps(out, indent=2))
    print("Scobot says: Wow, nice output")
    print("Scobot says: Dispatching URL to Selenium Tests")

    dispatcher(out['ADMIN_URL'], out['ADMIN_USERNAME'], out['ADMIN_PASSWORD'])

    return True


def message_handler(message):
    #Check SNS Status from Cloudformation Stack
    i = message.index("ResourceStatus='") + len("ResourceStatus='")
    j = message.index("'", i)
    resourceStatus = message[i:j]
    print("Scobot says: Cloudformation Status: ", resourceStatus)

    if "ResourceType='AWS::CloudFormation::Stack'" not in message:
        print("Scobot says: These are not the codes we are looking for")
        return True

    if "ResourceStatus='CREATE_COMPLETE'" in message:
        print(message)
        print("Scobot says: Wow, that is a lot of data")

        i = message.index("StackId='") + len("StackId='")
        j = message.index("'", i)
        stackId = message[i:j]
        
        print("Hmm, it looks like the stack id is: ", stackId)
        cloudformation_handler(stackId)
        return True
    else:
        print("Scobot says: Let's wait a bit more for this resource")
        return True


def dispatcher(url, username, password):
    try:
        login.test(url, username, password)
        print("Scobot says: That does it. See you next time.")
    except BaseException as e:
        print(str(e))
        print("Oh no, the test failed.  Please alert the team.")
        
    return True


def _to_env(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()