#!/usr/bin/env python3
import json
import os

def resolve_reference(reference, defs):
    """Resolve a reference like '#/$defs/AllocatedSubframe' to its actual value in defs."""
    # Strip the initial '#/' and split by '/'
    path = reference.lstrip('#/').split('/')
    
    # Navigate through defs based on the path
    current = defs
    for part in path[1:]:  # skip 'defs'
        if part in current:
            current = current[part]
        else:
            raise ValueError(f"Reference {reference} not found in $defs.")
    return current

def replace_references(data, defs):
    """Recursively replace all references in the data with values from defs."""
    if isinstance(data, dict):
        return {k: replace_references(v, defs) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_references(item, defs) for item in data]
    elif isinstance(data, str) and data.startswith("#/$defs/"):
        return resolve_reference(data, defs)
    else:
        return data

def schema_replace(json_path):
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # json_path = os.path.join(current_dir, "schema", "schema.json")
    # json_path_out = os.path.join(current_dir, "schema", "schema.json")
    # Load the JSON file
    with open(json_path, 'r') as file:
        json_data = json.load(file)
    
    # Extract $defs section
    defs = json_data.get('$defs', {})
    
    # Replace all references in the JSON
    updated_json = replace_references(json_data, defs)

    defs = updated_json.get('$defs', {})
    
    # Replace all references in the JSON
    updated_json = replace_references(updated_json, defs)
    
    # Save the updated JSON to a new file
    with open(json_path, 'w') as file:
        json.dump(updated_json, file, indent=4)
