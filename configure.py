import os
import tomllib
from argparse import ArgumentParser
from urllib.parse import urlparse


parser = ArgumentParser()
parser.add_argument("config_path")


def main() -> None:
    args = parser.parse_args()

    with open(args.config_path, "rb") as config_file:
        config = tomllib.load(config_file)

    db_url = urlparse(config["db_url"])

    environment = {
        "MIGRATIONS_URL": (
            f"postgresql://{db_url.username}:{db_url.password}@{db_url.hostname}:{db_url.port}{db_url.path}"
        ),
        "POSTGRES_USER": db_url.username,
        "POSTGRES_PASSWORD": db_url.password,
        "POSTGRES_DB": db_url.path.lstrip("/"),
        "CONFIG_PATH": args.config_path,
        "PWD": os.path.abspath(os.curdir),
    }

    environment_string = "\n".join(f"{name}={value}" for name, value in environment.items())

    with open(f".env", "w") as env_file:
        env_file.write(environment_string)


if __name__ == "__main__":
    main()
