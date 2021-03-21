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




file = find_file('safety_honda.h', '/data/openpilot')
with open (file.replace(".h", ".bak"), 'w') as file_write:
    with open (file, 'r') as file_read:
        for line in file_read:
            if "CanMsg HONDA_N_TX_MSGS[]" in line and "0xE4, 2, 5" not in line:
                file_write.write(line.replace("}};", "}, {0xE4, 2, 5}};"))
            else:
                file_write.write(line)
shutil.move(file.replace(".h", ".bak"), file)
os.chmod(file, 0o0777)

file = find_file('carstate.py', '/data/openpilot/selfdrive/car/honda')
with open (file.replace(".py", ".bak"), 'w') as file_write:
    carFPfound = False
    carFPfound2 = False
    carFPfound2_indents = False
    carFPfound3 = False
    carFPfound3_indents = False
    carFPfound4 = False
    with open (file, 'r') as file_read:
        for line in file_read:
            if "from selfdrive.car.honda.values" in line and "HONDA_NIDEC_SERIAL_STEERING" not in line:
                file_write.write(line.replace(line, line.strip("\n") + ", HONDA_NIDEC_SERIAL_STEERING\n"))
            elif "(\"STEER_STATUS\", \"STEER_STATUS\", " in line:
                file_write.write("      (\"STEER_STATUS\", \"STEER_STATUS\", 0), #needs 0 until we fix steer_status\n")

            elif " if CP.carFingerprint == CAR.ODYSSEY_CHN:" in line:
                file_write.write(line.replace("== ","in (").replace(":",", CAR.ACCORD_2016):"))

            elif "elif CP.carFingerprint == CAR.ACCORD_2016:" in line:
                carFPfound = True
                file_write.write(line)

            elif "add gas interceptor reading if we are using it" in line:
                if carFPfound == True:
                    file_write.write(line)
                else:
                    file_write.write("  elif CP.carFingerprint == CAR.ACCORD_2016:\n")
                    file_write.write("    signals += [(\"MAIN_ON\", \"SCM_BUTTONS\", 0),\n")
                    file_write.write("                (\"CAR_GAS\", \"GAS_PEDAL\", 0)]\n")
                    file_write.write("               # (\"LKAS_DISABLED\", \"STEER_MOTOR_TORQUE\",0)]\n")
                    file_write.write("    checks += [(\"GAS_PEDAL\", 100)]\n\n")
                    file_write.write(line)

            elif "self.steer_status_values =" in line and "#" not in line:
                file_write.write(line.replace(line, "#" + line))

            elif "if self.CP.carFingerprint in HONDA_NIDEC_SERIAL_STEERING:" in line:
                carFPfound2 = True
                file_write.write(line)

            elif "steer_status = self.steer_status_values" in line:
                if carFPfound2 == True:
                    file_write.write(line)
                else:
                    file_write.write("    if self.CP.carFingerprint in HONDA_NIDEC_SERIAL_STEERING:\n")
                    file_write.write("      steer_status = 1\n")
                    file_write.write("      ret.steerError = bool(cp_cam.vl[\"STEER_STATUS\"]['LIN_INTERFACE_FATAL_ERROR'])\n")
                    file_write.write("      self.steer_not_allowed =  bool(abs(cp_cam.vl[\"STEER_STATUS\"]['STEER_TORQUE_SENSOR']) > 95)\n")
                    file_write.write("      ret.steerWarning = False\n")
                    file_write.write("    else:\n")
                    file_write.write(line.replace(line, "  " + line))
                    carFPfound2_indents = True

            elif "ret.steerError = " in line and carFPfound2_indents == True:
                file_write.write(line.replace(line, ("  " + line)))
            elif "self.steer_not_allowed =" in line and carFPfound2_indents == True:
                file_write.write(line.replace(line, "  " + line))
            elif "ret.steerWarning =" in line and carFPfound2_indents == True:
                file_write.write(line.replace(line, "  " + line))

            elif "if self.CP.carFingerprint in (CAR.CRV, CAR.CRV_EU, CAR.HRV, CAR.ODYSSEY, CAR.ACURA_RDX, CAR.RIDGELINE, CAR.PILOT_2019, CAR.ODYSSEY_CHN" in line and "CAR.ACCORD_2016" not in line:
                file_write.write(line.replace("):", ", CAR.ACCORD_2016):"))

            elif "if self.CP.carFingerprint in (HONDA_NIDEC_SERIAL_STEERING):" in line:
                carFPfound3 = True
                file_write.write(line)
            elif "ret.steeringTorque =" in line:
                if carFPfound3 == True:
                    file_write.write(line)
                else:
                    file_write.write("    if self.CP.carFingerprint in (HONDA_NIDEC_SERIAL_STEERING):\n")
                    file_write.write("      ret.steeringTorque = cp_cam.vl[\"STEER_STATUS\"]['STEER_TORQUE_SENSOR']\n")
                    file_write.write("      ret.steeringTorqueEps = cp_cam.vl[\"STEER_MOTOR_TORQUE\"]['MOTOR_TORQUE']\n")
                    file_write.write("    else:\n")
                    file_write.write(line.replace(line, "  " + line))
                    carFPfound3_indents = True
            elif "ret.steeringTorqueEps =" in line and carFPfound3_indents == True:
                file_write.write(line.replace(line, ("  " + line)))


            elif "if CP.carFingerprint in HONDA_NIDEC_SERIAL_STEERING:" in line:
                carFPfound4 = True
                file_write.write(line)

            elif "CP.carFingerprint in [CAR.CRV, CAR.CRV_EU, CAR.ACURA_RDX, CAR.ODYSSEY_CHN" in line:
                if carFPfound4 == True:
                    file_write.write(line)
                else:
                    file_write.write("    if CP.carFingerprint in HONDA_NIDEC_SERIAL_STEERING:\n")
                    file_write.write("      checks = [(\"STEER_MOTOR_TORQUE\",0),\n")
                    file_write.write("                (\"STEER_STATUS\",0)]\n")
                    file_write.write("      signals += [(\"LIN_INTERFACE_FATAL_ERROR\", \"STEER_STATUS\", 0),\n")
                    file_write.write("                  (\"MOTOR_TORQUE\", \"STEER_MOTOR_TORQUE\", 0),\n")
                    file_write.write("                  (\"STEER_TORQUE_SENSOR\", \"STEER_STATUS\", 0)]\n")
                    file_write.write(line)

            else:
                file_write.write(line)
