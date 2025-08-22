import hashlib, yaml

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def choose_version(cfg: dict, user_key: str = "anon", override: str = None) -> str:
    if override: return override
    default = cfg.get("default_version","v1")
    canary = cfg.get("canary_version","v2")
    ratio = float(cfg.get("canary_ratio",0.05))
    h = hashlib.sha256(user_key.encode("utf-8")).hexdigest()
    bucket = int(h[:8],16) / 16**8
    return canary if bucket < ratio else default
