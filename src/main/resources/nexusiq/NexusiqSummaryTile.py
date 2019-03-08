#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest


username = nexusiqServer['username']
password = nexusiqServer['password']
httpRequest = HttpRequest(nexusiqServer, username, password)

apps = {}
violationsArray = []

# Fetching the list of policies
url = '/api/v2/policies/'
print "About to read Policy List"
response = httpRequest.get(url, contentType='application/json')
policyList = json.loads(response.getResponse())
#print json.dumps(policyList, indent=4)

# Grabbing policy name that matches the security-level
policy = [item for item in policyList['policies'] if item['name'] == secLevel ]
if policy:
  policyID = policy[0]['id']


  # Fetching policy voilations
  url = '/api/v2/policyViolations?p=%s' % policyID
  print "About to get violations from the response"
  response = httpRequest.get(url, contentType='application/json')
  violations = json.loads(response.getResponse())
  #print json.dumps(violations, indent=4)

  # Grabbing voilations for the matching application
  app = [item for item in violations['applicationViolations'] if item['application']['publicId'] == application]
  print app
  if app:
    for policyViolation in app[0]['policyViolations']:
      policyName = policyViolation['policyName']
      violationObject = {
          'appName'   : application,
          'stageId'   : policyViolation['stageId'],
          'reportUrl' : policyViolation['reportUrl'],
      }
      violationsArray.append(violationObject)

    appObject = {
      policyName : violationsArray
    }
    apps.update(appObject)
     
print "%s voilations for applicaton %s" % (secLevel, application)
data = json.dumps(apps)
print json.dumps(data, indent=4)
