import requests
from confutil import ConfUtil 

class EmailSenderMailGun:
    """
    This is the email sender class using the MailGun implementation.
    The interface is send(self, from_email, to_list, cc_list, bcc_list, subject, text)
    """
    def __init__(self):
        self._conf = ConfUtil('emailsender.conf')
        
        
        
    def send(self, from_email, to_list, cc_list, bcc_list, subject, text):
        """
        this is to acutally send the email
        
        from_email is one single email address
        to_list is a list of email address. It could be an empty list.
        cc_list is a list. It could be an empty list.
        bcc_list is a list. It could be an empty list.
        
        return 0 if the sending sucess
        return 1 if the sending failed
        return 5 if the configuration is not complete
        """
        api_url = self._conf.get('mailgun_api_url');
        key = self._conf.get('mailgun_key');
                        
        data_dict = {'from':from_email,
                'subject':subject,
                'text':text
            }
        
        if len(to_list) > 0:
            data_dict['to'] = ','.join(to_list)
        
        if len(cc_list) > 0:
            data_dict['cc'] = ','.join(cc_list)
        
        if len(bcc_list) > 0:
            data_dict['bcc'] = ','.join(bcc_list)
        
        #print data_dict
        
        if not api_url or not key:
            return 5, 'configuration not complete'
        else:
            response = requests.post(
                api_url,
                auth=('api', key),
                data=data_dict)
                
            if response.ok:
                status = 0
            else:
                status = 1
            message = str(response.content)
            
            #print 'mailgun'
            #print status
            #print message
                            
            return status, message
                
        
    
    
    
    