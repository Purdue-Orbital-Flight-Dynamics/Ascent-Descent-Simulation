from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
import ascent_simulation
import descent_simulation

graphviz = GraphvizOutput()
graphviz.output_file = 'ascent_map.png'

with PyCallGraph(output=graphviz):
    ascent_simulation.main()
    
    
graphviz = GraphvizOutput()
graphviz.output_file = 'descent_map.png'

with PyCallGraph(output=graphviz):
    descent_simulation.main()