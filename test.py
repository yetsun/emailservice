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
    """
    This is to test the ConfUtil, which is to read the configuration file.
    """
    
    conf = ConfUtil('/Users/junye/Workspaces/git/emailservice/emailsender.conf')
    test("not conf.get('test')", not conf.get('test'))
    test("configuration dict is not empty", bool(conf._conf)) 


def test_mailgun():
    """
    This is to test the MailGun implementation EmailSenderMailGun
    """
    
    mailgun = EmailSenderMailGun()
    status, message = mailgun.send('yetsun@gmail.com', ['youxiang2006@hotmail.com'], ['yetsun@gmail.com'], [], 'test1', 'testcontent1')
    print status
    print message
    #test("mailgun works", status == 0)


def test_emailservice_validation():
    """
    This is to test the email address validation function in EmailService
    """
    
    emailService = EmailService()
    test( "emailService.validate_email_address('yetsun@gmail.com')", (bool(emailService.validate_email_address('yetsun@gmail.com'))))
    test( "emailService.validate_email_address('yetsun.yetsun@gmail.gmail.com')", (bool(emailService.validate_email_address('yetsun.yetsun@gmail.gmail.com'))))
    test( "not emailService.validate_email_address('@gmail.com')", (bool(not emailService.validate_email_address('@gmail.com'))))
    test( "not emailService.validate_email_address('test@gmail')", (bool(not emailService.validate_email_address('test@gmail'))))
    
def test_emailservice_send():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email("yetsun@gmail.com", ["yetsun@gmail.com"], ["yetsun@gmail.com"], "youxiang2006@hotmail.com", "test subject 101", "test content 102")
    print status
    print message

def test_emailservice_send_only_to():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email("yetsun@gmail.com", "yetsun@gmail.com", None, None, "test subject only to", "test content 102")
    print status
    print message


def test_emailservice_send_only_cc():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email("yetsun@gmail.com", [], ["yetsun@gmail.com"], [], "test subject only cc", "test content 102")
    print status
    print message
    

def test_emailservice_send_only_bcc():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email("yetsun@gmail.com", ["xxx"], "yyyy", "yetsun@gmail.com", "test subject only bcc", "test content 102")
    print status
    print message
        
    
    
def test_maildrill():
    """
    This is to test the Mandrill implementation EmailSenderMandrill
    """
    mandrill = EmailSenderMandrill()
    status, message = mandrill.send('yetsun@gmail.com', ['yetsun@gmail.com'], [], [], 'test', 'testcontent')
    print status
    print message
    
#test_conf()
#test_emailservice_validation()

#test_mailgun()
#test_maildrill()
#test_emailservice_send()

#test_emailservice_send_only_to()
test_emailservice_send_only_cc()
#test_emailservice_send_only_bcc()


