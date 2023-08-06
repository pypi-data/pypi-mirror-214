🔖 [Table of Contents](../../README.md) / [Concepts](../README.md) / [Tasks](README.md)

# Docker-Compose task

Docker Compose is a convenient way to run containers on your local computer.

Suppose you have the following Docker Compose file:

```yaml
# docker-compose.yml file
version: '3'

services:
  # The load balancer
  nginx:
    image: nginx:1.16.0-alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "${HOST_PORT:-8080}:80"
```

You can define a task to run your Docker Compose file (i.e., `docker compose up`) like this:

```python
from zrb import DockerComposeTask, HTTPChecker, Env, runner

run_container = DockerComposeTask(
    name='run-container',
    compose_cmd='up',
    compose_file='docker-compose.yml',
    envs=[
        Env(name='HOST_PORT', default='3000')
    ],
    checkers=[
        HTTPChecker(
            name='check-readiness', port='{{env.HOST_PORT}}'
        )
    ]
)
runner.register(run_container)
```

You can then run the task by invoking:

```bash
zrb run-container
```

🔖 [Table of Contents](../../README.md) / [Concepts](../README.md) / [Tasks](README.md)