from flask import request
from flask import abort

from app import app

import base64
import json
import os

DEBUG = True

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

config = {
  "DEBUG": DEBUG,
}

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config.from_mapping(config)

@app.route('/mutate', methods=HTTP_METHODS)
def mutate():
  if DEBUG:
    print(request.headers, flush=True)
    print(request.data, flush=True)

  try:
    request_json = json.loads(request.data.decode('utf-8'))
  except Exception as e:
    print(str(e), flush = True)

  print(str(request_json), flush = True)

  patch = "[{ \"op\": \"add\", \"path\": \"/metadata/labels/powered-by\", \"value\": \"pet2cattle.com\" }]"
  patch_bytes = patch.encode('ascii')
  patch_base64_bytes = base64.b64encode(patch_bytes)
  patch_base64 = patch_base64_bytes.decode('ascii')

  print(request_json['request']['uid'])

  response = {
    "apiVersion": "admission.k8s.io/v1",
    "kind": "AdmissionReview",
    "response": {
      "uid": request_json['request']['uid'],
      "allowed": True,
      'patch': patch_base64,
      'patchType': "JSONPatch",
    }
  }

  return json.dumps(response), 200, {'ContentType':'application/json-patch+json'} 

@app.route('/<path:path>')
def catch_all(path):
  abort(404)