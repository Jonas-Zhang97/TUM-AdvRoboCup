pip install spacy
python3 -m spacy download en_core_web_sm



export XDG_RUNTIME_DIR=/tmp/runtime-$USER
mkdir -p $XDG_RUNTIME_DIR
chmod 0700 $XDG_RUNTIME_DIR


(scripts/task_3_state_worked.py)这个版本是多次验证过的

roslaunch task_planner task_planner.launch instruction:="grab the bottle at A and move to B and move to D and move to C and release the bottle at C"
roslaunch task_planner task_planner.launch instruction:="grab a bottle at storage and move to me and release the bottle"

sm需要的list ，存在
/workspaces/cup/hsrb_ws/src/task_planner/scripts/actions_and_adverbials.json