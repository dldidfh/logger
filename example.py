from CallLog import CallLog
import sys 
stream_logger = CallLog(log_name="stream", log_level="debug", log_extension="txt")
stream_logger.add_stream_handler(H_type='rich', log_level="d")
stream_logger.add_file_handler(path="log", H_type="R", log_level="d")

file_logger = CallLog(log_name="file", log_level="debug")
file_logger.add_file_handler(path="savelog", H_type="R", log_level="degub")

sys.excepthook = stream_logger.handle_exception

stream_logger.debug("qwe")
file_logger.info("asd")

file_logger.remove_file_handler()
stream_logger.remove_file_handler()
raise