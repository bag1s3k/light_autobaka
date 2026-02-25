import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

LOGIN_URL = config["server"]["base_url"] + config["server"]["login_endpoint"]
MARKS_URL = config["server"]["base_url"] + config["server"]["marks_endpoint"]