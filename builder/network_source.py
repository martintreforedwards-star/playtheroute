from builder.config import load_config
from builder.knowledgebase_client import load_knowledgebase
from builder.normalise_network import normalise_network


def load_network(network):

    config = load_config(network)

    
    stations = load_knowledgebase(config["knowledgebase"])

    return normalise_network(stations, config)