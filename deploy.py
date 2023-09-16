import os, sys, json, time

def print_info(text: str):
  print(text, end='\n\n')

def print_warning(text: str):
  print('**warning**:', text)

def print_config_error():
  print_warning('configuration file must be a json containing those keys: \"targets\"(string array), \"search_dirs\"(string array), \"out_dir\"(string)')


json_data = {'targets': [''], 'search_dirs': [''], 'out_dir': ''}
targets_found_flag_list = []
targets_rest_count = 0

def copy_file(src_path: str, out_path: str):
  print('copying file:', src_path, '->', out_path, flush=True)
  with open(src_path, 'rb') as f_in:
    with open(out_path, 'wb') as f_out:
      f_out.write(f_in.read())

def walk_file(dir: str):
  global targets_rest_count
  if targets_rest_count == 0:
    return

  for root, dirs, files in os.walk(dir):
    # print('walk', root, dirs, files)
    #
    # files
    #
    i = 0
    for wait_for_search_file in json_data['targets']:
      # if not yet found
      if targets_found_flag_list[i] == False:
        for cur_file in files:
          if cur_file == wait_for_search_file:
            targets_found_flag_list[i] = True
            copy_file(os.path.join(root, cur_file), os.path.join(json_data['out_dir'], cur_file))
            targets_rest_count -= 1
            break
          # found wait_for_search_file!
      if targets_rest_count == 0: return
      i+=1
    
    #
    # dirs
    #
    for dir in dirs:
      walk_file(os.path.join(root, dir))

if(__name__ == '__main__'):
  cwd_path = os.getcwd()
  # print(cwd_path)
  dependents_file_path = ''
  if len(sys.argv) > 1: 
    dependents_file_path = sys.argv[1]
  dependents_file_path = os.path.join(dependents_file_path)

  # check if has dependents_file_path
  if not os.path.exists(dependents_file_path):
    print_warning('{} not exists'.format(dependents_file_path))
    exit(-1)

  print_info('read configuration from{}'.format(dependents_file_path))
  
  # 
  # initialize vars
  #
  try:
    with open(dependents_file_path, mode = 'r') as f:
      json_data = json.load(f)
  except:
    print_config_error()
    exit(-1)
  
  #
  # check config file
  #
  if 'targets' not in json_data or 'search_dirs' not in json_data or 'out_dir' not in json_data:
    print_config_error()
    exit(-1)

  for k in json_data:
    v = json_data[k]
    # print(k, type(v))
    if ('targets' == k and not isinstance(v, list)) or ('search_dirs' == k and not isinstance(v, list)) or ('out_dir' == k and not isinstance(v, str)) :
      print_config_error()
      exit(-1)


  if not os.path.exists(json_data['out_dir']):
    os.mkdir(json_data['out_dir'])
  # print_info('configurations: {}'.format(json_data))
  targets_rest_count = len(json_data['targets'])
  # mark targets as not found 
  for i in json_data['targets']:
    targets_found_flag_list.append(False)
  
  t = time.time()
  for src_rootdir in json_data['search_dirs']:
    walk_file(src_rootdir)
  
  # print targets not found
  if targets_rest_count > 0:
    print('not found: ', end='')
    i = 0
    for dll in json_data['targets']:
      if not targets_found_flag_list[i]:
        print(dll, end = ' ')
      i += 1
  t = time.time() - t
  print()
  print_info('finished at {} {}'.format(t if t > 1 else t * 1000, 's' if t > 1 else 'ms'))