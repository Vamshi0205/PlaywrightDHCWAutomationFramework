from pydantic import BaseModel
from pathlib import Path
import os, yaml

class AppConfig(BaseModel):
    base_url: str
    username: str | None = None
    password: str | None = None

def config_dir() -> Path:
    # Allow override; default to Tests/config
    env = os.getenv("FWK_CONFIG_DIR", "Tests/config")
    p = Path(env)
    if not p.exists():
        raise FileNotFoundError(f"Config directory not found: {p.resolve()}")
    return p

def load_config(env_name: str) -> AppConfig:
    cfg_path = config_dir() / f"{env_name}.yaml"
    data = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    return AppConfig(**data)
