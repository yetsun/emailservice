Email Service
============

a service that accepts the necessary information and sends emails. It should provide an abstraction between two different email service providers. If one of the services goes down, your service can quickly failover to a different provider without affecting your customers.

REST API URL
http://localhost:5000/emailservice/api/v1.0/sendemail

POST method

One from email address, at least one to email address, email subject and email content are required in a json as input. Email subject and email content cannot be all empty. Following is an sample input json:

{
    'from':'test_from@mail.com',
    'to':'test_to1@mail.com,test_to2@mail.com',
    'subject':'test subject',
    'text':'test text'
}

Output is a json object. 
Following is a sample

{'status': 0, 'messgae':'success'}

This is for successfully transaction.

You can consider any 0 status code as an error. The message will give details. Following are typical errors, in the format of status code and message:
1 from email address invalid
2 to email address invalid
3 subject and text both are empty
4 all email sender failed
5 email provider configuration not complete



Beside this API, there is also an help API. The URL is as followed:
http://localhost:5000/emailservice/api/v1.0/sendemail/help

Method POST or GET and it takes no input parameter. 

It is to help the user of the /sendemail API to understand what it is and how to use it.