shutil.move(file.replace(".py", ".bak"), file)
os.chmod(file, 0o0777)


file = find_file('hondacan.py', '/data/openpilot/selfdrive/car/honda')
with open (file.replace(".py", ".bak"), 'w') as file_write:
    with open (file, 'r') as file_read:
        for line in file_read:
            if "from selfdrive.car.honda.values import" in line and "HONDA_NIDEC_SERIAL_STEERING" not in line:
                file_write.write(line.replace(line, line.strip("\n") + ", HONDA_NIDEC_SERIAL_STEERING\n"))
            elif "bus = get_lkas_cmd_bus" in line and "," in line:
                if "HONDA_NIDEC_SERIAL_STEERING" not in line:
                    file_write.write(line.replace("bus =", "bus = 2 if car_fingerprint in HONDA_NIDEC_SERIAL_STEERING else"))
            else:
                file_write.write(line)
shutil.move(file.replace(".py", ".bak"), file)
os.chmod(file, 0o0777)



file = find_file('interface.py', '/data/openpilot/selfdrive/car/honda')
with open (file.replace(".py", ".bak"), 'w') as file_write:
    foundSection = False
    with open (file, 'r') as file_read:
        for line in file_read:
            if "elif candidate == CAR.ACCORD_2016:" in line:
                foundSection = True
                file_write.write(line)

            elif "elif candidate == CAR.ACURA_ILX:" in line:
                if foundSection == True:
                    file_write.write(line)
                else:
                    file_write.write("    elif candidate == CAR.ACCORD_2016:\n")
                    file_write.write("      stop_and_go = False\n")
                    file_write.write("      ret.safetyParam = 1\n")
                    file_write.write("      ret.mass = 3360. * CV.LB_TO_KG + STD_CARGO_KG\n")
                    file_write.write("      ret.wheelbase = 2.75\n")
                    file_write.write("      ret.centerToFront = ret.wheelbase * 0.39\n")
                    file_write.write("      ret.steerRatio = 13.23\n")
                    file_write.write("      ret.lateralParams.torqueBP, ret.lateralParams.torqueV = [[0, 238], [0, 238]]  # TODO: determine if there is a dead zone at the top end\n")
                    file_write.write("      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.24], [0.08]]\n")
                    file_write.write("      tire_stiffness_factor = 0.8467\n")
                    file_write.write("      ret.longitudinalTuning.kpBP = [0., 5., 35.]\n")
                    file_write.write("      ret.longitudinalTuning.kpV = [1.2, 0.8, 0.5]\n")
                    file_write.write("      ret.longitudinalTuning.kiBP = [0., 35.]\n")
                    file_write.write("      ret.longitudinalTuning.kiV = [0.18, 0.12]\n\n")
                    file_write.write(line)
            else:
                file_write.write(line)
shutil.move(file.replace(".py", ".bak"), file)
os.chmod(file, 0o0777)



carInClass = False
valueFP = False
fwVer = False
dbcChk = False
steerThreshold = False
speedFactor = False
findObject = False

file = find_file('values.py', '/data/openpilot/selfdrive/car/honda')
with open (file, 'r') as file_read:
    for line in file_read:
        if "ACCORD_2016 = \"HONDA ACCORD 2016 SERIAL STEERING\"" in line:
            carInClass = True
        elif "CAR.ACCORD_2016: [{" in line:
            valueFP = True
        elif "CAR.ACCORD_2016: {" in line:
            fwVer = True
        elif "CAR.ACCORD_2016: dbc_dict('honda_accord_touring_2016_can', 'acura_ilx_2016_nidec')" in line:
            dbcChk = True
        elif "CAR.ACCORD_2016: 25," in line:
            steerThreshold = True
        elif "CAR.ACCORD_2016: 1.," in line:
            speedFactor = True
        elif "HONDA_NIDEC_SERIAL_STEERING =" in line:
            findObject = True

