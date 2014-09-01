Email Service
============

Jun Ye, yetsun@gmail.com, 09/01/2014


a service that accepts the necessary information and sends emails. It should provide an abstraction between two different email service providers. If one of the services goes down, your service can quickly failover to a different provider without affecting your customers.



##Technical track
back-end

##Reasoning behind your technical choices
It is built with Python. The web framework is Flask.

I haven't used Python in work. I learnt Python recently, it is easy and fun to learn and use Python. The Python code is much more concise than Java. I can focus more on the logic I want to make. The Python dynamic typing and duck typing are very interesting to me. It is very fast to code and deploy in Python too, which saves me a ton of time comparing to Java.

Flask is a light-weighted, easy to use web framework. The web part of this project is just to serve the HTTP POST request for the REST API. So I think Flask is a good fit for this project.

Overall, for this project, it's very interesting to use Python and explore new technologies. I enjoyed using Python and the whole time of making this project in the past 3 days.


##Trade-offs you might have made, anything you left out, or what you might do differently if you were to spend additional time on the project
I think one design trade off is to make this service a more general purpose service v.s. a more specific ones for specific topics, like customer communication, marketing, internal process notification... For the specific ones, email content templates can be pre-defined, so that the users don't have to send the whole email content every time.
 
Left over are 
-To support rich email content and attachment. The implementation so far just supports plain text. The left over is to support rich content like images, video... And also supporting HTML format email content, as well as attachment. 

-To support authentication and authorization. To check if the user is authenticated and authorized to use this API.

-security
To support HTTPS
To validate if the user has access to the 'from' email address

-reporting
reporting on the usage per from/to email address and email service providers
reporting on the failure rate of the email service providers

-logging
-naming the email address
-scheduling email deliver


##Link to other code you're particularly proud of
##Link to your resume or public profile
The code and resume are sent by email before. Please let me know if you need the code and resume too. My email address is yetsun@gmail.com. Thanks.




##How to use this service
The service APIs are RESTful APIs.

The main API calls should be made with HTTP POST. (Help API can be called with GET)
Any non-0 status code in HTTP response code is an error. The returned message tells more detailed information.

###Main API 
URL: 
/emailservice/api/v1.0/sendemail

There is no UI for this project. It is a REST API. It is accessible through HTTP POST requests, expecting a JSON object as input. And it will return an object as output too.


method: POST

input: 
- One from email address
- at least one to or cc or bcc email address
- email subject
- email content (Email subject and email content cannot be both empty)

input format: json

JSON key | Meaning
-------- | -------
from     | string, the sender email address
to       | string or list, the to email address(es)
cc       | string or list, the cc email address(es)
bcc      | string or list, the bcc email address(es)
subject  | the email subject
text     | full text content of the email to be sent


Following is a sample input json:
```
{
    'from':'test_from@mail.com',
    'to':['test_to1@mail.com, test_to2@mail.com'],
    'cc':'test_cc@mail.com',
    'bcc':['test_bcc1@mail.com', 'test_bcc2@mail.com'],
    'subject':'test subject',
    'text':'This is the test text as the email content. Again, this is the test text as the email content.'
}
```

output:
- status code 
- message 

output format: json
 
Following is a sample output json:
```
{'status': 0, 'message':'success'}
```
This is for successfully transaction.

You can consider any non-0 status code as an error. The message will give details. 
Following are typical errors, in the format of status code and message:
-1 from email address invalid
-2 to/cc/bcc email address invalid
-3 subject and text both are empty
-4 all email sender failed
-5 email provider configuration not complete


###Help API
Beside the main API, there is also a help API to give an introduction about the main API and how to use it. 
The URL is as followed:
/emailservice/api/v1.0/sendemail/help

method: POST or GET 
input: N/A


##Testing
There is no UI for this project. It can be tested through curl or any tool that can send HTTP POST requests.
-Unit test cases are included in test.py
-End to end test scripts are included in test_script.txt (using curl)

Following are the scripts to test the service deployed on EC2:

-send email to one address
```
curl -i -H "Content-Type: application/json" -X POST -d \
 '{"from":"yetsun@gmail.com","to":"yetsun@gmail.com", "subject":"test subject","text":"This is an test email."}' \
  http://54.68.21.228/emailservice/api/v1.0/sendemail
 
```
output:
```
{
  "message": "success", 
  "status": 0
}
```

-send email with to, cc and bcc address
```
curl -i -H "Content-Type: application/json" -X POST -d  \
'{"from":"yetsun@gmail.com","to":["yetsun@gmail.com", "youxiang2006@hotmail.com"], "cc": "yetsun@gmail.com", "bcc":["youxiang2006@hotmail.com"], "subject":"test subject full to/cc/bcc","text":"test text"}' \
 http://54.68.21.228/emailservice/api/v1.0/sendemail
```

output:
```
{
  "message": "success", 
  "status": 0
}
```


-send email with invalid to/cc/bcc, expects erroring out
```
curl -i -H "Content-Type: application/json" -X POST -d \
 '{"from":"yetsun@gmail.com","to":[],"cc":"@hotmail.com", "bcc": ["xxx"], "subject":"test subject","text":"test text"}'  \
 http://54.68.21.228/emailservice/api/v1.0/sendemail
```
output:
```
{
  "message": "No valid to/cc/bcc email address. Please provide at least one valid to/cc/bcc email address.", 
  "status": 2
}
```

##Architecture

![alt tag](https://raw.githubusercontent.com/yetsun/emailservice/master/image/email_service_layers.png)

It's a 3 layers architecture.
- The webinterface.py is the presentation layer. It serves the REST API requests.
- The EmailService is the business layer. It handles the business logic like email address validation, provides the abstraction of email service providers and failover.
- The EmailSender is the email service provider specific implementation. It actually calls the email service provider's API to send emails.
	There is one email sender implemented MailGun and another Mandrill. 
	During testing, it is found that MailGun doesn't support cc only emails, which are the emails with only the cc emails address, with no to address. This is a good test case for the fail over. When the MailGun is the current first email sender, and send an email with only the cc email address, it will failover to the Mandrill email sender.



##Amazon EC2 Deployment

This Email Service is deployed to Amazon EC2. It's available in 
http://54.68.21.228/emailservice/api/v1.0/sendemail
The help API is available in 
http://54.68.21.228/emailservice/api/v1.0/sendemail/help

Following is a test script:
```
curl -i -H "Content-Type: application/json" -X POST -d \
 '{"from":"yetsun@gmail.com","to":["yetsun@gmail.com", "youxiang2006@hotmail.com"], "cc":"yetsun@gmail.com", "subject":"test subject", "text":"This is a test email."}'  \
 http://54.68.21.228/emailservice/api/v1.0/sendemail
```


