import sys
import networkx as nx
import matplotlib
matplotlib.use('QtAgg')

from PyQt6 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        # Create a spin box to select the number of nodes
        self.spin_box = QtWidgets.QSpinBox(self)
        self.spin_box.setRange(3, 50)  # Min 3 nodes, Max 50 nodes
        self.spin_box.setValue(5)  # Default value is 5 nodes
        self.spin_box.valueChanged.connect(self.update_graph)  # Connect to update_graph when value changes

        # Create a layout to hold the spin box and the canvas
        self.layout_widget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self.layout_widget)
        self.layout.addWidget(self.spin_box)
        self.layout.addWidget(self.canvas)

        self.setCentralWidget(self.layout_widget)

        # Initialize the graph and node positions
        self.graph = nx.Graph()
        self.positions = {}  # To store positions of nodes

        # Initial graph with 5 nodes
        self.add_nodes(5)
        self.update_plot()

        self.show()

    def add_nodes(self, num_new_nodes):
        """Add new nodes to the graph and connect each to every other node (complete graph)."""
        current_node_count = len(self.graph.nodes)
        new_nodes = range(current_node_count, current_node_count + num_new_nodes)

        # Add new nodes to the graph
        self.graph.add_nodes_from(new_nodes)

        # Connect each new node to all existing nodes (complete graph)
        for new_node in new_nodes:
            for existing_node in self.graph.nodes:
                if new_node != existing_node:
                    self.graph.add_edge(new_node, existing_node)

        # Calculate positions for new nodes while keeping old ones unchanged
        self.update_positions()

    def remove_nodes(self, num_nodes_to_remove):
        """Remove nodes from the graph, starting from the highest node number."""
        current_node_count = len(self.graph.nodes)
        if num_nodes_to_remove > current_node_count:
            num_nodes_to_remove = current_node_count

        nodes_to_remove = range(current_node_count - num_nodes_to_remove, current_node_count)
        self.graph.remove_nodes_from(nodes_to_remove)

        # Remove the positions of the removed nodes
        for node in nodes_to_remove:
            if node in self.positions:
                del self.positions[node]

    def update_positions(self):
        """Update positions of new nodes while keeping old positions."""
        # Use spring_layout for existing nodes and assign random positions to new ones
        if len(self.graph.nodes) == 0:
            return  # No nodes to position
        
        new_positions = nx.spring_layout(self.graph)

        # Update the position dictionary with new positions
        self.positions.update(new_positions)

    def update_graph(self):
        """Update the graph when the number of nodes changes."""
        new_node_count = self.spin_box.value()
        current_node_count = len(self.graph.nodes)

        if new_node_count > current_node_count:
            # Add new nodes
            self.add_nodes(new_node_count - current_node_count)
        elif new_node_count < current_node_count:
            # Remove nodes
            self.remove_nodes(current_node_count - new_node_count)

        # Redraw the graph after updating nodes
        self.update_plot()

    def update_plot(self):
        """Redraw the graph on the canvas."""
        self.canvas.axes.cla()  # Clear the canvas.
        nx.draw(self.graph, pos=self.positions, ax=self.canvas.axes, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500)

        # Trigger the canvas to update and redraw.
        self.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()
