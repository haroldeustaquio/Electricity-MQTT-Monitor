import json

def save_json(data, filename, folder = 'data'):
    try:
        if folder is None:
            with open(f'{filename}.json', "w") as f:
                json.dump(data, f, indent=4)
        else:
            with open(f'{folder}/{filename}.json', "w") as f:
                json.dump(data, f, indent=4)
    except FileNotFoundError:
        print(f'Error: Directory "data" not found. Could not save {filename}.json')
    except Exception as e:
        print(f'Unexpected error when saving {filename}.json: {e}')

def read_json(filename,folder="data"):
    try:
        if folder is None:
            with open(f'{filename}.json', 'r') as file:
                data = json.load(file)
                return data
        else:
            with open(f'{folder}/{filename}.json', "r") as file:
                data = json.load(file)
                return data
            
    except FileNotFoundError:
        print(f'Error: {filename}.json not found')
    except json.JSONDecodeError:
        print(f'Error: {filename}.json contains invalid JSON')
    except Exception as e:
        print(f'Unexpected error when reading {filename}.json: {e}')
    return None

def load_update(data_json,filename, folder='data'):
    
    data = read_json(filename,folder)
    if data is None:
        print(f"Error: Couldn't load {filename} file")
        return
    
    if not isinstance(data, list):
        print(f"Error: {filename} file doesn't contain a list")
        return
    
    data.extend(data_json)
    
    # Save data
    save_json(data,filename,folder)
