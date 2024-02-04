# Main file 
import json

# The following function loads the config.json file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    config = load_config('config.json')


    return

if __name__ == '__main__':
    main()