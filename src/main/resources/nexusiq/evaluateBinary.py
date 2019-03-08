#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
import json
import urllib2
import base64
import os.path
import shutil
import uuid
from nexusiq.LocalCLI import Localcliscript

directoryCreated = False
baseDirectory = "work"

def createSafeDirectory():
    global directoryCreated
    try:
        # Strip leading slashes for protection - we place in our own work directory
        safeDirectory = os.path.join(baseDirectory,'nexusiq',str(uuid.uuid1()))
        print safeDirectory
        os.makedirs(safeDirectory)
        print "Made directory [%s]" % safeDirectory
        directoryCreated = safeDirectory
        return safeDirectory
    except OSError, e:
        if e.errno != 17:
            raise
        # time.sleep might help here
        print "Directory always exists [%s]" % e
        pass

def cleanupDirectory():
    print "Cleaning up [%s]" % directoryCreated
    shutil.rmtree(directoryCreated)
        

def retrieveRemoteFile():
    request = urllib2.Request(binaryLocation)
    artifactName = binaryLocation.rsplit('/', 1)[-1]
    if ( locationUsername ):
        base64string = base64.b64encode('%s:%s' % (locationUsername, locationPassword))
        request.add_header("Authorization", "Basic %s" % base64string)
    
    dir = createSafeDirectory()
 
    print "downloading with urllib2"
    f = urllib2.urlopen(request)
    print f.code
    with open(os.path.join(dir, artifactName), "wb") as code:
        code.write(f.read())
    
    print "Artifact written to [%s/%s]" % (dir, artifactName)
    return os.path.join(dir, artifactName)



# See if the input file is local or from a URL
if binaryLocation.startswith('http'):
    # Grab it from destination
    print "Retrieving file and temporarily storing it in [%s]" % outputPath
    binaryLocalPath = retrieveRemoteFile()
else:
    # File is already local
    binaryLocalPath = binaryLocation


# Now we have the file run it into NexusIQ for evaluation
print "Running [Localcliscript(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)]" % (cli['cliJar'], cli['url'], cli['username'], cli['password'], cli['proxyHost'],  cli['proxyUsername'], cli['proxyPassword'], nexusiqApp, nexusiqStage, binaryLocalPath)
cliScript = Localcliscript(cli['cliJar'], cli['url'], cli['username'], cli['password'], cli['proxyHost'],  cli['proxyUsername'], cli['proxyPassword'], nexusiqApp, nexusiqStage, binaryLocalPath)

exitCode = 1

try:
    exitCode = cliScript.execute()

    output = cliScript.getStdout()
    err = cliScript.getStderr()

    if (exitCode == 0 ):
        print "Finished normally"
        print output
    else:
        print
        print "### Exit code "
        print exitCode
        print
        print "### Output:"
        print output
     
        print "### Error stream:"
        print err
        print 
        print "----"
finally:  
    if (directoryCreated) :
        print "Cleaning up my mess"
        cleanupDirectory()
    sys.exit(exitCode)



