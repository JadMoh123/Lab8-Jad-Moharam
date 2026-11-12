# Lab 8 – Docker, containers and images

**Jad Moharam – ID 202400899 – AUB username jmm47**
Software Tools Lab

| Folder | Image | Port | What it runs |
|--------|-------|------|--------------|
| `hello flask/` | `flask_docker:latest` | 5000 | The "Hello, World!" Flask app from the handout |
| `lab5 api/` | `jmm47/lab8-jad_moharam:0.0.1.RELEASE` | 5000 | Lab 5 – Postman and APIs (users CRUD API) |
| `get users api/` | `jmm47/lab8-jad_moharam:0.0.2.RELEASE` | 3000 | `GET /get_users` – names of all users in the database |

Docker image names must be lowercase, so `lab8-Jad_Moharam` is written `lab8-jad_moharam`, and the tag `0.0.1:RELEASE` is written `0.0.1.RELEASE` (a tag can't contain `:`), the same as in the handout's screenshot.

## Build and run your first container

```bash
cd "hello flask"
pip freeze > requirements.txt      # or use the requirements.txt in the folder
docker image build -t flask_docker .
docker run -p 5000:5000 -d --name flask_docker_app flask_docker
```

Open http://localhost:5000 → `Hello, World!`

## Activity 1

| Command | What it does |
|---------|--------------|
| `docker ps -a` | Lists **all** containers on the machine, running and stopped, with their ID, image, command, creation time, status, port mappings and name (without `-a` only running containers are shown). |
| `docker stop <container>` | Stops a running container: Docker sends it SIGTERM and, if it hasn't exited after 10 seconds, SIGKILL. The container still exists (status `Exited`) and can be started again with `docker start`. |
| `docker logs <container>` | Prints what the container wrote to stdout/stderr – here the Flask startup messages and one line per HTTP request it served. |

`docker stop` and `docker logs` take a container name or ID (not an image name), which is why the container is started with `--name flask_docker_app`.

```bash
docker ps -a
docker logs flask_docker_app
docker stop flask_docker_app
```

## Activity 2

### Image 1 – Lab 5 API on port 5000 (`0.0.1.RELEASE`)

```bash
docker image build -t jmm47/lab8-jad_moharam:0.0.1.RELEASE "lab5 api"
docker run -p 5000:5000 -d --name lab5_api jmm47/lab8-jad_moharam:0.0.1.RELEASE
```

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users` | GET | All users |
| `/api/users/<user_id>` | GET | One user |
| `/api/users/add` | POST | Add a user (JSON body) |
| `/api/users/update` | PUT | Update a user (JSON body with `user_id`) |
| `/api/users/delete/<user_id>` | DELETE | Delete a user |

The Postman collection and environment from Lab 5 are in `lab5 api/` and work against the container unchanged (`base_url = http://localhost:5000`).

### Image 2 – `get_users` API on port 3000 (`0.0.2.RELEASE`)

```bash
docker image build -t jmm47/lab8-jad_moharam:0.0.2.RELEASE "get users api"
docker run -p 3000:3000 -d --name get_users_api jmm47/lab8-jad_moharam:0.0.2.RELEASE
```

`GET http://localhost:3000/get_users` →

```json
["John Doe", "Jane Smith", "Ali Hassan"]
```

The database is created inside the container the first time it starts, with three sample users.

## Changes from the handout

- `python:3.12-alpine` instead of `python:3.8-alpine`: Python 3.8 is end-of-life and Flask 3.1 needs Python 3.9 or newer.
- Each app calls `app.run(host="0.0.0.0", ...)`. Flask's default `127.0.0.1` only accepts connections from inside the container, so `-p 5000:5000` would not reach it.
- A `.dockerignore` in each folder keeps `database.db`, `__pycache__` and virtual environments out of the image.
