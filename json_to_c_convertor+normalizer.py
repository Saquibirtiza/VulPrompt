import os, sys
import json

source_dir = "./reveal_source/"
 
# Opening JSON file
f = open('function.json')
data = json.load(f)
counter = 0

# Iterating through the json list
for i in data:
  code = i["func"]
  code = os.linesep.join([s for s in code.splitlines() if s])
  label = i["target"]
  filename = i["project"] + "_" + i["commit_id"]

  if label == 1:
    inp = source_dir + "Vul/" + filename + ".c"
    if not os.path.exists(source_dir + "Vul/"):
      os.makedirs(source_dir + "Vul/")  
    with open(inp, 'w') as f:
      f.writelines(code)
  else:
    inp = source_dir + "No-Vul/" + filename + ".c"
    if not os.path.exists(source_dir + "No-Vul/"):
      os.makedirs(source_dir + "No-Vul/")  
    with open(inp, 'w') as f:
      f.writelines(code)

os.environ['normalize_dir'] = str(source_dir)
os.system('python ./normalization.py -i $normalize_dir')