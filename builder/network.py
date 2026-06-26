from dataclasses import dataclass, field


@dataclass
class Station:
    """Represents a single railway station."""

    crs: str
    name: str

    latitude: float | None = None
    longitude: float | None = None

    routes: list[str] = field(default_factory=list)
    neighbours: list[str] = field(default_factory=list)

    route_count: int = 0
    service_count: int = 0

    avg_time_to_origin: int | None = None

    is_interchange: bool = False
    is_terminus: bool = False

    attributes: dict = field(default_factory=dict)


@dataclass
class Route:
    """Represents a railway route."""

    name: str
    stations: list[str]

    direction: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class Network:
    """Represents an entire train operator's network."""

    name: str

    stations: dict[str, Station] = field(default_factory=dict)
    routes: list[Route] = field(default_factory=list)

    graph: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)