import platform
from simple_term_menu import TerminalMenu
from subprocess import call
from os.path import expanduser

from tools.dtos.utill_var import var as utils_var

def render_choices(options:list):
  options.append("Back")
  terminal_menu = TerminalMenu(options)
  menu_entry_index = terminal_menu.show()
  result = options[menu_entry_index]
  if "Back" in result :
    return False
  return result

def get_executable():
  if platform.system()=='Darwin':
    executable = "/bin/zsh"
  else:
    executable = "/bin/bash"
  return executable

def get_config_path(path):
  path = path.split("~")[1]
  return expanduser("~")+path

def routing(gateway_ip, cidr):
  try:
    if platform.system()=='Darwin':
      try:
        call([
          'sudo',
          'route',
          'add',
          str(cidr),
          str(gateway_ip)
        ])
      except:
        call([
          'sudo',
          'route',
          'change',
          str(cidr),
          str(gateway_ip)
        ])
    else:
      try:
        call([
          'sudo',
          'ip',
          'route',
          'add',
          str(cidr),
          'via',
          str(gateway_ip)
        ])
      except:
        call([
          'sudo',
          'ip',
          'route',
          'replace',
          str(cidr),
          'via',
          str(gateway_ip)
        ])
  except:
    raise "Route error!"

def exist_handler(signum, frame):
  if utils_var.allow_exist == False:
    utils_var.allow_exist = True
  else:
    exit(1)

def ex_stacks(stacks: list): 
  i = 0
  while i < len(stacks) and i!= -1:
    r = stacks[i]()
    if r == True :
      i += 1
    elif r == False :
      i-=1
      
  if i != -1:
    return True
  return False
