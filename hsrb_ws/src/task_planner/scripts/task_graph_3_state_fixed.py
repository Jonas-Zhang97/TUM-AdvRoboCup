import networkx as nx
import matplotlib.pyplot as plt
import spacy
import json

# Load NLP model (example using spaCy)
nlp = spacy.load("en_core_web_sm")

# Step 1: NLP Module - Parse the natural language instruction
def parse_instruction(instruction):
    doc = nlp(instruction)
    tasks = []
    locations = []
    objects = []
    current_task = None

    for token in doc:
        print(f"Token: {token.text}, POS: {token.pos_}, DEP: {token.dep_}")  # Debugging output
        if token.pos_ == "VERB":
            current_task = token.lemma_
            tasks.append((current_task, None))
        elif token.pos_ == "NOUN":
            if token.dep_ in ("pobj", "dobj"):
                if token.head.dep_ == "prep" and token.head.head.pos_ == "VERB":
                    locations.append((token.head.head.lemma_, token.text))
                else:
                    objects.append(token.text)
        elif token.dep_ == "prep" and token.head.pos_ == "VERB":
            for child in token.children:
                if child.pos_ == "NOUN":
                    locations.append((token.head.lemma_, child.text))

    print(f"Parsed tasks: {tasks}")
    print(f"Parsed locations: {locations}")
    print(f"Parsed objects: {objects}")
    
    return tasks, locations, objects

# Step 2: Task Decomposition and Mapping
def decompose_tasks(tasks, locations, objects):
    sub_tasks = []
    object_index = 0
    last_location = 'start'
    current_location = 'start'

    location_dict = {task: loc for task, loc in locations}

    for i, (task, _) in enumerate(tasks):
        if task == 'move':
            target_location = locations[i][1]
            if current_location != target_location:
                sub_tasks.append(('move', current_location, target_location))
                current_location = target_location
        elif task == 'grab' and object_index < len(objects):
            target_location = location_dict.get(task, current_location)
            if current_location != target_location:
                sub_tasks.append(('move', current_location, target_location))
                current_location = target_location
            sub_tasks.append(('grab', objects[object_index], target_location))
            current_location = target_location
            object_index += 1
        elif task == 'release' and object_index > 0:
            target_location = location_dict.get(task, current_location)
            if current_location != target_location:
                sub_tasks.append(('move', current_location, target_location))
                current_location = target_location
            sub_tasks.append(('release', objects[object_index - 1], target_location))
            current_location = target_location

    print(f"Decomposed sub_tasks: {sub_tasks}")  # Debugging output
    return sub_tasks

# Step 3: Build Task Graph
def build_task_graph(sub_tasks):
    G = nx.DiGraph()
    previous_task = 'start'

    for sub_task in sub_tasks:
        print(f"Processing sub_task: {sub_task}")  # Debugging output
        action, *params = sub_task

        if action == 'move':
            current_task = f'move_to_{params[1]}'
            G.add_edge(previous_task, current_task)
            previous_task = current_task
        elif action == 'grab':
            current_task = f'grab_{params[0]}_at_{params[1]}'
            G.add_edge(previous_task, current_task)
            previous_task = current_task
        elif action == 'release':
            current_task = f'release_{params[0]}_at_{params[1]}'
            G.add_edge(previous_task, current_task)
            previous_task = current_task

    print(f"Nodes in graph: {G.nodes}")
    print(f"Edges in graph: {G.edges}")
    return G

# Step 4: Visualize the task graph
def visualize_task_graph(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 7))
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=10, font_weight='bold')
    edge_labels = {(edge[0], edge[1]): f'{edge[0]}->{edge[1]}' for edge in graph.edges}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    plt.title('Task Dependency Graph')
    plt.show()

# Step 5: Save sub_tasks to a file
def save_sub_tasks(sub_tasks, filename="sub_tasks.json"):
    with open(filename, 'w') as file:
        json.dump(sub_tasks, file)
    print(f"Sub tasks saved to {filename}")

# Example usag
# instruction = "grab the bottle at A and move to B and move to C and release the bottle at C"
# instruction = "move to A and grab the bottle then move to B and release the bottle"
instruction = "grab the bottle at A and move to B and move to D then move to C and release the bottle"

tasks, locations, objects = parse_instruction(instruction)
sub_tasks = decompose_tasks(tasks, locations, objects)
task_graph = build_task_graph(sub_tasks)
visualize_task_graph(task_graph)
save_sub_tasks(sub_tasks)
