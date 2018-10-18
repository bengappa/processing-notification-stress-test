###
###			Processing Notification Stress Test
###                  10/18/18 | v1.0
###           Written by Benjamin A Gappa
###		
###    This script was built to test (a) all the different iterations of email we could potentially send to customers after a 
###    Processing Event and (b) send a critical mass of emails via CSV to stress test our email delivery so we are not exceeding
###    our hourly limit during high-traffic periods our products experience.
###
###    When installing boto3 you will be prompted for your AWS Credentials. Please follow AWS instructions on the topic.
###    https://aws.amazon.com/sdk-for-python/
###
###    The CSV file ProcessingNotificationTypes should be edited to change/add/remove the JSON objects being added to the queue.
###    These objects are then converted to HTML in a second queue and sent as emails via AWS Simple Email Service.
###    The variable define_queue should then be changed to send the JSON objects to a different queue

#					#
#	Import all      #
#					#
import boto3
import json
import csv
from Message import Message

#								#
#	Define the SQS Services     #
#								#

# Input SQS queue to be delivered to:
define_queue = # Define your queue here

# Set queue
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName= define_queue)

#               #
#   CSV Work    #
#               #

# Start counter
i = 0

# Open a CSV Reader
with open('ProcessingNotificationTypes.csv', 'r') as csvfile: 
    reader = csv.reader(csvfile)
   
    # For each row in the CSV, instantiate Message using the values in that row then turn it into a JSON
    # the default parameter is defined in order to serialize a Class object
    for row in reader:
        message_class_instance = Message(int(row[0]), int(row[1]), int(row[2]), int(row[3]), row[4], int(row[5]), str(row[6]), str(row[7]), int(row[8]), int(row[9]), int(row[10]), str(row[11]), str(row[12]), int(row[13]), int(row[14]), str(row[15]), bool(row[16]), bool(row[17]), bool(row[18]), bool(row[19]), bool(row[20]), bool(row[21]), int(row[22]), int(row[23]), int(row[24]), str(row[25]))
        j_message = json.dumps(message_class_instance, indent=4, default =lambda o: o.__dict__)

        # Increment the counter and print a statement every 10 messages
        i += 1
        if (i % 10) == 0:
            print("You've sent " + str(i) + " Messages")

        # The counter is necessary in order to send multiple messages to SQS
        # The last line, response, actually sends the message
        full_message = {'Id': str(i), 'MessageBody': j_message}
        response = queue.send_messages(Entries=[full_message])

        # Then we move to the next row of the CSV