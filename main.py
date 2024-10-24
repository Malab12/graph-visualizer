import sys
import networkx as nx
import matplotlib
import random
matplotlib.use('QtAgg')

from PyQt6 import QtWidgets, QtCore
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

        # Create a slider to select the edge probability
        self.edge_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.edge_slider.setRange(0, 100)  # Probability from 0 to 100 percent
        self.edge_slider.setValue(50)  # Default is 50%
        self.edge_slider.valueChanged.connect(self.update_graph)  # Connect to update_graph when slider changes

        # Label to show edge probability
        self.slider_label = QtWidgets.QLabel(f"Edge Probability: {self.edge_slider.value()}%", self)

        # Create a layout to hold the spin box, slider, and canvas
        self.layout_widget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self.layout_widget)
        self.layout.addWidget(self.spin_box)
        self.layout.addWidget(self.slider_label)
        self.layout.addWidget(self.edge_slider)
        self.layout.addWidget(self.canvas)

        self.setCentralWidget(self.layout_widget)

        # Initialize the graph and node positions
        self.graph = nx.Graph()
        self.positions = {}  # To store positions of nodes

        # Initial graph with 5 nodes and edge probability of 50%
        self.add_nodes(5)
        self.update_plot()

        self.show()

    def add_nodes(self, num_new_nodes):
        """Add new nodes to the graph and connect them based on edge probability."""
        current_node_count = len(self.graph.nodes)
        new_nodes = range(current_node_count, current_node_count + num_new_nodes)

        # Add new nodes to the graph
        self.graph.add_nodes_from(new_nodes)

        # Get edge probability from the slider
        edge_prob = self.edge_slider.value() / 100.0

        # Connect new nodes to existing nodes with the given probability
        for new_node in new_nodes:
            for existing_node in self.graph.nodes:
                if new_node != existing_node and random.random() < edge_prob:
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
        if len(self.graph.nodes) == 0:
            return  # No nodes to position
        
        # Maintain positions for existing nodes
        new_positions = nx.spring_layout(self.graph)

        # Update the position dictionary with new positions
        self.positions.update(new_positions)

    def update_graph(self):
        """Update the graph when the number of nodes or edge probability changes."""
        # Update slider label
        self.slider_label.setText(f"Edge Probability: {self.edge_slider.value()}%")

        new_node_count = self.spin_box.value()
        current_node_count = len(self.graph.nodes)

        if new_node_count > current_node_count:
            # Add new nodes
            self.add_nodes(new_node_count - current_node_count)
        elif new_node_count < current_node_count:
            # Remove nodes
            self.remove_nodes(current_node_count - new_node_count)
        else:
            # Update edges only if node count is the same
            self.update_edges()

        # Redraw the graph after updating nodes/edges
        self.update_plot()

    def update_edges(self):
        """Update edges in the graph based on the edge probability."""
        self.graph.clear_edges()  # Remove all current edges

        edge_prob = self.edge_slider.value() / 100.0

        # Reconnect nodes based on the current edge probability
        for node1 in self.graph.nodes:
            for node2 in self.graph.nodes:
                if node1 != node2 and random.random() < edge_prob:
                    self.graph.add_edge(node1, node2)

    def update_plot(self):
        """Redraw the graph on the canvas."""
        self.canvas.axes.cla()  # Clear the canvas.
        nx.draw(self.graph, pos=self.positions, ax=self.canvas.axes, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500)

        # Trigger the canvas to update and redraw.
        self.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()
