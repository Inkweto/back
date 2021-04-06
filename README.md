# AIIR back
## Development
Create `.env` file from `.env.example`
```bash
cp .env.example .env
```
### VSCode + Docker
1. Start Docker and open project's dir in VSCode
2. Install `ms-vscode-remote.remote-containers` extension
3. `Ctrl+Shift+P` -> Remote-Containers: Reopen in Container

### Docker only
In project's dir run:
```bash
docker-compose up -d
```
Then run the flask app:
```bash
docker-compose exec flask flask run
```

