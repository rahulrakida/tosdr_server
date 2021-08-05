from flask import Flask, render_template, url_for
import requests
import logging

# Download data from tosdr
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
TOSDR_API = 'https://api.tosdr.org/service/v1/'

logging.info(f'downloading data from [{TOSDR_API}]...')

request = requests.get(TOSDR_API)
data = request.json()
service_list = []

logging.info('processing data')
for service in data['parameters']['services']:
    if service['rating']['letter'] != 'N/A':
        entry = (service['name'], service['rating']['letter'], service['links']['crisp']['service'])
        service_list.append(entry)

service_list = sorted(service_list, key=lambda service: service[1])
logging.info('done')

# start flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', service_list=service_list)

@app.route("/json")
def return_json():
    return request.text.encode('utf-8')