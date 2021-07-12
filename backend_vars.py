from config import WorkerConfiguration
import utils.logger as logger
from apscheduler.schedulers.background import BackgroundScheduler

log = logger.setup_logger("root")
configFile = WorkerConfiguration()
log.debug("initalized logger")

workers = {}
scheduler = BackgroundScheduler()

WORKER_URL = "http://0.0.0.0:5201"