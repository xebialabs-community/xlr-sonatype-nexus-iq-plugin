#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
      if nexusiqProxyUrl:
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
