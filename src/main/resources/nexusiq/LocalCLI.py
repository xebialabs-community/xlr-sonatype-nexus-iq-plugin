#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import java.lang.System as System
import java.lang.String as String

from java.lang import Exception
from java.io import PrintWriter
from java.io import StringWriter

from com.xebialabs.overthere import CmdLine, ConnectionOptions, OperatingSystemFamily
from com.xebialabs.overthere.util import CapturingOverthereExecutionOutputHandler, OverthereUtils
from com.xebialabs.overthere.local import LocalConnection, LocalFile

class Localcliscript():

   def __init__(self, cliJar, nexusiqUrl, nexusiqUserName, nexusiqPassword, nexusiqProxyUrl, nexusiqProxyUserName, nexusiqProxyPassword, app, stage, targetUrl):
      self.cmdLine = CmdLine()
      
      self.cmdLine.addArgument( 'java' )
      self.cmdLine.addArgument( '-jar' )
      self.cmdLine.addArgument( cliJar )
      self.cmdLine.addArgument( '--application-id')
      self.cmdLine.addArgument( app )
      self.cmdLine.addArgument( '--server-url' )
      self.cmdLine.addArgument( nexusiqUrl )
      self.cmdLine.addArgument( '--authentication' )
      self.cmdLine.addArgument( "%s:%s" % (nexusiqUserName,nexusiqPassword) )
      if nexusiqProxyUrl  != "DEFAULT":
        self.cmdLine.addArgument( '--proxy' )
        self.cmdLine.addArgument( nexusiqProxyUrl )
        self.cmdLine.addArgument( "%s:%s" % (nexusiqProxyUserName, nexusiqProxyPassword) )
      self.cmdLine.addArgument( '--ignore-system-errors' )
      self.cmdLine.addArgument( '--stage')
      self.cmdLine.addArgument( stage )
      self.cmdLine.addArgument( targetUrl )
      
      self.stdout = CapturingOverthereExecutionOutputHandler.capturingHandler()
      self.stderr = CapturingOverthereExecutionOutputHandler.capturingHandler()

   # End __init__

   def execute( self ):
      connection = None
      try:
         connection = LocalConnection.getLocalConnection()
         exitCode = connection.execute( self.stdout, self.stderr, self.cmdLine )
      except Exception, e:
            stacktrace = StringWriter()
            writer = PrintWriter(stacktrace, True)
            e.printStackTrace(writer)
            self.stderr.handleLine(stacktrace.toString())
            return 1
      finally:
            if connection is not None:
                connection.close()
      return exitCode
   # End execute


   def getStdout(self):
        return self.stdout.getOutput()
   # End getStdout

   def getStdoutLines(self):
        return self.stdout.getOutputLines()
   # End getStdoutLines

   def getStderr(self):
        return self.stderr.getOutput()
   # End getStderr

   def getStderrLines(self):
        return self.stderr.getOutputLines()
   # End getStderrLines

# End Class