with open (file.replace(".py", ".bak"), 'w') as file_write:
    with open (file, 'r') as file_read:
        for line in file_read:
            if "class CAR:" in line:
                if carInClass == True:
                    file_write.write(line)
                else:
                    file_write.write(line)
                    file_write.write("  ACCORD_2016 = \"HONDA ACCORD 2016 SERIAL STEERING\"\n")
                    continue

            elif "CAR.ACURA_ILX: [{" in line:
                if valueFP == True:
                    file_write.write(line)
                else:
                    file_write.write("  CAR.ACCORD_2016: [{\n")
                    file_write.write("    57: 3, 145: 8, 316: 8, 342: 6, 344: 8, 380: 8, 398: 3, 401: 8, 420: 8, 422: 8, 426: 8, 432: 7, 464: 8, 476: 4, 487: 4, 490: 8, 506: 8, 507: 1, 542: 7, 545: 4, 597: 8, 660: 8, 661: 4, 773: 7, 777: 8, 780: 8, 800: 8, 804: 8, 808: 8, 829: 5, 871: 8, 882: 2, 884: 8, 891: 8, 892: 8, 918: 7, 923: 2, 927: 8, 929: 8, 983: 8, 985: 3, 1024: 5, 1027: 5, 1029: 8, 1036: 8, 1039: 8, 1057: 5, 1064: 7, 1088: 8, 1089: 8, 1108: 8, 1125: 8, 1296: 3, 1365: 5, 1424: 5, 1600: 5, 1601: 8\n")
                    file_write.write("  }],\n")
                    file_write.write(line)
                    continue

            elif "CAR.ACCORDH: {" in line:
                if fwVer == True:
                    file_write.write(line)
                else:
                    file_write.write("  CAR.ACCORD_2016: {\n")
                    file_write.write("    (Ecu.vsa, 0x18DA28F1, None): [\n")
                    file_write.write("      b'57114-T2F-X840\\x00\\x00',\n")
                    file_write.write("    ],\n")
                    file_write.write("    (Ecu.fwdRadar, 0x18DAB0F1, None): [\n")
                    file_write.write("      b'36161-T2F-A140\\x00\\x00',\n")
                    file_write.write("    ],\n")
                    file_write.write("    (Ecu.combinationMeter, 0x18DA60F1, None): [\n")
                    file_write.write("      b'78109-T2F-L110\\x00\\x00',\n")
                    file_write.write("    ],\n")
                    file_write.write("    (Ecu.srs, 0x18DA53F1, None): [\n")
                    file_write.write("      b'77959-T2F-A030\\x00\\x00',\n")
                    file_write.write("    ],\n")
                    file_write.write("  },\n")
                    file_write.write(line)
                    continue

            elif "b'37805-5PA-AF20\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'78109-TLA-A120\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'77959-TLA-A420\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'37805-5YF-C210\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'36802-TJB-A050\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'78109-TJB-AD10\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'78109-TJB-AW10\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'77959-TJB-A210\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'38897-TJB-A120\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'39990-TJB-A040\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'39990-T6Z-A050\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'36161-T6Z-A620\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'78109-T6Z-AA10\\x00\\x00'," in line:
                pass #delete the line if exists
            elif "b'78109-THX-A220\\x00\\x00'," in line:
                pass #delete the line if exists

            elif "DBC = {" in line:
                if dbcChk == True:
                    file_write.write(line)
                else:
                    file_write.write(line)
                    file_write.write("  CAR.ACCORD_2016: dbc_dict('honda_accord_touring_2016_can', 'acura_ilx_2016_nidec'),\n")

            elif "STEER_THRESHOLD = {" in line:
                if steerThreshold == True:
                    file_write.write(line)
                else:
                    file_write.write(line)
                    file_write.write("  CAR.ACCORD_2016: 25,\n")

            elif "SPEED_FACTOR = {" in line:
                if speedFactor == True:
                    file_write.write(line)
                else:
                    file_write.write(line)
                    file_write.write("  CAR.ACCORD_2016: 1.,\n")

            elif "HONDA_BOSCH = set" in line:
                if findObject == True:
                    file_write.write(line)
                else:
                    file_write.write(line)
                    file_write.write("HONDA_NIDEC_SERIAL_STEERING = set([CAR.ACCORD_2016])\n")

            else:
                file_write.write(line)
shutil.move(file.replace(".py", ".bak"), file)
os.chmod(file, 0o0777)

shutil.copy("honda_accord_touring_2016_can.dbc", "/data/openpilot/opendbc/honda_accord_touring_2016_can.dbc")
os.chmod('/data/openpilot/opendbc/honda_accord_touring_2016_can.dbc', 0o0777)
print ("Serial steering patch complete!");
