import matplotlib.pyplot as plt
import networkx as nx

from pyzefir.model.bus import Bus
from pyzefir.model.enum import EnergyType
from pyzefir.model.generator import Generator, GeneratorConfig
from pyzefir.model.storage import Storage, StorageConfig
from tests.unit.utils import (
    default_generator_config,
    default_line_config,
    default_storage_config,
)

gen_config = GeneratorConfig(**default_generator_config)
gen_A = Generator(id=1, name="PV", config=gen_config)
bus_electric = Bus(id=1, name="bus_electric", energy_type=EnergyType.ELECTRIC_ENERGY)
storage_config = StorageConfig(**default_storage_config)
storage = Storage(id=1, name="Battery", config=storage_config)
link = "link"

graph = nx.Graph()
graph.add_node(bus_electric)
graph.add_node(gen_A)
graph.add_edge(bus_electric, gen_A)

nx.draw(graph)
plt.show()
