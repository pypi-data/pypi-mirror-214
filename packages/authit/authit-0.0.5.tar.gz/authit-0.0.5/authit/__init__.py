from authit.gateways.connect import ConnectionGateway


def connect(storageEngine: str):
    return ConnectionGateway(storageEngine=storageEngine)