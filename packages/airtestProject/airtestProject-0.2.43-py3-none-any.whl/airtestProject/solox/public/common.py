import json
import os
import platform
import re
import shutil
import time
import requests
from logzero import logger
from tqdm import tqdm
import socket
from urllib.request import urlopen
import ssl
import xlwt
import psutil
import signal
import cv2
from airtestProject.airtest.utils.compat import script_dir_name
from airtestProject.commons.utils.tools import get_folder_path_up
from jinja2 import Environment, FileSystemLoader
from tidevice._device import Device
from tidevice import Usbmux
from airtestProject.solox.public.adb import adb


class Platform:
    Android = 'Android'
    iOS = 'iOS'
    Mac = 'MacOS'
    Windows = 'Windows'


class Devices:

    def __init__(self, platform=Platform.Android):
        self.platform = platform
        self.adb = adb.adb_path

    def execCmd(self, cmd):
        """Execute the command to get the terminal print result"""
        r = os.popen(cmd)
        try:
            text = r.buffer.read().decode(encoding='gbk').replace('\x1b[0m', '').strip()
        except UnicodeDecodeError:
            text = r.buffer.read().decode(encoding='utf-8').replace('\x1b[0m', '').strip()
        finally:
            r.close()
        return text

    def filterType(self):
        """Select the pipe filtering method according to the system"""
        filtertype = ('grep', 'findstr')[platform.system() == Platform.Windows]
        return filtertype

    def getDeviceIds(self):
        """Get all connected device ids"""
        Ids = list(os.popen(f"{self.adb} devices").readlines())
        deviceIds = []
        for i in range(1, len(Ids) - 1):
            id, state = Ids[i].strip().split()
            if state == 'device':
                deviceIds.append(id)
        return deviceIds

    def getDevicesName(self, deviceId):
        """Get the device name of the Android corresponding device ID"""
        try:
            devices_name = os.popen(f'{self.adb} -s {deviceId} shell getprop ro.product.model').readlines()[0].strip()
        except Exception:
            devices_name = os.popen(f'{self.adb} -s {deviceId} shell getprop ro.product.model').buffer.readlines()[
                0].decode("utf-8").strip()
        return devices_name

    def getDevices(self):
        """Get all Android devices"""
        DeviceIds = self.getDeviceIds()
        Devices = [f'{id}({self.getDevicesName(id)})' for id in DeviceIds]
        logger.info('Connected devices: {}'.format(Devices))
        return Devices

    def getIdbyDevice(self, deviceinfo, platform):
        """Obtain the corresponding device id according to the Android device information"""
        if platform == Platform.Android:
            deviceId = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", deviceinfo)
            if deviceId not in self.getDeviceIds():
                raise Exception('no device found')
        else:
            deviceId = deviceinfo
        return deviceId

    def getSdkVersion(self, deviceId):
        version = adb.shell(cmd='getprop ro.build.version.sdk', deviceId=deviceId)
        return version

    def getPid(self, deviceId, pkgName):
        """Get the pid corresponding to the Android package name"""
        try:
            sdkversion = self.getSdkVersion(deviceId)
            if sdkversion and int(sdkversion) < 26:
                result = os.popen(f"{self.adb} -s {deviceId} shell ps | {self.filterType()} {pkgName}").readlines()
                resultList = [result[0]]
                # print(resultList)
                processList = ['{}:{}'.format(process.split()[1], process.split()[8]) for process in resultList]
            else:
                result = os.popen(f"{self.adb} -s {deviceId} shell ps -ef | {self.filterType()} {pkgName}").readlines()
                processList = ['{}:{}'.format(process.split()[1], process.split()[7]) for process in result]
            for i in range(len(processList)):
                if processList[i].count(':') == 1:
                    index = processList.index(processList[i])
                    processList.insert(0, processList.pop(index))
                    break
            if len(processList) == 0:
                logger.warning('{}: no pid found'.format(pkgName))
        except Exception as e:
            processList = []
            logger.exception(e)
        return processList

    def checkPkgname(self, pkgname):
        flag = True
        replace_list = ['com.google']
        for i in replace_list:
            if i in pkgname:
                flag = False
        return flag

    def getPkgname(self, deviceId):
        """Get all package names of Android devices"""
        pkginfo = os.popen(f"{self.adb} -s {deviceId} shell pm list packages --user 0")
        pkglist = [p.lstrip('package').lstrip(":").strip() for p in pkginfo]
        if pkglist.__len__() > 0:
            return pkglist
        else:
            pkginfo = os.popen(f"{self.adb} -s {deviceId} shell pm list packages")
            pkglist = [p.lstrip('package').lstrip(":").strip() for p in pkginfo]
            return pkglist

    def getDeviceInfoByiOS(self):
        """Get a list of all successfully connected iOS devices"""
        deviceInfo = [udid for udid in Usbmux().device_udid_list()]
        logger.info('Connected devices: {}'.format(deviceInfo))
        return deviceInfo

    def getPkgnameByiOS(self, udid):
        """Get all package names of the corresponding iOS device"""
        d = Device(udid)
        pkgNames = [i.get("CFBundleIdentifier") for i in d.installation.iter_installed(app_type="User")]
        return pkgNames

    def get_pc_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            logger.error('get local ip failed')
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def get_device_ip(self, deviceId):
        content = os.popen(f"{self.adb} -s {deviceId} shell ip addr show wlan0").read()
        logger.info(content)
        math_obj = re.search(r'inet\s(\d+\.\d+\.\d+\.\d+).*?wlan0', content)
        if math_obj and math_obj.group(1):
            return math_obj.group(1)
        return None

    def devicesCheck(self, platform, deviceid=None, pkgname=None):
        """Check the device environment"""
        if platform == Platform.Android:
            if len(self.getDeviceIds()) == 0:
                raise Exception('no devices found')
            if len(self.getPid(deviceId=deviceid, pkgName=pkgname)) == 0:
                raise Exception('no process found')
        elif platform == Platform.iOS:
            if len(self.getDeviceInfoByiOS()) == 0:
                raise Exception('no devices found')
        else:
            raise Exception('platform must be Android or iOS')


    def getDdeviceDetail(self, deviceId, platform):
        result = dict()
        if platform == Platform.Android:
            result['brand'] = adb.shell(cmd='getprop ro.product.brand', deviceId=deviceId)
            result['name'] = adb.shell(cmd='getprop ro.product.model', deviceId=deviceId)
            cmd1 = '"cat /proc/cpuinfo | grep \'processor\' | wc -l"'
            result['cpuinfo'] = adb.shell(cmd=cmd1, deviceId=deviceId)
            result['version'] = adb.shell(cmd='getprop ro.build.version.release', deviceId=deviceId)
            result['serialno'] = adb.shell(cmd='getprop ro.serialno', deviceId=deviceId)
            cmd = f'ip addr show wlan0 | {self.filterType()} link/ether'
            wifiadr_content = adb.shell(cmd=cmd, deviceId=deviceId)
            result['wifiadr'] = Method._index(wifiadr_content.split(), 1, '')
        elif platform == Platform.iOS:
            ios_device = Device(udid=deviceId)
            result['brand'] = ios_device.get_value("DeviceClass", no_session=True)
            result['name'] = ios_device.get_value("DeviceName", no_session=True)
            result['version'] = ios_device.get_value("ProductVersion", no_session=True)
            result['serialno'] = deviceId
            result['wifiadr'] = ios_device.get_value("WiFiAddress", no_session=True)
        else:
            raise Exception('{} is undefined'.format(platform))
        return result

    def getCurrentActivity(self, deviceId):
        result = adb.shell(cmd='dumpsys window | {} mCurrentFocus'.format(self.filterType()), deviceId=deviceId)
        if result.__contains__('mCurrentFocus'):
            activity = str(result).split(' ')[-1].replace('}', '')
            return activity
        else:
            raise Exception('no activity found')

    def getStartupTimeByAndroid(self, activity, deviceId):
        result = adb.shell(cmd='am start -W {}'.format(activity), deviceId=deviceId)
        return result

    def getStartupTimeByiOS(self, pkgname):
        try:
            import ios_device
        except ImportError:
            logger.error('py-ios-devices not found, please run [pip install py-ios-devices]')
        result = self.execCmd('pyidevice instruments app_lifecycle -b {}'.format(pkgname))
        return result


