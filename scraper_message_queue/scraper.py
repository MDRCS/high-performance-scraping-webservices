from urllib.request import urlopen
from bs4 import BeautifulSoup

import boto3
import botocore

# create sqs client
sqs = boto3.client('sqs', "us-west-2")

# create / open the SQS queue
queue = sqs.create_queue(QueueName="sqs_queue")
print(queue)

# read and parse the planets HTML
html = urlopen("http://0.0.0.0:8080/scraper_message_queue/planets.min.html")
bsobj = BeautifulSoup(html, "lxml")

planets = []
planet_rows = bsobj.html.body.div.table.findAll("tr", {"class": "planet"})

for i in planet_rows:
    tds = i.findAll("td")

    # get the URL
    more_info_url = tds[5].findAll("a")[0]["href"].strip()

    # send the URL to the queue
    sqs.send_message(QueueUrl=queue["QueueUrl"],
                     MessageBody=more_info_url)
    print("Sent %s to %s" % (more_info_url, queue["QueueUrl"]))

"""
    The code connects to the given account and the us-west-2 region of AWS. A queue is then created if one does not exist.
    Then, for each planet in the source content, the program sends a message which consists of the more info URL for the planet.
    At this point, there is no one listening to the queue, so the messages will sit there until eventually read or
    they expire. The default life for each message is 4 days.
"""
