"""
This is the test cases of the email service

"""

from confutil import ConfUtil
from emailsendermailgun import EmailSenderMailGun
from emailservice import EmailService


def test(text, passed):
    output = ''
    if passed:
        output += 'Pass  : '
    else:
        output += 'Fail! : '
    output += text;
    print output


conf = ConfUtil('/Users/junye/Workspaces/git/emailservice/emailsender.conf')
test("not conf.get('test')", not conf.get('test'))
test("configuration dict is not empty", bool(conf._conf)) 


mailgun = EmailSenderMailGun()
status, message = mailgun.send('yetsun@gmail.com', 'yetsun@gmail.com', 'test', 'testcontent')
test("mailgun works", status == 0)


emailService = EmailService()
test( "emailService.validate_email_address('yetsun@gmail.com')", (bool(emailService.validate_email_address('yetsun@gmail.com'))))
test( "emailService.validate_email_address('yetsun.yetsun@gmail.gmail.com')", (bool(emailService.validate_email_address('yetsun.yetsun@gmail.gmail.com'))))
test( "not emailService.validate_email_address('@gmail.com')", (bool(not emailService.validate_email_address('@gmail.com'))))
test( "not emailService.validate_email_address('test@gmail')", (bool(not emailService.validate_email_address('test@gmail'))))



