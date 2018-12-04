import login

#Boot up tests
login = login.Login()

def lambda_handler(event, context):

    print("Run App")
    print(event)
    print(context)

    #Run Application
    dispatcher()

def dispatcher():
    login.test()
    return True