class File:

    def __init__(self, fileroot='.', file_path=None):
        self.fileroot = fileroot
        self.report_dir = self.get_repordir(file_path)
        self.test = os.path.dirname(os.path.realpath(__file__))
        self.script_root, self.script_name = script_dir_name(self.test)

    def clear_file(self):
        logger.info('Clean up useless files ...')
        if os.path.exists(self.report_dir):
            for f in os.listdir(self.report_dir):
                filename = os.path.join(self.report_dir, f)
                if f.split(".")[-1] in ['log', 'json', 'mkv']:
                    os.remove(filename)
        logger.info('Clean up useless files success')

    def export_excel(self, platform, scene):
        logger.info('Exporting excel ...')
        android_log_file_list = ['cpu_app', 'cpu_sys', 'cpu_freq', 'mem_total', 'mem_native', 'mem_dalvik',
                                 'battery_level', 'battery_tem', 'upflow', 'downflow', 'fps', 'gpu']
        ios_log_file_list = ['cpu_app', 'cpu_sys', 'mem_total', 'battery_tem', 'battery_current',
                             'battery_voltage', 'battery_power', 'upflow', 'downflow', 'fps', 'gpu']
        log_file_list = android_log_file_list if platform == 'Android' else ios_log_file_list
        wb = xlwt.Workbook(encoding='utf-8')

        k = 1
        for name in log_file_list:
            ws1 = wb.add_sheet(name)
            ws1.write(0, 0, 'Time')
            ws1.write(0, 1, 'Value')
            row = 1  # start row
            col = 0  # start col
            if os.path.exists(f'{self.report_dir}/{scene}/{name}.log'):
                f = open(f'{self.report_dir}/{scene}/{name}.log', 'r', encoding='utf-8')
                for lines in f:
                    target = lines.split('=')
                    k += 1
                    for i in range(len(target)):
                        ws1.write(row, col, target[i])
                        col += 1
                    row += 1
                    col = 0
        xls_path = os.path.join(self.report_dir, scene, f'{scene}.xls')
        wb.save(xls_path)
        logger.info('Exporting excel success : {}'.format(xls_path))
        return xls_path

    def make_android_html(self, scene, summary: dict):
        logger.info('Generating HTML ...')
        STATICPATH = os.path.dirname(os.path.realpath(__file__))
        print(STATICPATH)
        file_loader = FileSystemLoader(os.path.join(STATICPATH, 'report_template'))
        env = Environment(loader=file_loader)
        template = env.get_template('android.html')
        with open(os.path.join(self.report_dir, scene, 'report.html'), 'w+', encoding='utf-8') as fout:
            html_content = template.render(cpu_app=summary['cpu_app'], cpu_sys=summary['cpu_sys'],
                                           mem_total=summary['mem_total'], mem_swap=summary['mem_swap'],
                                           fps=summary['fps'], jank=summary['jank'], bigjank=summary['bigjank'],
                                           Stutter=summary["Stutter"],
                                           maxTotalPass=summary['maxTotalPass'],
                                           level=summary['level'],
                                           gpu=summary['gpu'],
                                           tem=summary['tem'],
                                           corenum=summary['corenum'],
                                           temMax=summary['temMax'],
                                           temAvg=summary['temAvg'],net_send=summary['net_send'],
                                           net_recv=summary['net_recv'], cpu_charts=summary['cpu_charts'],
                                           cpufreq_charts=summary['cpufreq_charts'],
                                           mem_charts=summary['mem_charts'], net_charts=summary['net_charts'],
                                           battery_charts=summary['battery_charts'], fps_charts=summary['fps_charts'],
                                           jank_charts=summary['jank_charts'], bigjank_charts=summary['bigjank_charts'],
                                           Stutter_charts=summary['Stutter_charts'],
                                           mem_detail_charts=summary['mem_detail_charts'],
                                           gpu_charts=summary['gpu_charts'])

            fout.write(html_content)
        html_path = os.path.join(self.report_dir, scene, 'report.html')
        logger.info('Generating HTML success : {}'.format(html_path))
        return html_path

    def make_ios_html(self, scene, summary: dict):
        logger.info('Generating HTML ...')
        STATICPATH = os.path.dirname(os.path.realpath(__file__))
        file_loader = FileSystemLoader(os.path.join(STATICPATH, 'report_template'))
        env = Environment(loader=file_loader)
        template = env.get_template('ios.html')
        with open(os.path.join(self.report_dir, scene, 'report.html'), 'w+') as fout:
            html_content = template.render(cpu_app=summary['cpu_app'], cpu_sys=summary['cpu_sys'], gpu=summary['gpu'],
                                           mem_total=summary['mem_total'], fps=summary['fps'],
                                           tem=summary['tem'], current=summary['current'],
                                           voltage=summary['voltage'], power=summary['power'],
                                           net_send=summary['net_send'], net_recv=summary['net_recv'],
                                           cpu_charts=summary['cpu_charts'], mem_charts=summary['mem_charts'],
                                           net_charts=summary['net_charts'], battery_charts=summary['battery_charts'],
                                           fps_charts=summary['fps_charts'], gpu_charts=summary['gpu_charts'])
            fout.write(html_content)
        html_path = os.path.join(self.report_dir, scene, 'report.html')
        logger.info('Generating HTML success : {}'.format(html_path))
        return html_path

    def filter_secen(self, scene):
        dirs = os.listdir(self.report_dir)
        dir_list = list(reversed(sorted(dirs, key=lambda x: os.path.getmtime(os.path.join(self.report_dir, x)))))
        dir_list.remove(scene)
        return dir_list

    def get_repordir(self, file_path):
        ## 新的报告地址
        test_dir = file_path
        report_dir = get_folder_path_up(test_dir, "reports")
        if not os.path.exists(report_dir):
            os.mkdir(report_dir)
        return report_dir

    def create_file(self, filename, content=''):
        if not os.path.exists(self.report_dir):
            os.mkdir(self.report_dir)
        with open(os.path.join(self.report_dir, filename), 'a+', encoding="utf-8") as file:
            file.write(content)

    def add_log(self, path, log_time, value):
        if value >= 0:
            with open(path, 'a+', encoding="utf-8") as file:
                file.write(f'{log_time}={str(value)}' + '\n')

    def record_net(self, type, send, recv):
        net_dict = {}
        if type == "pre":
            net_dict['send'] = send
            net_dict['recv'] = recv
            content = json.dumps(net_dict)
            self.create_file(filename='pre_net.json', content=content)
        elif type == "end":
            net_dict['send'] = send
            net_dict['recv'] = recv
            content = json.dumps(net_dict)
            self.create_file(filename='end_net.json', content=content)
        else:
            logger.error('record network data failed')

    def make_report(self, script_name, app, devices, corenum, platform=Platform.Android, model='normal'):
        logger.info('Generating test results ...')
        current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        result_dict = {
            "app": app,
            "icon": "",
            "platform": platform,
            "model": model,
            "devices": devices,
            "corenum": corenum,
            "ctime": current_time,
        }
        content = json.dumps(result_dict)
        self.create_file(filename='result.json', content=content)
        report_new_dir = os.path.join(self.report_dir, f'apm.{script_name}-{current_time}')
        if not os.path.exists(report_new_dir):
            os.mkdir(report_new_dir)

        for f in os.listdir(self.report_dir):
            filename = os.path.join(self.report_dir, f)
            if f.split(".")[-1] in ['log', 'json', 'mkv']:
                shutil.move(filename, report_new_dir)
                if os.path.exists(filename):
                    os.remove(filename)
        logger.info('Generating test results success: {}'.format(report_new_dir))
        return f'apm.{script_name}-{current_time}', report_new_dir

    def instance_type(self, data):
        if isinstance(data, float):
            return 'float'
        elif isinstance(data, int):
            return 'int'
        else:
            return 'int'

    def open_file(self, path, mode):
        with open(path, mode) as f:
            for line in f:
                yield line

    def readLog(self, scene, filename):
        """Read apmlog file data"""
        log_data_list = list()
        target_data_list = list()
        if os.path.exists(os.path.join(self.report_dir, scene, filename)):
            lines = self.open_file(os.path.join(self.report_dir, scene, filename), "r")
            for line in lines:
                if isinstance(line.split('=')[1].strip(), int):
                    log_data_list.append({
                        "x": line.split('=')[0].strip(),
                        "y": int(line.split('=')[1].strip())
                    })
                    target_data_list.append(int(line.split('=')[1].strip()))
                else:
                    log_data_list.append({
                        "x": line.split('=')[0].strip(),
                        "y": float(line.split('=')[1].strip())
                    })
                    target_data_list.append(float(line.split('=')[1].strip()))
        return log_data_list, target_data_list

    def getCpuLog(self, platform, scene):
        targetDic = {}
        targetDic['cpuAppData'] = self.readLog(scene=scene, filename='cpu_app.log')[0]
        targetDic['cpuSysData'] = self.readLog(scene=scene, filename='cpu_sys.log')[0]
        result = {'status': 1, 'cpuAppData': targetDic['cpuAppData'], 'cpuSysData': targetDic['cpuSysData']}
        return result

    def getCpuFreqLog(self, platform, scene, corenum):
        targetDic = {}
        # print(corenum)
        for i in range(int(corenum)):
            targetDic['cpuFreq_{}'.format(i)] = self.readLog(scene=scene, filename='cpu_freq_{}.log'.format(i))[0]
        result = {'status': 1, 'cpuFreq': targetDic}
        # print(result)
        return result

    def getCpuLogCompare(self, platform, scene1, scene2):
        targetDic = {}
        targetDic['scene1'] = self.readLog(scene=scene1, filename='cpu_app.log')[0]
        targetDic['scene2'] = self.readLog(scene=scene2, filename='cpu_app.log')[0]
        result = {'status': 1, 'scene1': targetDic['scene1'], 'scene2': targetDic['scene2']}
        return result

    def getGpuLog(self, platform, scene):
        targetDic = {}
        targetDic['gpu'] = self.readLog(scene=scene, filename='gpu.log')[0]
        result = {'status': 1, 'gpu': targetDic['gpu']}
        return result

    def getGpuLogCompare(self, platform, scene1, scene2):
        targetDic = {}
        targetDic['scene1'] = self.readLog(scene=scene1, filename='gpu.log')[0]
        targetDic['scene2'] = self.readLog(scene=scene2, filename='gpu.log')[0]
        result = {'status': 1, 'scene1': targetDic['scene1'], 'scene2': targetDic['scene2']}
        return result

    def getMemLog(self, platform, scene):
        targetDic = {}
        targetDic['memTotalData'] = self.readLog(scene=scene, filename='mem_total.log')[0]
        if platform == Platform.Android:
            targetDic['memSwapData'] = self.readLog(scene=scene, filename='mem_swap.log')[0]
            result = {'status': 1,
                      'memTotalData': targetDic['memTotalData'],
                      'memSwapData': targetDic['memSwapData']}
        else:
            result = {'status': 1, 'memTotalData': targetDic['memTotalData']}
        return result

    def getMemDetailLog(self, platform, scene):
        targetDic = {}
        targetDic['java_heap'] = self.readLog(scene=scene, filename='mem_java_heap.log')[0]
        targetDic['native_heap'] = self.readLog(scene=scene, filename='mem_native_heap.log')[0]
        targetDic['code_pss'] = self.readLog(scene=scene, filename='mem_code_pss.log')[0]
        targetDic['stack_pss'] = self.readLog(scene=scene, filename='mem_stack_pss.log')[0]
        targetDic['graphics_pss'] = self.readLog(scene=scene, filename='mem_graphics_pss.log')[0]
        targetDic['private_pss'] = self.readLog(scene=scene, filename='mem_private_pss.log')[0]
        targetDic['system_pss'] = self.readLog(scene=scene, filename='mem_system_pss.log')[0]
        result = {'status': 1, 'memory_detail': targetDic}
        return result

    def getMemLogCompare(self, platform, scene1, scene2):
        targetDic = {}
        targetDic['scene1'] = self.readLog(scene=scene1, filename='mem_total.log')[0]
        targetDic['scene2'] = self.readLog(scene=scene2, filename='mem_total.log')[0]
        result = {'status': 1, 'scene1': targetDic['scene1'], 'scene2': targetDic['scene2']}
        return result

    def getBatteryLog(self, platform, scene):
        targetDic = {}
        if platform == Platform.Android:
            targetDic['batteryLevel'] = self.readLog(scene=scene, filename='battery_level.log')[0]
            targetDic['batteryTem'] = self.readLog(scene=scene, filename='battery_tem.log')[0]
            result = {'status': 1,
                      'batteryLevel': targetDic['batteryLevel'],
                      'batteryTem': targetDic['batteryTem']}
        else:
            targetDic['batteryTem'] = self.readLog(scene=scene, filename='battery_tem.log')[0]
            targetDic['batteryCurrent'] = self.readLog(scene=scene, filename='battery_current.log')[0]
            targetDic['batteryVoltage'] = self.readLog(scene=scene, filename='battery_voltage.log')[0]
            targetDic['batteryPower'] = self.readLog(scene=scene, filename='battery_power.log')[0]
            result = {'status': 1,
                      'batteryTem': targetDic['batteryTem'],
                      'batteryCurrent': targetDic['batteryCurrent'],
                      'batteryVoltage': targetDic['batteryVoltage'],
                      'batteryPower': targetDic['batteryPower']}
        return result

    def getBatteryLogCompare(self, platform, scene1, scene2):
        targetDic = {}
        if platform == Platform.Android:
            targetDic['scene1'] = self.readLog(scene=scene1, filename='battery_level.log')[0]
            targetDic['scene2'] = self.readLog(scene=scene2, filename='battery_level.log')[0]
            result = {'status': 1, 'scene1': targetDic['scene1'], 'scene2': targetDic['scene2']}
        else:
            targetDic['scene1'] = self.readLog(scene=scene1, filename='batteryPower.log')[0]
            targetDic['scene2'] = self.readLog(scene=scene2, filename='batteryPower.log')[0]
            result = {'status': 1, 'scene1': targetDic['scene1'], 'scene2': targetDic['scene2']}
        return result

    def getFlowLog(self, platform, scene):
        targetDic = {}
        targetDic['upFlow'] = self.readLog(scene=scene, filename='upflow.log')[0]
        targetDic['downFlow'] = self.readLog(scene=scene, filename='downflow.log')[0]
        result = {'status': 1, 'upFlow': targetDic['upFlow'], 'downFlow': targetDic['downFlow']}
        return result

    def getFlowSendLogCompare(self, platform, scene1, scene2):
        targetDic = {}
        targetDic['scene1'] = self.readLog(scene=scene1, filename='upflow.log')[0]
        targetDic['scene2'] = self.readLog(scene=scene2, filename='upflow.log')[0]
        result = {'status': 1, 'scene1': targetDic['scene1'], 'scene2': targetDic['scene2']}
        return result

    def getFlowRecvLogCompare(self, platform, scene1, scene2):
        targetDic = {}
        targetDic['scene1'] = self.readLog(scene=scene1, filename='downflow.log')[0]
        targetDic['scene2'] = self.readLog(scene=scene2, filename='downflow.log')[0]
        result = {'status': 1, 'scene1': targetDic['scene1'], 'scene2': targetDic['scene2']}
        return result

    def getFpsLog(self, platform, scene):
        targetDic = {}
        targetDic['fps'] = self.readLog(scene=scene, filename='fps.log')[0]
        if platform == Platform.Android:
            targetDic['jank'] = self.readLog(scene=scene, filename='jank.log')[0]
            targetDic['bigjank'] = self.readLog(scene=scene, filename='bigjank.log')[0]
            Stutter_date_dict = self.readLog(scene=scene, filename='Stutter.log')[0]
            for item in Stutter_date_dict:
                item['y'] = round((item['y'] * 100), 2)
            targetDic['Stutter'] = Stutter_date_dict
            result = {'status': 1, 'fps': targetDic['fps'], 'jank': targetDic['jank'], 'bigjank': targetDic['bigjank'],
                      'Stutter': targetDic['Stutter']}
        else:
            result = {'status': 1, 'fps': targetDic['fps'], 'bigjank': targetDic['bigjank'],
                      'Stutter': targetDic['Stutter']}
        return result

    def getFpsLogCompare(self, platform, scene1, scene2):
        targetDic = {}
        targetDic['scene1'] = self.readLog(scene=scene1, filename='fps.log')[0]
        targetDic['scene2'] = self.readLog(scene=scene2, filename='fps.log')[0]
        result = {'status': 1, 'scene1': targetDic['scene1'], 'scene2': targetDic['scene2']}
        return result

    def approximateSize(self, size, a_kilobyte_is_1024_bytes=True):
        '''
        convert a file size to human-readable form.
        Keyword arguments:
        size -- file size in bytes
        a_kilobyte_is_1024_bytes -- if True (default),use multiples of 1024
                                    if False, use multiples of 1000
        Returns: string
        '''

        suffixes = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
                    1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}

        if size < 0:
            raise ValueError('number must be non-negative')

        multiple = 1024 if a_kilobyte_is_1024_bytes else 1000

        for suffix in suffixes[multiple]:
            size /= multiple
            if size < multiple:
                return '{0:.2f} {1}'.format(size, suffix)

    def _setAndroidPerfs(self, scene, corenum):
        """Aggregate APM data for Android"""
        apm_dict = dict()
        cpuAppData = self.readLog(scene=scene, filename=f'cpu_app.log')[1]
        cpuSystemData = self.readLog(scene=scene, filename=f'cpu_sys.log')[1]
        if cpuAppData.__len__() > 0 and cpuSystemData.__len__() > 0:
            cpuAppRate = f'{round(sum(cpuAppData) / len(cpuAppData), 2)}%'
            cpuSystemRate = f'{round(sum(cpuSystemData) / len(cpuSystemData), 2)}%'
        else:
            cpuAppRate, cpuSystemRate = 0, 0

        for i in range(int(corenum)):
            cpuFreqData = self.readLog(scene=scene, filename=f'cpu_core_{i}.log')[1]
            apm_dict['cpuFreq_{}'.format(i)] = cpuFreqData
        gpuData = self.readLog(scene=scene, filename='gpu.log')[1]
        if gpuData.__len__() > 0:
            gpu = f'{round(sum(gpuData) / len(gpuData), 2)}%'
        else:
            gpu = 0
        batteryLevelData = self.readLog(scene=scene, filename=f'battery_level.log')[1]
        batteryTemlData = self.readLog(scene=scene, filename=f'battery_tem.log')[1]
        if batteryLevelData.__len__() > 0 and batteryTemlData.__len__() > 0:
            batteryLevel = f'{batteryLevelData[-1]}%'
            batteryTeml = f'{batteryTemlData[-1]}°C'
            batteryTemlAvg = f'{int(sum(batteryTemlData) / len(batteryTemlData))}°C'
            batteryTemlDataSort = batteryTemlData.copy()
            batteryTemlDataSort.sort()
            batteryTemlMax = f'{batteryTemlDataSort[-1]}°C'
        else:
            batteryLevel, batteryTeml, batteryTemlAvg, batteryTemlMax = 0, 0, 0, 0

        totalPassData = self.readLog(scene=scene, filename=f'mem_total.log')[1]
        totalPassData.sort()
        maxTotalPass = f'{totalPassData[totalPassData.__len__() - 1]}MB'

        if totalPassData.__len__() > 0:
            swapPassData = self.readLog(scene=scene, filename=f'mem_swap.log')[1]
            totalPassAvg = f'{round(sum(totalPassData) / len(totalPassData), 2)}MB'
            swapPassAvg = f'{round(sum(swapPassData) / len(swapPassData), 2)}MB'
        else:
            totalPassAvg, swapPassAvg = 0, 0

        fpsData = self.readLog(scene=scene, filename=f'fps.log')[1]
        jankData = self.readLog(scene=scene, filename=f'jank.log')[1]
        bigjankData = self.readLog(scene=scene, filename=f'bigjank.log')[1]
        # time_date = self.readLog(scene=scene, filename=f'collect_jank_time.log')
        Stutter_date = self.readLog(scene=scene, filename=f'Stutter.log')[1]
        # jank_time_date = time_date[0]
        if Stutter_date.__len__() > 0:

            Stutter = Stutter_date[Stutter_date.__len__() - 1]
            # print(Stutter_date)
            Stutter = "{:.3%}".format(Stutter)
        else:
            Stutter = '0.0%'
        if fpsData.__len__() > 0:
            fpsAvg = f'{round(sum(fpsData[1:]) / (len(fpsData)-1), 2)}HZ/s'
            jankAvg = f'{int(sum(jankData))}'
            bigjankAvg = f'{int(sum(bigjankData))}'
        else:
            fpsAvg, jankAvg, bigjankData = 0, 0, 0

        if os.path.exists(os.path.join(self.report_dir, scene, 'end_net.json')):
            f_pre = open(os.path.join(self.report_dir, scene, 'pre_net.json'))
            f_end = open(os.path.join(self.report_dir, scene, 'end_net.json'))
            json_pre = json.loads(f_pre.read())
            json_end = json.loads(f_end.read())
            send = json_end['send'] - json_pre['send']
            recv = json_end['recv'] - json_pre['recv']
        else:
            send, recv = 0, 0
        flowSend = f'{round(float(send / 1024), 2)}MB'
        flowRecv = f'{round(float(recv / 1024), 2)}MB'
        mem_detail_flag = os.path.exists(os.path.join(self.report_dir, scene, 'mem_java_heap.log'))
        apm_dict['cpuAppRate'] = cpuAppRate
        apm_dict['cpuSystemRate'] = cpuSystemRate
        apm_dict['gpu'] = gpu
        apm_dict['totalPassAvg'] = totalPassAvg
        apm_dict['swapPassAvg'] = swapPassAvg
        apm_dict['fps'] = fpsAvg
        apm_dict['jank'] = jankAvg
        apm_dict['bigjank'] = bigjankAvg
        apm_dict['Stutter'] = Stutter
        apm_dict['maxTotalPass'] = maxTotalPass
        apm_dict['flow_send'] = flowSend
        apm_dict['flow_recv'] = flowRecv
        apm_dict['batteryLevel'] = batteryLevel
        apm_dict['batteryTeml'] = batteryTeml
        apm_dict['batteryTemlMax'] = batteryTemlMax
        apm_dict['batteryTemlAvg'] = batteryTemlAvg
        apm_dict['mem_detail_flag'] = mem_detail_flag

        return apm_dict

    def _setiOSPerfs(self, scene):
        """Aggregate APM data for iOS"""
        cpuAppData = self.readLog(scene=scene, filename=f'cpu_app.log')[1]
        cpuSystemData = self.readLog(scene=scene, filename=f'cpu_sys.log')[1]
        if cpuAppData.__len__() > 0 and cpuSystemData.__len__() > 0:
            cpuAppRate = f'{round(sum(cpuAppData) / len(cpuAppData), 2)}%'
            cpuSystemRate = f'{round(sum(cpuSystemData) / len(cpuSystemData), 2)}%'
        else:
            cpuAppRate, cpuSystemRate = 0, 0
        gpuData = self.readLog(scene=scene, filename='gpu.log')[1]
        if gpuData.__len__() > 0:
            gpu = round(sum(gpuData) / len(gpuData), 2)
        else:
            gpu = 0
        totalPassData = self.readLog(scene=scene, filename='mem_total.log')[1]
        if totalPassData.__len__() > 0:
            totalPassAvg = f'{round(sum(totalPassData) / len(totalPassData), 2)}MB'
        else:
            totalPassAvg = 0

        fpsData = self.readLog(scene=scene, filename='fps.log')[1]
        if fpsData.__len__() > 0:
            fpsAvg = f'{int(sum(fpsData) / len(fpsData))}HZ/s'
        else:
            fpsAvg = 0

        flowSendData = self.readLog(scene=scene, filename='upflow.log')[1]
        flowRecvData = self.readLog(scene=scene, filename='downflow.log')[1]
        if flowSendData.__len__() > 0:
            flowSend = f'{round(float(sum(flowSendData) / 1024), 2)}MB'
            flowRecv = f'{round(float(sum(flowRecvData) / 1024), 2)}MB'
        else:
            flowSend, flowRecv = 0, 0

        batteryTemlData = self.readLog(scene=scene, filename='battery_tem.log')[1]
        batteryCurrentData = self.readLog(scene=scene, filename='battery_current.log')[1]
        batteryVoltageData = self.readLog(scene=scene, filename='battery_voltage.log')[1]
        batteryPowerData = self.readLog(scene=scene, filename='battery_power.log')[1]
        if batteryTemlData.__len__() > 0:
            batteryTeml = int(batteryTemlData[-1])
            batteryCurrent = int(sum(batteryCurrentData) / len(batteryCurrentData))
            batteryVoltage = int(sum(batteryVoltageData) / len(batteryVoltageData))
            batteryPower = int(sum(batteryPowerData) / len(batteryPowerData))
        else:
            batteryTeml, batteryCurrent, batteryVoltage, batteryPower = 0, 0, 0, 0

        apm_dict = dict()
        apm_dict['cpuAppRate'] = cpuAppRate
        apm_dict['cpuSystemRate'] = cpuSystemRate
        apm_dict['gpu'] = gpu
        apm_dict['totalPassAvg'] = totalPassAvg
        apm_dict['nativePassAvg'] = 0
        apm_dict['dalvikPassAvg'] = 0
        apm_dict['fps'] = fpsAvg
        apm_dict['jank'] = 0
        apm_dict['bigjank'] = 0
        apm_dict['Stutter'] = 0
        apm_dict['flow_send'] = flowSend
        apm_dict['flow_recv'] = flowRecv
        apm_dict['batteryTeml'] = batteryTeml
        apm_dict['batteryCurrent'] = batteryCurrent
        apm_dict['batteryVoltage'] = batteryVoltage
        apm_dict['batteryPower'] = batteryPower

        return apm_dict

    # todolist 增加PK模式下的GPU数据的比对
    def _setpkPerfs(self, scene):
        """Aggregate APM data for pk model"""
        cpuAppData1 = self.readLog(scene=scene, filename='cpu_app1.log')[1]
        cpuAppRate1 = f'{round(sum(cpuAppData1) / len(cpuAppData1), 2)}%'
        cpuAppData2 = self.readLog(scene=scene, filename='cpu_app2.log')[1]
        cpuAppRate2 = f'{round(sum(cpuAppData2) / len(cpuAppData2), 2)}%'

        totalPassData1 = self.readLog(scene=scene, filename='mem1.log')[1]
        totalPassAvg1 = f'{round(sum(totalPassData1) / len(totalPassData1), 2)}MB'
        totalPassData2 = self.readLog(scene=scene, filename='mem2.log')[1]
        totalPassAvg2 = f'{round(sum(totalPassData2) / len(totalPassData2), 2)}MB'

        fpsData1 = self.readLog(scene=scene, filename='fps1.log')[1]
        fpsAvg1 = f'{int(sum(fpsData1) / len(fpsData1))}HZ/s'
        fpsData2 = self.readLog(scene=scene, filename='fps2.log')[1]
        fpsAvg2 = f'{int(sum(fpsData2) / len(fpsData2))}HZ/s'

        networkData1 = self.readLog(scene=scene, filename='network1.log')[1]
        network1 = f'{round(float(sum(networkData1) / 1024), 2)}MB'
        networkData2 = self.readLog(scene=scene, filename='network2.log')[1]
        network2 = f'{round(float(sum(networkData2) / 1024), 2)}MB'

        apm_dict = {}
        apm_dict['cpuAppRate1'] = cpuAppRate1
        apm_dict['cpuAppRate2'] = cpuAppRate2
        apm_dict['totalPassAvg1'] = totalPassAvg1
        apm_dict['totalPassAvg2'] = totalPassAvg2
        apm_dict['network1'] = network1
        apm_dict['network2'] = network2
        apm_dict['fpsAvg1'] = fpsAvg1
        apm_dict['fpsAvg2'] = fpsAvg2
        return apm_dict


