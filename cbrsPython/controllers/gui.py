from Loggers.LoggerHandler import LoggerHandler as logger, LoggerHandler
from controllers.CLIUtils.enums import TestStatus
from Loggers.LoggerObserver import loggerObserver
from Loggers.CmdLogger import CmdLogger
from Loggers.XmlLogger import XmlLogger
from Loggers.DebugLogger import DebugLogger

observable = loggerObserver("C:\Users\iagmon\cbrsPython")
 
cmdLogger = CmdLogger()
observable.register(cmdLogger)

xmlLogger = XmlLogger()
observable.register(xmlLogger)

debugLogger = DebugLogger()
observable.register(debugLogger)

observable.start_Test("reg","artiq10")