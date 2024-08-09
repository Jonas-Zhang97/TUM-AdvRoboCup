#!/usr/bin/env python3

import rospy
import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import spacy
import os
import time
import rospkg

# Load NLP model
nlp = spacy.load("en_core_web_sm")

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
    if not tasks or not locations:
        return []
    
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
    if tasks and tasks[-1][0] == 'move' and current_location != locations[-1][1]:
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
def visualize_task_graph(graph, filename='task_graph.png'):
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots(figsize=(10, 7))
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=10, font_weight='bold', ax=ax)
    edge_labels = {(edge[0], edge[1]): f'{edge[0]}->{edge[1]}' for edge in graph.edges}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red', ax=ax)
    plt.title('Task Dependency Graph')

    canvas = FigureCanvas(fig)
    canvas.print_figure(filename)
    print(f"Task graph saved to {filename}")

# Step 5: Save sub_tasks to a file
def save_sub_tasks(sub_tasks, filename):
    with open(filename, 'w') as file:
        json.dump(sub_tasks, file)
    print(f"Sub tasks saved to {filename}")

def load_sub_tasks(filename):
    if not os.path.exists(filename):
        rospy.logerr(f"File {filename} does not exist.")
        return []
    rospy.loginfo(f"Loading sub tasks from {filename}")
    with open(filename, 'r') as file:
        sub_tasks = json.load(file)
    return sub_tasks

def save_actions_and_adverbials(sub_tasks, filename):
    actions_and_adverbials = []

    for task in sub_tasks:
        action, *params = task
        if action == 'move':
            adverbial = params[1]
        elif action in ('grab', 'release'):
            adverbial = params[0]
        else:
            adverbial = 'None'
        action_adverbial_pair = [action, adverbial]
        actions_and_adverbials.append(action_adverbial_pair)
        
    rospy.set_param('/tasks', actions_and_adverbials)
    test_tasks = rospy.get_param('/tasks')
    rospy.loginfo(f"Saving actions and adverbials to {filename}")
    with open(filename, 'w') as file:
        json.dump(actions_and_adverbials, file, indent=4)
    rospy.loginfo(f"Actions and adverbials saved to {filename}")

# Main function to execute the task planning and visualization
def main():
    rospy.init_node('task_planner_node', anonymous=True)
    rospack = rospkg.RosPack()
    pkg_path = rospack.get_path('task_planner')

    instruction = rospy.get_param('~instruction', "grab a bottle at storage and move to me and release the bottle")
    is_first_time = rospy.get_param('~is_first_time', True)
    sub_tasks_filepath = rospy.get_param('~sub_tasks_filepath', os.path.join(pkg_path, 'scripts/sub_tasks.json'))
    actions_and_adverbials_filepath = rospy.get_param('~actions_and_adverbials_filepath', os.path.join(pkg_path, 'scripts/actions_and_adverbials.json'))

    tasks, locations, objects = parse_instruction(instruction)
    sub_tasks = decompose_tasks(tasks, locations, objects)

    if is_first_time:
        initial_tasks = [('look_for',), ('Listen',), ('AudioOutput',)]
        sub_tasks = initial_tasks + sub_tasks

    task_graph = build_task_graph(sub_tasks)
    save_sub_tasks(sub_tasks, sub_tasks_filepath)
    # uncomment for visualization of task graph
    # visualize_task_graph(task_graph, filename=os.path.join(pkg_path, 'scripts/task_graph.png'))

    rospy.loginfo("Task planning completed, proceeding to load sub tasks.")
    
    # Wait a moment to ensure the file system is updated
    time.sleep(1)

    # Load sub tasks and save actions and adverbials
    sub_tasks = load_sub_tasks(sub_tasks_filepath)
    if sub_tasks:
        save_actions_and_adverbials(sub_tasks, actions_and_adverbials_filepath)
    
    rospy.loginfo("All tasks completed, shutting down node.")
    rospy.signal_shutdown("All tasks completed")

if __name__ == "__main__":
    main()
