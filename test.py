"""
This is the test cases of the email service

"""

from confutil import ConfUtil
from emailsendermailgun import EmailSenderMailGun
from emailsendermandrill import EmailSenderMandrill
from emailservice import EmailService


def _test(text, passed):
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
    _test("not conf.get('test')", not conf.get('test'))
    _test("configuration dict is not empty", bool(conf._conf)) 


def test_mailgun():
    """
    This is to test the MailGun implementation EmailSenderMailGun
    """
    
    mailgun = EmailSenderMailGun()
    status, message = mailgun.send('yetsun@gmail.com', ['youxiang2006@hotmail.com'], ['yetsun@gmail.com'], [], 'test1', 'testcontent1')
    _test("mailgun works", status == 0)

def test_mailgun_only_cc():
    """
    This is to test the MailGun implementation EmailSenderMailGun
    """
    mailgun = EmailSenderMailGun()
    status, message = mailgun.send('yetsun@gmail.com', [], ['yetsun@gmail.com'], [], 'test1', 'testcontent1')    
    _test("mailgun cannot send email without to", status == 1)
    
def test_mailgun_only_bcc():
    """
    This is to test the MailGun implementation EmailSenderMailGun
    """
    mailgun = EmailSenderMailGun()
    status, message = mailgun.send('yetsun@gmail.com', [], [], ['yetsun@gmail.com'], 'test1', 'testcontent1')    
    _test("mailgun cannot send email without to", status == 1)
    
def test_mandrill():
    """
    This is to test the Mandrill implementation EmailSenderMandrill
    """
    mandrill = EmailSenderMandrill()
    status, message = mandrill.send('yetsun@gmail.com', ['yetsun@gmail.com'], [], [], 'test', 'testcontent')
    _test("mandrill works", status == 0)
    

def test_mandrill_only_cc():
    """
    This is to test the Mandrill implementation EmailSenderMandrill
    """
    mandrill = EmailSenderMandrill()
    status, message = mandrill.send('yetsun@gmail.com', [], ['yetsun@gmail.com'], [], 'test mandrill only cc', 'testcontent')
    _test("mandrill works without to", status == 0)

def test_mandrill_only_bcc():
    """
    This is to test the Mandrill implementation EmailSenderMandrill
    """
    mandrill = EmailSenderMandrill()
    status, message = mandrill.send('yetsun@gmail.com', [], [], ['yetsun@gmail.com'], 'test mandril only bcc', 'testcontent')
    _test("mandrill works without to", status == 0)
    

def test_emailservice_validation():
    """
    This is to test the email address validation function in EmailService
    """
    
    emailService = EmailService()
    _test( "emailService.validate_email_address('yetsun@gmail.com')", (bool(emailService.validate_email_address('yetsun@gmail.com'))))
    _test( "emailService.validate_email_address('yetsun.yetsun@gmail.gmail.com')", (bool(emailService.validate_email_address('yetsun.yetsun@gmail.gmail.com'))))
    _test( "not emailService.validate_email_address('@gmail.com')", (bool(not emailService.validate_email_address('@gmail.com'))))
    _test( "not emailService.validate_email_address('test@gmail')", (bool(not emailService.validate_email_address('test@gmail'))))
    
def test_emailservice_send():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email("yetsun@gmail.com", ["yetsun@gmail.com"], ["yetsun@gmail.com"], "youxiang2006@hotmail.com", "test subject 101", "test content 102")
    _test('send email', status == 0)

def test_emailservice_send_only_to():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email("yetsun@gmail.com", "yetsun@gmail.com", None, None, "test subject only to", "test content 102")
    _test('send to only', status == 0)
    


def test_emailservice_send_only_cc():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email("yetsun@gmail.com", [], ["yetsun@gmail.com"], [], "test subject only cc", "test content 102")
    _test('send cc only and failover', status == 0)
    

def test_emailservice_send_only_bcc():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email("yetsun@gmail.com", ["xxx"], "yyyy", "yetsun@gmail.com", "test subject only bcc", "test content 102")
    _test('send bcc only and failover', status == 0)
        
def test_emailservice_send_invalid_from():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email(None, ["xxx"], "yyyy", "yetsun@gmail.com", "test subject only bcc", "test content 102")
    _test("validate from", status == 1)
    
def test_emailservice_send_invalid_from1():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email('xxxxx', ["xxx"], "yyyy", "yetsun@gmail.com", "test subject", "test content 102")
    _test("validate from", status == 1)
    
def test_emailservice_send_invalid_to_cc_bcc():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email('yetsun@gmail.com', ["xxx"], "yyyy", None, "test subject", "test content 102")
    _test("validate to/cc/bcc", status == 2)  
    
def test_emailservice_send_invalid_subject_text_empty():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email('yetsun@gmail.com', ["xxx"], "yyyy", 'youxiang2006@hotmail.com', None, "")
    _test("validate subject/text", status == 3)      
          
    
    
test_conf()
test_emailservice_validation()

test_mailgun()
test_mandrill()

test_mailgun_only_cc()
test_mailgun_only_bcc()

test_mandrill_only_cc()
test_mandrill_only_bcc()

test_emailservice_send_invalid_from()
test_emailservice_send_invalid_from1()
test_emailservice_send_invalid_to_cc_bcc()
test_emailservice_send_invalid_subject_text_empty()

test_emailservice_send()
test_emailservice_send_only_to()
test_emailservice_send_only_cc()
test_emailservice_send_only_bcc()




