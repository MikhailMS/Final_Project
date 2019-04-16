## Usage
1. `docker-compose up -d` to start development cluster (RabbitMQ cluster of 3 + HAproxy node)
2. Now you can access Web GUI from your browser on **localhost:15672**, credentials:
  1. User: **segal**
  2. Pass: **segal**
3. To start Celery app, execute command `celery -A tasks worker --loglevel=info --logfile="./celery.log" --pidfile="./celery.pid" --detach --concurrency=2 -E`
