from datetime import datetime


def lambda_handler():
    now = datetime.now()
    "{:%B %d, %Y}".format(datetime.now())
    print('Hello World!')
    print('Today is ' + now.strftime("%B %d, %Y") + ' and the time is ' + now.strftime("%H:%M."))
