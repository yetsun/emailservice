#!../bin/python
from flask import Flask, jsonify, request
from emailservice import EmailService

"""
This is the web interface of the email service API. It serve the REST API request 

The url is like
/emailservice?from=from@mail.com&to=to1@mail.com,to2@mail.com&subject=subject111&text=text111
"""

app = Flask(__name__)


SAMPLE_INPUT_JSON = {
    'from':'test_from@mail.com',
    'to':'test_to1@mail.com,test_to2@mail.com',
    'subject':'test subject',
    'text':'test text'
}

SAMPLE_OUTPUT_JSON = {'status': 0, 'messgae':'success'}
    

@app.route('/emailservice/api/v1.0/sendemail/help', methods = ['POST', 'GET'])
def help():
    """
    This is give help to the use of this API.
    It give an brief introduction of this API and how to use it, as well as sample input and output json.
    """

    
    sample_output_json = {'status': 0, 'messgae':'success'}
    
    help_message = "Welcome to the Email Service! This service is to send emails. " \
        + "Please provide all the following parameters: "\
        + "- from email address "\
        + "- to email address(es) "\
        + "- email subject "\
        + "- email content "\
        + "in a json object. Please refere the sample_json for an sample json of the format. "\
        + "The return result is also a json object. "\
        + "Typical errors are, in the format of status and message: " \
        + "- 0 success, "\
        + "- 1 from email address invalid, "\
        + "- 2 to email address invalid, "\
        + "- 3 subject and text both are empty, "\
        + "- 4 all email sender failed, "\
        + "- 5 configuration not complete. "\
        + "If you have any questions about this API, please contact admin@uber.com"
    
    return jsonify( { 'status': 0, 'message': help_message, 'sample_input_json': SAMPLE_INPUT_JSON, 'sample_output_json':SAMPLE_OUTPUT_JSON} )
    

@app.route('/emailservice/api/v1.0/sendemail', methods = ['POST'])
def send_email():
    

    json_dict = request.json
   
    if not json_dict.has_key("from") or not json_dict.has_key("to") or not json_dict.has_key("subject") or not json_dict.has_key("text"): 
        status = 101
        message = "Please provide from email address, to email address(es), email subject and email content in a json object. A sample json:" + str(SAMPLE_INPUT_JSON)
    else:       
        from_email = json_dict["from"]
        to_list = json_dict["to"]
        subject = json_dict["subject"]
        text = json_dict["text"]    
        status, message = EmailService().send_email(from_email, to_list, subject, text)
        
    
    return jsonify( { 'status': status, 'message': message } )

if __name__ == '__main__':
    app.run(debug = True)