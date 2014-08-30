import requests
from confutil import ConfUtil 

class EmailSenderMailGun:
    """
    This is the email sender class using the MailGun implementation.
    It gets 
    """
    def __init__(self):
        self._conf = ConfUtil('emailsender.conf')
        
        
        
    def send(self, from_email, to, subject, text):
        """
        this is to acutally send the email
        return 0 if the sending sucess
        return 1 if the sending failed
        return 5 if the configuration is not complete
        """
        api_url = self._conf.get('mailgun_api_url');
        key = self._conf.get('mailgun_key');
        
        if not api_url or not key:
            return 5, 'configuration not complete'
        else:
            response = requests.post(
                api_url,
                auth=('api', key),
                data={
                    'from':from_email,
                    'to':to,
                    'subject':subject,
                    'text':text
                })
            if response.ok:
                status = 0
            else:
                status = 1
            message = str(response.content)
                            
            return status, message
                
        
    
    
    
    