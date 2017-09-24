import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '67e917dbf9ec40188a4945bb5e216138',
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/face/v1.0/identify?%s" % params, '{"personGroupId":"blue_cross_people","faceIds":["0b6dc65f-c7d6-4ad7-87af-38d40fcc3694"], "maxNumOfCandidatesReturned":1, "confidenceThreshold": 0.5}', headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
