from botocore.vendored import requests
import os
import json
import gzip
from StringIO import StringIO


URL = "https://logs.logdna.com/logs/ingest"
KEY = os.environ['LOGDNA_KEY']


def lambda_handler(event, context):
	# Retrieve CloudWatch logs and convert into dictionary
	cw_data = str(event['awslogs']['data'])
	cw_logs = gzip.GzipFile(fileobj=StringIO(cw_data.decode('base64', 'strict'))).read()
	cw_log_lines = json.loads(cw_logs)
	# Check for app and host options
	app = 'CloudWatch'
	hostname = 'CloudWatch'
	if 'logGroup' in cw_log_lines:
		hostname = cw_log_lines['logGroup'].split('/')[-1]
	if 'logStream' in cw_log_lines:
		app = cw_log_lines['logStream']
	json_object = { "lines": [] }
	for cw_log_line in cw_log_lines['logEvents']:
		msg = "\r".join(cw_log_line['message'].splitlines())
		print msg
		json_object["lines"].append({
			"line": msg,
			"timestamp": cw_log_line['timestamp'],
			"file": app
		})
	postLog(hostname, json.dumps(json_object))

def postLog(hostname, payload):
	headers = {
		"Content-Type": 'application/json; charset=UTF-8'
	}
	url = "%s?hostname=%s" % (URL, hostname)
	res = requests.post(url, headers=headers, auth=(KEY, ''), data=payload)
	print "%s: %s" % (res.status_code, res.text)
	return res
