import json
import os

original_path = os.getcwd() + '/original/'

for file_name in os.listdir(original_path):
    file_path = os.path.join(original_path, file_name)

    f = open(file_path, "r")
    content = f.read()
    f.close()

    json_content = json.loads(content)
    results = json_content['response']['results']

    result_path = os.getcwd() + '/result/' + file_name
    result_file = open(result_path, "w+")
    for result in results:
        result_file.write(result['alternatives'][0]['transcript'] + '\n')