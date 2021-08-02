from config import WorkerConfiguration
import utils.logger as logger
from LocalWorker import LocalWorker
from apscheduler.schedulers.background import BackgroundScheduler

log = logger.setup_logger("root")
configFile = WorkerConfiguration()
log.debug("initalized logger")
localWorker = LocalWorker(configFile,log)
workers = {}
scheduler = BackgroundScheduler()
