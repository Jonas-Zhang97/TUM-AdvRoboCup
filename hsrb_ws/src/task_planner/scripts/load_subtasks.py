import json

# 加载子任务
def load_sub_tasks(filename="sub_tasks.json"):
    with open(filename, 'r') as file:
        sub_tasks = json.load(file)
    return sub_tasks

# 执行子任务
def execute_sub_tasks(sub_tasks):
    for sub_task in sub_tasks:
        action = sub_task[0]
        params = sub_task[1:]
        
        if action == 'move':
            execute_move(*params)
        elif action == 'grab':
            execute_grab(*params)
        elif action == 'release':
            execute_release(*params)

# 示例执行函数
def execute_move(start, end):
    print(f"Moving from {start} to {end}")

def execute_grab(object, location):
    print(f"Grabbing {object} at {location}")

def execute_release(object, location):
    print(f"Releasing {object} at {location}")

# 主程序
sub_tasks = load_sub_tasks()
execute_sub_tasks(sub_tasks)
