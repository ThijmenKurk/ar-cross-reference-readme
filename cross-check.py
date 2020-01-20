import os
import json
from termcolor import colored
import pandas as pd
from tabulate import tabulate

ANDROID_RUNNER_PATH = os.path.expanduser("~/school/isp/project/android-runner")
BLACKLIST = ["nexus6p", "AndroidPlugin", "android", "trepn", "batterystats"]


def fname(path): return os.path.basename(path)
def traverse_dir(dir, file_filter, files=[]):
    for entry in os.listdir(dir):
        path = os.path.join(dir, entry)
        
        if os.path.isdir(path):
            traverse_dir(path, file_filter, files)
        elif file_filter(path):
            files.append(path)
    return files 

def get_documented_properties():
    properties = set()
    with open('documented-by-readme', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0: continue
            properties.add(line)
    return properties
   
def traverse_json(obj, path="", output=[]):
    if isinstance(obj, dict):
        for prop in obj:
            prop_path = "%s.%s"%(path, prop)
            prop_value = obj[prop]
            
            if prop not in BLACKLIST:
                output.append((prop in properties, prop_path, file[len(ANDROID_RUNNER_PATH):]))
           
            traverse_json(prop_value, prop_path, output)
    elif isinstance(obj, list):
        for item in obj:
            traverse_json(item, path + "[]", output)

    return output
            

files = traverse_dir(
    os.path.join(ANDROID_RUNNER_PATH, "examples"), 
    lambda path: path.lower().endswith('.json') and "config" in fname(path.lower())
)
properties = get_documented_properties()

output = []
for file in files:
   with open(file, 'r') as f:
        obj = json.load(f)
        output += traverse_json(obj)

df = pd.DataFrame(output)
df.columns = ["documented", "property", "file"]

df = df.groupby(['documented', 'property']).apply(lambda x: set(x.file)).reset_index()
df.columns = ["documented", "property", "files"]
# df.columns = ['files']


with open('REPORT.md', 'w') as f:
    f.writelines(tabulate(df, tablefmt="pipe", headers="keys", showindex=False))
