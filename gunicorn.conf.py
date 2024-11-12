# Number of worker processes
workers = 4

# Number of threads per worker
threads = 2

# The socket to bind
bind = '0.0.0.0:5000'

# Timeout for worker processes
timeout = 120

# Maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'smartarts'

# SSL (uncomment and modify if using HTTPS)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# Worker class
worker_class = 'sync'  # You can use 'gevent' or 'eventlet' for async workers

# Clean up worker processes when receiving TERM signal
graceful_timeout = 30 