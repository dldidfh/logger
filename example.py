from CallLog import CallLog

stream_logger = CallLog(log_name="stream", log_level="debug")
stream_logger.add_stream_handler(H_type='rich', log_level="d")
stream_logger.add_file_handler(path="log", H_type="R", log_level="i")

file_logger = CallLog(log_name="file", log_level="debug")
file_logger.add_file_handler(path="savelog", H_type="R", log_level="d")

stream_logger.debug("qwe")
file_logger.info("asd")
