import re
from emailsendermailgun import EmailSenderMailGun
from emailsendermandrill import EmailSenderMandrill

class EmailService:
    """
    This class is the service interface. It will call the actual email sender to send the message. 
    Meanwhile it will do failover. When once email sender failer, it will another email sender. 
    This is transparent to the user and will not affect the user.
    """
    
    
    def __init__(self):
        self._sender_id = 0
        self._senders = []
        self._senders.append(EmailSenderMailGun())
        self._senders.append(EmailSenderMandrill())
        
        
        
    
    def validate_email_address(self, email_address):
        return re.match(r"[a-zA-Z0-9]+(\.?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(\.?[a-zA-Z0-9]+)*\.[a-zA-Z0-9]{2,}", email_address)
            
        
    def send_email(self, from_email, to_list, subject, text):
        """
        This is to send email by the email sender class and failover on the class.
        It will also validate the from, to email address. Validate the subject and email content text.
        It will return an status code and message
        status  message  
        0       success
        1       from email address invalid
        2       to email address invalid
        3       subject and text both are empty
        4       all email sender failed
        5       configuration not complete
        """
        
        if not self.validate_email_address(from_email):
            return 1, 'from email address invalid'
        
        if to_list is None or len(to_list) == 0:
            return 2, 'to email address invalid'
        else:
            for to_email in to_list:
                if not self.validate_email_address(to_email):
                    to_list.remove(to_email)
                    
            if len(to_list) == 0:
                return 2, 'to email address invalid'
        
        if not subject and not text:
            return 3, 'subject and text both are empty'
            
        
        status, message = self._senders[self._sender_id].send(from_email, to_list, subject, text);
        
        if status == 0:
            message = 'success'
        else:
            self._sender_id = (self._sender_id + 1) % len(self._senders)
            status, message = self._senders[self._sender_id].send(from_email, to_list, subject, text);
            if status == 0:
                message = 'success'
            else:
                status = 4
                message = 'Emails failed in sending. The error message is as followed:\n' + message
        
        return status, message
        
        
    