class Method:

    @classmethod
    def _request(cls, request, object):
        if request.method == 'POST':
            return request.form[object]
        elif request.method == 'GET':
            return request.args[object]
        else:
            raise Exception('request method error')


    @classmethod
    def _setValue(cls, value, default=0):
        try:
            result = value
        except ZeroDivisionError:
            result = default
        except IndexError:
            result = default
        except Exception:
            result = default
        return result

    @classmethod
    def _settings(cls, request):
        content = {}
        content['cpuWarning'] = (0, request.cookies.get('cpuWarning'))[
            request.cookies.get('cpuWarning') not in [None, 'NaN']]
        content['memWarning'] = (0, request.cookies.get('memWarning'))[
            request.cookies.get('memWarning') not in [None, 'NaN']]
        content['fpsWarning'] = (0, request.cookies.get('fpsWarning'))[
            request.cookies.get('fpsWarning') not in [None, 'NaN']]
        content['netdataRecvWarning'] = (0, request.cookies.get('netdataRecvWarning'))[
            request.cookies.get('netdataRecvWarning') not in [None, 'NaN']]
        content['netdataSendWarning'] = (0, request.cookies.get('netdataSendWarning'))[
            request.cookies.get('netdataSendWarning') not in [None, 'NaN']]
        content['betteryWarning'] = (0, request.cookies.get('betteryWarning'))[
            request.cookies.get('betteryWarning') not in [None, 'NaN']]
        content['duration'] = (0, request.cookies.get('duration'))[request.cookies.get('duration') not in [None, 'NaN']]
        content['solox_host'] = ('', request.cookies.get('solox_host'))[
            request.cookies.get('solox_host') not in [None, 'NaN']]
        content['host_switch'] = request.cookies.get('host_switch')
        return content

    @classmethod
    def _index(cls, target: list, index: int, default: any):
        try:
            return target[index]
        except IndexError:
            return default


