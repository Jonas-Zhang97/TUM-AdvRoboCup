import networkx as nx
import matplotlib.pyplot as plt
import spacy
import json

# Load NLP model (example using spaCy)
nlp = spacy.load("en_core_web_sm")

# Current location, you can set this dynamically in your application
current_location = "my_location"

# Step 1: NLP Module - Parse the natural language instruction
def parse_instruction(instruction):
    instruction = instruction.replace("me", current_location)  # Replace 'me' with the current location
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

    # Remove duplicate locations
    locations = list(dict.fromkeys(locations))
    objects = list(objects) 
    
    print(f"Parsed tasks: {tasks}")
    print(f"Parsed locations: {locations}")
    print(f"Parsed objects: {objects}")
    
    return tasks, locations, objects

# Step 2: Task Decomposition and Mapping
def decompose_tasks(tasks, locations, objects):
    sub_tasks = []
    object_index = 0
    current_location = 'start'

    location_dict = {i: loc for i, loc in enumerate(locations)}

    for i, (task, _) in enumerate(tasks):
        if task == 'move':
            target_location = location_dict.get(i, (None, current_location))[1]
            if current_location != target_location:
                sub_tasks.append(('move', current_location, target_location))
                current_location = target_location
        elif task == 'grab' and object_index < len(objects):
            target_location = location_dict.get(i, (None, current_location))[1]
            if current_location != target_location:
                sub_tasks.append(('move', current_location, target_location))
                current_location = target_location
            sub_tasks.append(('grab', objects[object_index], target_location))
            current_location = target_location
            object_index += 1
        elif task == 'release' and object_index > 0:
            target_location = location_dict.get(i, (None, current_location))[1]
            sub_tasks.append(('release', objects[object_index - 1], target_location))
            current_location = target_location

    # Ensure to handle only the last move without adding release if it doesn't exist
    if tasks[-1][0] == 'move' and current_location != locations[-1][1]:
        sub_tasks.append(('move', current_location, locations[-1][1]))
    
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
        elif action in ('look_for', 'Listen', 'AudioOutput'):
            current_task = action
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

# Main function to execute the task planning and visualization
def main(instruction, is_first_time):
    tasks, locations, objects = parse_instruction(instruction)
    sub_tasks = decompose_tasks(tasks, locations, objects)

    if is_first_time:
        initial_tasks = [('look_for',), ('Listen',), ('AudioOutput',)]
        sub_tasks = initial_tasks + sub_tasks

    task_graph = build_task_graph(sub_tasks)
    visualize_task_graph(task_graph)
    save_sub_tasks(sub_tasks)

# Example usage
if __name__ == "__main__":
    # instruction = "move to A and grab the bottle at A and move to B and move to D and move to C and release the bottle at C"
    # instruction = "grab the bottle at A and move to B and move to D and move to C and release the bottle at C"
    instruction = "grab a bottle at storage and move to me and release the bottle"

    is_first_time = True # False # True  # Set this to False after the first execution
    main(instruction, is_first_time)
