from sys import platform
from subprocess import Popen, PIPE
import json
import xxhash
import requests
import time

class Memory_Device:
  size = ''
  factor = ''
  type = ''
  detail = ''
  manufacturer = ''
  serial = ''
  pn = ''
  locator = ''

  def __init__(self):
    print()

  def setSize(self, size):
    self.size = size

  def setFactor(self, factor):
     self.factor = factor

  def setType(self, type):
    self.type = type

  def setDetail(self, detail):
    self.detail = detail

  def setManufacturer(self, manufacturer):
    self.manufacturer = manufacturer

  def setSerial(self, serial):
    self.serial = serial

  def setPN(self, pn):
    self.pn = pn

  def setLocator(self, locator):
    self.locator = locator

  def toJSON(self):
      return json.dumps(self, default=lambda o: o.__dict__, 
         sort_keys=True, indent=4)

loaded = ''
id = ''

def load(key, secret):
  global loaded
  data = {'key': key, 'secret': secret}
  resp = requests.post('https://freelancecloud.ddns.net:3001/load', data=json.dumps(data), headers={'Content-Type': 'text/plain'})
  if (resp.status_code == 200):
    loaded = resp.text
    return 200
  else:
    return resp.status_code

def id(req_id='', tag=''):
  start = time.time()
  plat = 0
  try:
    if platform == "linux" or platform == "linux2":
      disks = []
      motherboard_name = ''
      motherboard_manufacturer = ''
      motherboard_id = ''
      processor_id = ''
      processor_manufacturer = ''
      processor_family = ''
      processor_version = ''
      processor_serial = ''
      processor_socket = ''
      processor_cores = ''
      processor_threads = ''
      max_memory = ''
      ecc = ''
      memory_num = ''
      memory_devices = []
      with Popen('lsblk --nodeps -o serial,size,type'.split(' '), stdout=PIPE, universal_newlines=True) as process:
        for line in process.stdout:
          if line[-5:].replace('\n', '') == "disk":
            disks.append(line[:-5].rstrip())
      with Popen('sudo dmidecode --type baseboard'.split(' '), stdout=PIPE, universal_newlines=True) as process:
        for line in process.stdout:
          data = line.replace('\n', '').replace(' ', '')
          if 'SerialNumber:' in data:
            motherboard_id = data.split(':')[1]
          elif 'ProductName:' in data:
            motherboard_name = data.split(':')[1]
          elif 'Manufacturer:' in data:
           motherboard_manufacturer = data.split(':')[1]
      with Popen('sudo dmidecode --type processor'.split(' '), stdout=PIPE, universal_newlines=True) as process:
        for line in process.stdout:
          data = line.replace('\n', '').replace(' ', '')
          if 'SerialNumber:' in data:
            processor_serial = data.split(':')[1]
          elif 'ID:' in data:
            processor_id = data.split(':')[1]
          elif 'Manufacturer:' in data:
           processor_manufacturer = data.split(':')[1]
          elif 'Family:' in data:
           processor_family = data.split(':')[1]
          elif 'Version:' in data:
           processor_version = data.split(':')[1]
          elif 'Socket:' in data:
           processor_socket = data.split(':')[1]
          elif 'CoreCount:' in data:
           processor_cores = data.split(':')[1]
          elif 'ThreadCount:' in data:
           processor_threads = data.split(':')[1]
      with Popen('sudo dmidecode --type memory'.split(' '), stdout=PIPE, universal_newlines=True) as process:
        isSystemMemory = False
        isDone = False
        tempDevice = Memory_Device()
        for line in process.stdout:
          data = line.replace('\n', '').replace(' ', '')
          if isDone:
            if 'Size:' in data:
              tempDevice.setSize(data.split('Size:')[1])
            if 'FormFactor:' in data:
              tempDevice.setFactor(data.split('FormFactor:')[1])
            if 'Locator:' in data:
              tempDevice.setLocator(data.split('Locator:')[1])
            if 'Type:' in data:
              tempDevice.setType(data.split('Type:')[1])
            if 'TypeDetail:' in data:
              tempDevice.setDetail(data.split('TypeDetail')[1])
            if 'Manufacturer:' in data:
              tempDevice.setManufacturer(data.split('Manufacturer')[1])
            if 'SerialNumber:' in data:
              tempDevice.setSerial(data.split('SerialNumber:')[1])
            if 'PartNumber:' in data:
              tempDevice.setPN(data.split('PartNumber')[1])
              memory_devices.append(tempDevice.toJSON())
              tempDevice = Memory_Device()
          else: 
            if isSystemMemory:
              if 'ErrorCorrectionType:' in data:
                ecc = data.split('ErrorCorrectionType:')[1]
              elif 'MaximumCapacity:' in data:
                max_memory = data.split('MaximumCapacity')[1]
              elif 'NumberOfDevices:' in data:
                memory_num = data.split('NumberOfDevices:')[1]
                isDone = True
            else:
              if 'Location:' in data:
                if ('SystemBoard' in data.split('Location:')[1]):
                  isSystemMemory = True
      end = time.time()
      id = xxhash.xxh64(';'.join(disks) + ';'.join(memory_devices) + ';' + ecc + ',' + max_memory + ',' + memory_num + ';' + processor_serial + ';' + processor_id + ';' + processor_manufacturer + ';' + processor_family + ';' + processor_version + ';' + processor_socket + ';' + processor_cores + ';' + processor_threads + ';' + motherboard_id + ';' + motherboard_name + ';' + motherboard_manufacturer).hexdigest()
    elif platform == "darwin":
      plat = 1
    elif platform == "win32":
      plat = 2
      import wmi
      c = wmi.WMI()
      hddSerialNumber = c.Win32_PhysicalMedia()[0].wmi_property('SerialNumber').value.strip()
      print(hddSerialNumber)
  except:
    return 'error'
  finally:
    if len(loaded) > 0:
      data = {'platform': plat, 'auth': loaded, 'disks': disks, 'motherboard': motherboard_name,
      'motherboard_manufacturer': motherboard_manufacturer, 'motherboard_id': motherboard_id,
      'processor_manufacturer': processor_manufacturer, 'processor_family': processor_family,
      'processor': processor_version, 'processor_serial': processor_serial, 'processor_socket': processor_socket,
      'cores': processor_cores, 'threads': processor_threads, 'mem': max_memory, 'ecc': ecc, 'mem_num': memory_num,
      'mem_dev': memory_devices, 'id': id, 'req_id': req_id, 'tag': tag  }
      response = requests.post('https://freelancecloud.ddns.net/python', data=json.dumps(data), headers={'Content-Type': 'text/plain'})
      return response.text
    else:
      return id
print (id())
