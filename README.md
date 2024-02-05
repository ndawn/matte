# [Matte](https://t.me/matterss_bot) - A simple RSS bot for Telegram:

## Deployment
1. Create a config TOML file (sample config can be found at `config.sample.toml`) and populate it with your data.
2. Generate `.env` file for Docker Compose stack:
   ```bash
   $ python generate.py <PATH_TO_CONFIG_TOML>
   ```
3. Deploy with Docker Compose:
   ```bash
   $ sudo docker compose --env-file .env up --build -d
   ```
