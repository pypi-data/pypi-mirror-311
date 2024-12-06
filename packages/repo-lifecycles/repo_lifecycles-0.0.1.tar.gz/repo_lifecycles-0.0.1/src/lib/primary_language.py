import os
import json
from collections import defaultdict

def language_sizes(repo_path):
    json_file_path = os.path.join(os.path.dirname(__file__), "resources", "file_extensions.json")
    with open(json_file_path, 'r') as json_file:
        language_extensions = json.load(json_file)
    language_sizes = defaultdict(int)
    for root, _, files in os.walk(repo_path):
        for file in files:
            ext = file.split('.')[-1]
            if ext in language_extensions.keys():
                file_path = os.path.join(root, file)
                with open(file_path, 'r', errors='ignore') as f:
                    lines = f.readlines()
                    language_sizes[language_extensions[ext]] += len(lines)
    return language_sizes