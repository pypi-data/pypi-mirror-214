import logging
import os
import sys
from opencensus.ext.azure.log_exporter import AzureLogHandler

# TODO: Long term aim : Head this to a library, can be re-used for various projects (e.g. tadpole, io, scenario gen)

app_logger={}

def get_logger(console_only=False):

    global app_logger

    current_pid = str(os.getpid())

    if current_pid in app_logger:
        print("returning existing logger " + current_pid)
        return app_logger[current_pid]
    else:
        log_level = os.getenv("FROG_LOG_LEVEL") or logging.DEBUG
        log_level = int(log_level)
        print(log_level)

        logger = logging.getLogger(current_pid)
        app_logger[current_pid] = logger

        # Add log to Insights
        if not console_only:
            print("Logging to Azure Insights")
            if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING") is not None:
                logger.addHandler(AzureLogHandler(connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")))
            else:
                print("APPLICATIONINSIGHTS_CONNECTION_STRING is not configured")

        # Add log to console
        print("Logging to console")
        stdhandler = logging.StreamHandler(sys.stdout)
        stdhandler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stdhandler.setFormatter(formatter)
        logger.addHandler(stdhandler)

        logger.setLevel(log_level)
        print("created logger for pid " + current_pid)

    return logger