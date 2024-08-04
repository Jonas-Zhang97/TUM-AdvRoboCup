import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Define tasks and their dependencies
tasks = [
    ("start", "move_to_A"),
    ("move_to_A", "locate_bottle"),
    ("locate_bottle", "grab_bottle"),
    ("grab_bottle", "move_to_B"),
    ("move_to_B", "release_bottle")
]

# Step 2: Build the task graph
def build_task_graph(tasks):
    G = nx.DiGraph()
    for task in tasks:
        G.add_edge(task[0], task[1])
    return G

# Step 3: Plan task sequence using topological sort
def plan_tasks(graph):
    task_sequence = list(nx.topological_sort(graph))
    return task_sequence

# Step 4: State Machine to execute task sequence
class StateMachine:
    def __init__(self, task_sequence):
        self.task_sequence = task_sequence
        self.current_state = 'INIT'

    def execute_tasks(self):
        for task in self.task_sequence:
            self.current_state = 'EXECUTING'
            self.execute_task(task)
            self.current_state = 'COMPLETED'

    def execute_task(self, task):
        # Implement task execution logic
        print(f"Executing task: {task}")

# Step 5: Visualize the task graph
def visualize_task_graph(graph):
    pos = nx.spring_layout(graph)  # Position nodes using Fruchterman-Reingold force-directed algorithm
    plt.figure(figsize=(10, 7))
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=10, font_weight='bold')
    edge_labels = {edge: f'{edge[0]}->{edge[1]}' for edge in graph.edges}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    plt.title('Task Dependency Graph')
    plt.show()

# Example usage
task_graph = build_task_graph(tasks)
task_sequence = plan_tasks(task_graph)
state_machine = StateMachine(task_sequence)
state_machine.execute_tasks()
visualize_task_graph(task_graph)
