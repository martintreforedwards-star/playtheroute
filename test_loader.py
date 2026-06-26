from builder.config import load_config
from builder.loaders import load_network

cfg = load_config("scotrail")
network = load_network(cfg)

print(network.name)
print(len(network.stations))