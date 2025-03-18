import logging
import os
from datetime import datetime

log_dir = "D:\Data Science\Projects\Heart Disease Detection\logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file =f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# logs_path = os.path.join(os.getcwd(), 'logs', log_file)
# os.makedirs(logs_path, exist_ok=True)
log_file_path = os.path.join(log_dir, log_file)
logging.basicConfig(
    filename=log_file_path,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


