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
    conn.request("POST", "/face/v1.0/persongroups/blue_cross_people/persons/081ec17f-ffdd-4da7-974a-ca2b1e1c3faf/persistedFaces?%s" % params, '{"url":"http://media.bizj.us/view/img/194511/04-12guyette-michael-bluecrossblue-shield*750.jpg"}', headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
