import os,paramiko,time
import login

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

    for notification_type in notification_types:
        if notification_type in message:
            print(event)
            print(context)

            sns_subject = "CloudFormation %s" % (notification_type)
            sns_message = message.replace(",", "\n")

            if notification_type == "CREATE_COMPLETE":
                dispatcher()
            else:
                return True
        else:
            return True


def dispatcher():
    login.test()
    return True