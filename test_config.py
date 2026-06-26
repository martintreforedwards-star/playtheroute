from builder.config import load_config

cfg = load_config("scotrail")

print(cfg)
print(cfg["name"])