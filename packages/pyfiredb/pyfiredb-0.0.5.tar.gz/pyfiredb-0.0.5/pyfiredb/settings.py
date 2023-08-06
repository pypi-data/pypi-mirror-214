from dataclasses import dataclass
from environs import Env
from pathlib import Path
import json

if not (Path.cwd()/".env").exists():
    (Path.cwd()/".env").touch()


env = Env()
env.read_env(Path.cwd()/".env")


@dataclass
class Settings:
    try:
        setup = json.loads(env("DB_SETUP"))
    except Exception:
        with open(Path.cwd()/".env", "a") as env:
            db_setup = input("DB_SETUP")
            env.writelines("DB_SETUP="+db_setup+"\n")


@dataclass
class Credentials:
    try:
        user = env("DB_USER")
    except Exception:
        with open(Path.cwd()/".env", "a") as env:
            user = input("DB_USER")
            env.writelines("DB_USER="+user+"\n")

    try:
        password = env("DB_PASS")
    except Exception:
        with open(Path.cwd()/".env", "a") as env:
            user = input("DB_PASS")
            env.writelines("DB_PASS="+user+"\n")
