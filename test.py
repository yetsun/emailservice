"""
This is the test cases of the email service

"""

from confutil import ConfUtil
from emailsendermailgun import EmailSenderMailGun
from emailsendermandrill import EmailSenderMandrill
from emailservice import EmailService


def test(text, passed):
    output = ''
    if passed:
        output += 'Pass  : '
    else:
        output += 'Fail! : '
    output += text;
    print output

def test_conf():
    conf = ConfUtil('/Users/junye/Workspaces/git/emailservice/emailsender.conf')
    test("not conf.get('test')", not conf.get('test'))
    test("configuration dict is not empty", bool(conf._conf)) 


def test_mailgun():
    mailgun = EmailSenderMailGun()
    status, message = mailgun.send('yetsun@gmail.com', ['yetsun@gmail.com'], 'test1', 'testcontent1')
    print status
    print message
    #test("mailgun works", status == 0)


def test_emailservice_validation():
    emailService = EmailService()
    test( "emailService.validate_email_address('yetsun@gmail.com')", (bool(emailService.validate_email_address('yetsun@gmail.com'))))
    test( "emailService.validate_email_address('yetsun.yetsun@gmail.gmail.com')", (bool(emailService.validate_email_address('yetsun.yetsun@gmail.gmail.com'))))
    test( "not emailService.validate_email_address('@gmail.com')", (bool(not emailService.validate_email_address('@gmail.com'))))
    test( "not emailService.validate_email_address('test@gmail')", (bool(not emailService.validate_email_address('test@gmail'))))
    
def test_emailservice_send():
    emailservice = EmailService()
    status, message = emailservice.send_email("yetsun@gmail.com", ["yetsun@gmail.com", "youxiang2006@hotmail.com"], "test subject 101", "test content 102")
    print status
    print message

def test_maildrill():
    mandrill = EmailSenderMandrill()
    status, message = mandrill.send('yetsun@gmail.com', ['yetsun@gmail.com'], 'test', 'testcontent')
    print status
    print message
    
test_mailgun()
test_emailservice_send()

