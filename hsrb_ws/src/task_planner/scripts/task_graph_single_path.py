import networkx as nx
import matplotlib.pyplot as plt
import spacy

# Load NLP model (example using spaCy)
nlp = spacy.load("en_core_web_sm")

# Step 1: NLP Module - Parse the natural language instruction
def parse_instruction(instruction):
    doc = nlp(instruction)
    tasks = []
    locations = []
    objects = []
    
    for token in doc:
        print(f"Token: {token.text}, POS: {token.pos_}, DEP: {token.dep_}")  # Debugging output
        if token.pos_ == "VERB":
            tasks.append(token.lemma_)
        elif token.pos_ == "NOUN":
            if token.dep_ == "pobj" or token.dep_ == "dobj":
                objects.append(token.text)
            else:
                locations.append(token.text)
    
    print(f"Parsed tasks: {tasks}")
    print(f"Parsed locations: {locations}")
    print(f"Parsed objects: {objects}")
    
    return tasks, locations, objects

# Step 2: Task Decomposition and Mapping
def decompose_tasks(tasks, locations, objects):
    sub_tasks = []
    for task in tasks:
        if task == 'move' and len(locations) >= 2:
            sub_tasks.append(('move', locations[0], locations[1]))
        elif task == 'locate' and objects:
            sub_tasks.append(('locate', objects[0]))
        elif task == 'grab' and objects:
            sub_tasks.append(('grab', objects[0]))
        elif task == 'release' and len(locations) >= 2 and objects:
            sub_tasks.append(('release', objects[0], locations[1]))
    
    print(f"Decomposed sub_tasks: {sub_tasks}")  # Debugging output
    return sub_tasks

# Step 3: Build Task Graph
def build_task_graph(sub_tasks):
    G = nx.DiGraph()
    for sub_task in sub_tasks:
        print(f"Processing sub_task: {sub_task}")  # Debugging output
        action, *params = sub_task
        if action == 'move':
            G.add_edge('start', f'move_to_{params[0]}')
            G.add_edge(f'move_to_{params[0]}', f'move_to_{params[1]}')
        elif action == 'locate':
            G.add_edge(f'move_to_{params[0]}', f'locate_{params[0]}')
        elif action == 'grab':
            G.add_edge(f'locate_{params[0]}', f'grab_{params[0]}')
        elif action == 'release':
            G.add_edge(f'grab_{params[0]}', f'move_to_{params[1]}')
            G.add_edge(f'move_to_{params[1]}', f'release_{params[0]}')
    
    print(f"Nodes in graph: {G.nodes}")
    print(f"Edges in graph: {G.edges}")
    return G

# Step 4: Plan Task Sequence using topological sort
def plan_tasks(graph):
    task_sequence = list(nx.topological_sort(graph))
    print(f"Planned task sequence: {task_sequence}")  # Debugging output
    return task_sequence

# Step 5: State Machine to execute task sequence
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

# Step 6: Visualize the task graph
def visualize_task_graph(graph):
    pos = nx.spring_layout(graph)  # Position nodes using Fruchterman-Reingold force-directed algorithm
    plt.figure(figsize=(10, 7))
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=10, font_weight='bold')
    edge_labels = {(edge[0], edge[1]): f'{edge[0]}->{edge[1]}' for edge in graph.edges}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    plt.title('Task Dependency Graph')
    plt.show()

# Example usage
instruction = "move to A and grab the bottle then move to B and release the bottle"
tasks, locations, objects = parse_instruction(instruction)
sub_tasks = decompose_tasks(tasks, locations, objects)
task_graph = build_task_graph(sub_tasks)
task_sequence = plan_tasks(task_graph)
state_machine = StateMachine(task_sequence)
state_machine.execute_tasks()
visualize_task_graph(task_graph)
