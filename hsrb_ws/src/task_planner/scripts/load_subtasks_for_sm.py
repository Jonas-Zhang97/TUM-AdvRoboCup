import json

# Function to load sub-tasks from a JSON file
def load_sub_tasks(filename="sub_tasks.json"):
    with open(filename, 'r') as file:
        sub_tasks = json.load(file)
    return sub_tasks

# Function to print sub-tasks in a readable format
def print_sub_tasks(sub_tasks):
    for i, task in enumerate(sub_tasks):
        action, *params = task
        if action == 'move':
            print(f"Task {i+1}: Move from {params[0]} to {params[1]}")
        elif action == 'grab':
            print(f"Task {i+1}: Grab {params[0]} at {params[1]}")
        elif action == 'release':
            print(f"Task {i+1}: Release {params[0]} at {params[1]}")
        elif action == 'look_for':
            print(f"Task {i+1}: Look for something")
        elif action == 'Listen':
            print(f"Task {i+1}: Listen for instructions")
        elif action == 'AudioOutput':
            print(f"Task {i+1}: Output audio")

# Function to save action and adverbial phrases to a new JSON file
def save_actions_and_adverbials(sub_tasks, filename="actions_and_adverbials.json"):
    actions_and_adverbials = []

    for task in sub_tasks:
        action, *params = task
        if action == 'move':
            adverbial = params[1]
        elif action in ('grab', 'release'):
            adverbial = params[0]
        else:
            adverbial = None
        action_adverbial_pair = [action, adverbial]
        actions_and_adverbials.append(action_adverbial_pair)

    with open(filename, 'w') as file:
        json.dump(actions_and_adverbials, file, indent=4)
    print(f"Actions and adverbials saved to {filename}")

# Main function to load, print and save tasks
def main():
    sub_tasks = load_sub_tasks()
    print_sub_tasks(sub_tasks)
    save_actions_and_adverbials(sub_tasks)

if __name__ == "__main__":
    main()