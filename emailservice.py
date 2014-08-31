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
            
        
    def send_email(self, from_email, to, subject, text):
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
        
        if not self.validate_email_address(to):
            return 2, 'to email address invalid'
        
        if not subject and not text:
            return 3, 'subject and text both are empty'
            
        
        status, message = self._senders[self._sender_id].send(from_email, to, subject, text);
        
        if status != 0:
            self._sender_id = (self._sender_id + 1) % len(self._senders)
            status, message = self._senders[self._sender_id].send(from_email, to, subject, text);
            if status == 5:
                return 5, 'configuration not complete'
            else:
                return 4, 'all message sender failed. error message:' + message
        
        return status, message
        
        
    