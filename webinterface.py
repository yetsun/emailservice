#!../bin/python
from flask import Flask, jsonify, request
from emailservice import EmailService

"""
This is the web interface of the email service API. It serves the REST API requests. 

The url is like
/emailservice/api/v1.0/sendemail, the main API
/emailservice/api/v1.0/sendemail/help, for help

"""

app = Flask(__name__)


SAMPLE_INPUT_JSON = {
    'from':'test_from@mail.com',
    'to':['test_to1@mail.com,test_to2@mail.com'],
    'cc':'test_cc@mail.com',
    'bcc':['test_bcc1@mail.com', 'test_bcc2@mail.com'],
    'subject':'test subject',
    'text':'This is the test text as the email content. Again, this is the test text as the email content.'
}

SAMPLE_OUTPUT_JSON = {'status': 0, 'messgae':'success'}
    

@app.route('/emailservice/api/v1.0/sendemail/help', methods = ['POST', 'GET'])
def help():
    """
    This is the help of this API.
    It gives an brief introduction to this API and how to use it, as well as a sample input and a output json.
    """

    
    sample_output_json = {'status': 0, 'messgae':'success'}
    
    help_message = "Welcome to the Email Service! This service is to send emails. " \
        + "Please provide the following parameters: "\
        + "- from email address "\
        + "- to email address(es) (a list or a string if only one email address)"\
        + "- cc email address(es) (a list or a string if only one email address)"\
        + "- bcc email address(es) (a list or a string if only one email address)"\
        + " please provide at least one valid to or cc or bcc email address"\
        + "- email subject "\
        + "- email content "\
        + "in a json object. Please refere the sample_input_json. "\
        + "The return result is also a json object. Please refere the sampel_output_json."\
        + "Typical errors are (in the format of status and message): " \
        + "- 0 success, "\
        + "- 1 from email address invalid, "\
        + "- 2 no valid to/cc/bcc email address, "\
        + "- 3 subject and text both are empty, "\
        + "- 4 all email sender failed, "\
        + "- 5 configuration not complete. "\
        + "If you have any questions about this API, please contact admin@uber.com. Thank you."
    
    return jsonify( { 'status': 0, 'message': help_message, 'sample_input_json': SAMPLE_INPUT_JSON, 'sample_output_json':SAMPLE_OUTPUT_JSON} )
    



@app.route('/emailservice/api/v1.0/sendemail', methods = ['POST'])
def send_email():
    

    json_dict = request.json
   
    if not json_dict.has_key("from") \
        or (not json_dict.has_key("to") and not json_dict.has_key("cc") and not json_dict.has_key("bcc")) \
        or (not json_dict.has_key("subject") or not json_dict.has_key("text")): 
        
        status = 101
        message = "Please provide from email address, to/cc/bcc email address(es), email subject and email content in a json object. A sample json:" + str(SAMPLE_INPUT_JSON)
    else:       
        from_email = json_dict["from"]
        
        to_list = None
        cc_list = None
        bcc_list = None
        subject = None
        text = None
        
        if json_dict.has_key("to"):
            to_list = json_dict["to"]
            
        if json_dict.has_key("cc"):
            cc_list = json_dict["cc"]
        
        if json_dict.has_key("bcc"):
            bcc_list = json_dict["bcc"]
        
        if json_dict.has_key("subject"):
            subject = json_dict["subject"]
            
        if json_dict.has_key("text"):
            text = json_dict["text"] 
                   
        status, message = EmailService().send_email(from_email, to_list, cc_list, bcc_list, subject, text)
        
    
    return jsonify( { 'status': status, 'message': message } )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)    