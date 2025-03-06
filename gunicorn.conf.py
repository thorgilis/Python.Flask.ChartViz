import multiprocessing

# Gunicorn configuration for production

# Binding
bind = "0.0.0.0:50006"
preload_app = False

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 2

# Timeouts
timeout = 60
keepalive = 5

# Server mechanics
daemon = False
pidfile = "gunicorn.pid"
umask = 0o007
user = None
group = None
tmp_upload_dir = None

# Logging
errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = '%({X-Forwarded-For}i)s %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = None

# Server hooks
def on_starting(server):
    server.log.info("Starting Gunicorn server")

def on_exit(server):
    server.log.info("Stopping Gunicorn server")