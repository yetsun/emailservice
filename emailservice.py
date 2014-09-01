import re
from emailsendermailgun import EmailSenderMailGun
from emailsendermandrill import EmailSenderMandrill

class EmailService:
    """
    This class is the service interface. 
    It will 
    - validate the emails address, subject and email content text
    - call EmailSender to send the emails. EmailSender is the email service providers. 
    - failover. EmailSerivce privode the abstract of the email service provides. 
      If one of the services goes down,  EmailService will quickly failover to a different provider without affecting the customers.
    """
    
    """
    class static variable
    It is to remember the last working email service provider. And start using it since then until it fails.
    """
    _sender_id = 0
    
    def __init__(self):
        self._senders = []
        self._senders.append(EmailSenderMailGun())
        self._senders.append(EmailSenderMandrill())
        
        
        
    
    def validate_email_address(self, email_address):
        """
        This is a helper method to validate the email address format
        return True if it is good.
        """
        return re.match(r"[a-zA-Z0-9]+(\.?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(\.?[a-zA-Z0-9]+)*\.[a-zA-Z0-9]{2,}", email_address)
            

    def list_or_str_to_valid_list(self, list_or_string):
        """
        This is a helper method to convert a string into a list with the string only
        Or if the input is already list, simply return itself
        Meanwhile if the email address is invalid, remove it from the list
        """
        if isinstance(list_or_string, list):            
            
            for email in list_or_string:
                if not self.validate_email_address(email):
                    list_or_string.remove(email)
            return list_or_string
            
        else:
            result_list = []            
            if self.validate_email_address(list_or_string):
                result_list.append(list_or_string)
            return result_list
    
        
    def send_email(self, from_email, to_list, cc_list, bcc_list, subject, text):
        """
        This is to send email by the email sender class and failover.
        It will also validate the from, to email address. Validate the subject and email content text.
        It will return an status code and message
        
        The to_list, cc_list and bcc_list could be None or an empty list [] or a string representing one email address, or a list of email addresses.
        But it should have at least one valid to or cc or bcc email address.
        
        status  message  
        0       success
        1       from email address invalid
        2       no valid to/cc/bcc email address
        3       subject and text both are empty
        4       all email sender failed
        5       configuration not complete
        """
                
        if from_email is None or len(from_email) == 0 or not self.validate_email_address(from_email):
            return 1, 'from email address invalid'
        
        if to_list is None or len(to_list) == 0:
            to_list = []
        else: 
            to_list = self.list_or_str_to_valid_list(to_list)
            
        if cc_list is None or len(cc_list) == 0:
            cc_list = []
        else: 
            cc_list = self.list_or_str_to_valid_list(cc_list)
            
        if bcc_list is None or len(bcc_list) == 0:
            bcc_list = []
        else:
            bcc_list = self.list_or_str_to_valid_list(bcc_list)

        
        if len(to_list) == 0 and len(cc_list) == 0 and len(bcc_list) == 0:
            return 2, 'No valid to/cc/bcc email address. Please provide at least one valid to/cc/bcc email address.'            
            
        
        if not subject and not text:
            return 3, 'subject and text both are empty'
        elif not subject:
            suject = ''
        elif not text:
            text = ''
        
        status, message = self._senders[EmailService._sender_id].send(from_email, to_list, cc_list, bcc_list, subject, text);
        
        if status == 0:
            message = 'success'
        else:
            #failover to another email service provider implementation
            EmailService._sender_id = (EmailService._sender_id + 1) % len(self._senders)
            status, message = self._senders[EmailService._sender_id].send(from_email, to_list, cc_list, bcc_list, subject, text);
            if status == 0:
                message = 'success'
            else:
                status = 4
                message = 'Emails failed in sending. The error message is as followed:\n' + message
        
        return status, message
        
        
    