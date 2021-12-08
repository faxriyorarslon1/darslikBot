import requests
file_info = tb.get_file(file_id)

file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))