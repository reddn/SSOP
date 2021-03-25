import shutil
import os

torquePatch = """    if apply_steer > 229 and False:
      apply_steer_orig = apply_steer
      apply_steer = (apply_steer - 228) * 2 + apply_steer
      if apply_steer > 240:
        self.apply_steer_over_max_counter += 1
        if self.apply_steer_over_max_counter > 3:
          apply_steer = apply_steer_orig
          self.apply_steer_over_max_counter = 0
      else:
        self.apply_steer_over_max_counter = 0
    elif apply_steer < -229 and False:
      apply_steer_orig = apply_steer
      apply_steer = (apply_steer + 228) * 2 + apply_steer                                                              >      if apply_steer < -240:
        self.apply_steer_over_max_counter+= 1
        if self.apply_steer_over_max_counter > 3:
          apply_steer = apply_steer_orig
          self.apply_steer_over_max_counter = 0
      else:
        self.apply_steer_over_max_counter = 0
    else:
      self.apply_steer_over_max_counter = 0
"""


def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

import os, fnmatch
def find_pattern(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


file = find_file('carcontroller.py', '/data/openpilot/selfdrive/car/honda')
with open (file.replace(".py", ".bak"), 'w') as file_write:
    with open (file, 'r') as file_read:
        for line in file_read:
            if "apply_steer = int(interp(" in line:
                file_write.write(line)
                file_write.write("\n")
                file_write.write(torquePatch)
            else:
                file_write.write(line)
shutil.move(file.replace(".py", ".bak"), file)
os.chmod(file, 0o0777)




# shutil.copy("honda_accord_touring_2016_can.dbc", "/data/openpilot/opendbc/honda_accord_touring_2016_can.dbc")
# os.chmod('/data/openpilot/opendbc/honda_accord_touring_2016_can.dbc', 0o0777)
print ("No Brakes for Over Speed when not following patch complete!");
