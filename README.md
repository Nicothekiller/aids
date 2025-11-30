# SIDA: simple intelligent data analyzer (or "AIDS: analizador inteligente de datos simples" in Spanish)

This repo contains the backend and the front-end for the project. What is it? SIDA (or AIDS in Spanish) is a
website that lets you analyze numeric datasets in a simple way.

## Features

- Front-end written in svelte
- Backend in python, using libraries like gRPC for an efficient API, pandas for efficient numeric analysis, seaborn for plots, etc.
- Nice way to visualize the general statistics of the data
- Beautiful charts using seaborn

## How to build

Using Linux is heavily encouraged, but it should be fine on any platform.

Beyond that, there are 3 hard dependencies:
- [uv](https://github.com/astral-sh/uv) for the backend
- [npm](https://www.npmjs.com/) and npx for some scripts in the front-end
- [deno](https://deno.com/) for the front-end (optional for deployment, but important for development)
- Docker with [Docker Compose](https://docs.docker.com/compose/) for deployment and ease of use

Afterwards, change directories to `./aids-frontend/src/lib/protos` and run the command:
```bash
./generate-protos.sh
```

This is important for generating the gRPC related files necessary for the front-end.

For windows users, either use [wsl](https://learn.microsoft.com/en-us/windows/wsl/install) or open the `./generate-protos.sh`
file and run the command manually inside of the directory.

Afterwards run:
```bash
docker compose build && docker compose up -d
```

Once finished, you can visit the website on http://localhost or on your ip address on port 80.
