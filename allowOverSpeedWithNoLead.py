import shutil
import os

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


file = find_file('controlsd.py', '/data/openpilot/selfdrive/controls')
with open (file.replace(".py", ".bak"), 'w') as file_write:
    with open (file, 'r') as file_read:
        for line in file_read:
            if "self.LoC.update(self.active, CS, v_acc_sol, long_plan.vTargetFuture, a_acc_sol, self.CP" in line and "long_plan.hasLead" not in line:
                file_write.write(line.replace(")", ", long_plan.hasLead)"))
            else:
                file_write.write(line)
shutil.move(file.replace(".py", ".bak"), file)
os.chmod(file, 0o0777)


file = find_file('longcontrol.py', '/data/openpilot/selfdrive/controls/lib')
with open (file.replace(".py", ".bak"), 'w') as file_write:
    with open (file, 'r') as file_read:
        for line in file_read:
            if "self.last_output_gb = output_gb" in line:
                file_write.write("    if not has_Lead and output_gb < 0.:")
                file_write.write("      output_gb = 0.")
                file_write.write()
                file_write.write(line)
            elif "def update(self, active, CS, v_target, v_target_future, a_target, CP" in line and "hasLead" is not in line:
                file_write.write(line.replace("CP):","CP, hasLead):"))
            else:
                file_write.write(line)
shutil.move(file.replace(".py", ".bak"), file)
os.chmod(file, 0o0777)


# shutil.copy("honda_accord_touring_2016_can.dbc", "/data/openpilot/opendbc/honda_accord_touring_2016_can.dbc")
# os.chmod('/data/openpilot/opendbc/honda_accord_touring_2016_can.dbc', 0o0777)
print ("No Brakes for Over Speed when not following patch complete!");
