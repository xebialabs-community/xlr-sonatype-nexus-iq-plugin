#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
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



