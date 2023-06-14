import json

# Read JSON data from a file
with open('/home/said/projects/handwriting-datasets/project-1-at-2023-06-13-20-22-08d03e05.json') as file:
    data = json.load(file)

count = 0
for item in data:
    if "transcription" in item:
        print(item.get('bbox'))
        break
        count += len(item["transcription"])

print("Total transcriptions:", count)


# convert from LS percent units to pixels 
def convert_from_ls(result):
    if 'original_width' not in result or 'original_height' not in result:
        return None

    value = result['value']
    w, h = result['original_width'], result['original_height']

    if all([key in value for key in ['x', 'y', 'width', 'height']]):
        return w * value['x'] / 100.0, \
               h * value['y'] / 100.0, \
               w * value['width'] / 100.0, \
               h * value['height'] / 100.0