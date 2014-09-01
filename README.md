Email Service
============

a service that accepts the necessary information and sends emails. It should provide an abstraction between two different email service providers. If one of the services goes down, your service can quickly failover to a different provider without affecting your customers.

REST API URL: 
/emailservice/api/v1.0/sendemail

method: POST
input: 
- One from email address
- at least one to or cc or bcc email address
- email subject
- email content (Email subject and email content cannot be both empty)
input format: json

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
-2 to email address invalid
-3 subject and text both are empty
-4 all email sender failed
-5 email provider configuration not complete



Beside this API, there is also a help API to give an introduction about the main API and how to use it. 
The URL is as followed:
emailservice/api/v1.0/sendemail/help

method: POST or GET 
input: N/A


A unit test suite is included (test.py)
Sample test script (uisng curl) is include (test_script.txt)


**Architecture***

![alt tag](https://raw.github.com/yetsun/emailservice/branch/path/to/img.png)

3 layers architecture
The webinterface.py is the presentation layer. It serves the REST API requests.
The EmailService is the business layer. It handles the business logic like email address validation, provides the abstraction of email service providers and failover.
The EmailSender is to email service provider specific implementation. It actually calls the email service provider's API to send emails.
	There is one email sender implemented the MailGun and another Mandrill. 
	During testing, it is found that MailGun doesn't support cc only emails, which are the emails with only the cc emails address, with no to address. This is a good test case for the fail over. When the MailGun is the current first email sender, and send an email with only the cc email address, it will failover to the Mandrill email sender.


**Amazon EC2 Deployment**

This Email Service is deployed to Amazon EC2. It's available in 
http://54.68.21.228/emailservice/api/v1.0/sendemail
The help API is available in 
http://54.68.21.228/emailservice/api/v1.0/sendemail/help

Following is a test script:
curl -i -H "Content-Type: application/json" -X POST -d  '{"from":"yetsun@gmail.com","to":["yetsun@gmail.com", "youxiang2006@hotmail.com"],"subject":"test subject301","text":"test text"}'  http://54.68.21.228/emailservice/api/v1.0/sendemail


**Design trade off***


**Left over**
- email rich content and attachment
The implementation so far just support plain text. The left over is the rich contents like including images, embedding video. And also supporting HTML format email content, as well as attachment. 
- authentication

- security
To support HTTPS
To validate if the user has access to the 'from' email address

- report
reporting on the usage per email address and email service provider
reporting on the failure rate of the email service provider

- loggin







