import os
import json
import asyncio
import subprocess
import importlib
import requests
from queue_message import QueueMessage


class BaseService:
    def __init__(self, id, queue):
        self.id = id
        self.queue = queue
        self.task = None
        self.msb_dir = f"{os.environ['HOME']}/msb-py"
        self.msb_settings_path = f"{self.msb_dir}/settings.json"

    def printf(self, msg):
        print(msg, flush=True)
        
    # region Default functions
    async def Start(self):
        pass

    async def Stop(self):
        pass

    async def Process(self, message):
        pass

    async def StateUpdate(self, state):
       pass

    async def _send_event(self, message):
        pass

    async def _change_state(self, message):
        pass

    async def get_configuration(self):
        try:
            await self.Debug(f"Calling get_configuration")
            session = requests.session()
            settings = self.get_settings()
            
            if settings["deviceState"]["desired"]["msbConfig"] != None:
                uri = settings["deviceState"]["desired"]["msbConfig"]["uri"]
                #await self.Debug(f"uri: {uri}")
                respose = session.get(uri)
                if respose.status_code == 200:
                    config = respose.json()
                    #await self.Debug("Configuration fetched")
                    return config
                else:
                    await self.ThrowError(f"Error fetching configuration: {respose.status_code}")
       
            return None

        except Exception as ex:
            await self.Debug(f"Error fetching configuration: {ex}") 
    
    def get_settings(self):
        # Check if directory exists
        if os.path.isdir(self.msb_dir) == False:
            os.mkdir(self.msb_dir)

        # Load settings file if exists
        if os.path.exists(self.msb_settings_path):
            with open(self.msb_settings_path) as f:
                settings = json.load(f)

        else:
            self.printf("Creating settings")
            settings = {
                "hubUri": self.base_uri
            }
            self.save_settings(settings)
        
        return settings

    async def save_settings(self, settings):
        try:
            with open(self.msb_settings_path, 'w') as settings_file:
                json.dump(settings, settings_file)
                self.settings = settings

                await self.Debug("Settings saved")
        except Exception as e:
            await self.ThrowError("Failed to save settings")

    async def msb_signed_in(self, args):
        pass
    # endregion

    # region Communication functions
    async def SubmitAction(self, destination, action, message):
        msg = QueueMessage(self.id, destination, action, message)
        asyncio.create_task(self.queue.put(msg))
        await asyncio.sleep(0)

    async def Debug(self, message):
        msg = QueueMessage(self.id, "logger", "_debug", message)
        task = asyncio.create_task(self.queue.put(msg))
        await asyncio.sleep(0)

    async def Warning(self, message):
        msg = QueueMessage(self.id, "logger", "_warning", message)
        task = asyncio.create_task(self.queue.put(msg))
        await asyncio.sleep(0)

    async def ThrowError(self, message, fault_code = None, fault_description = None):
        if isinstance(message,dict):
            if(fault_code != None):
                message["fault_code"] = fault_code
            if(fault_description != None):
                message["fault_description"] = fault_description
                
        msg = QueueMessage(self.id, "logger", "_error", message)
        task = asyncio.create_task(self.queue.put(msg))
        await asyncio.sleep(0)

    async def Track(self, message, description = None):
        if(description != None):
            message["description"] = description
        msg = QueueMessage(self.id, "logger", "_track", message)
        task = asyncio.create_task(self.queue.put(msg))
        await asyncio.sleep(0)

    async def SubmitMessage(self, message):
        msg = QueueMessage(self.id, "com", "_sendEvent", message)
        asyncio.create_task(self.queue.put(msg))
        await asyncio.sleep(0)

    async def StartService(self, service):
        msg = QueueMessage(self.id, "orchestrator", "_start_service", service)
        asyncio.create_task(self.queue.put(msg))
        await asyncio.sleep(0)

    async def StopCustomServices(self):
        msg = QueueMessage(self.id, "orchestrator",
                           "_stop_custom_services", "")
        asyncio.create_task(self.queue.put(msg))
        await asyncio.sleep(0)

    async def StartCustomServices(self):
        msg = QueueMessage(self.id, "msb", "_start_custom_services", "")
        asyncio.create_task(self.queue.put(msg))
        await asyncio.sleep(0)
    # endregion

    # region Private functions
    # package = pip package E.g "azure-iot-device"
    # module = module name E.g "azure.iot.device.aio"
    # name = name of object E.g "IoTHubDeviceClient". If you don't know the name, try dir(importlib.import_module("module name")

    # SAMPLES:
    # IoTHubDeviceClient = self.AddPipPackage("azure-iot-device", "azure.iot.device.aio", "IoTHubDeviceClient")
    # MqttClient = self.AddPipPackage("paho-mqtt", "paho.mqtt.client", "Client")

    # Think of it this way.... MqttClient = self.AddPipPackage("paho-mqtt", "paho.mqtt.client", "Client") ...is equivalent to:
    # pip install paho-mqtt
    # from paho.mqtt.client import Client
    def AddPipPackage(self, package, module, name):
        try:
            try:
                self.printf(f"Importing {module}")
                importlib.import_module(module)
            except Exception as e1:
                self.printf (f"Unable to import module:. \nTrying to install package {package}")

                response = subprocess.run(f"pip3 install {package}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
                if(response.returncode != 0):
                    self.printf (f"Failed to install {package}")
                    raise Exception('InstallPackage', f"Failed to install {package}")
                else:
                     self.printf (f"Successfully installed {package}")
                    
        except Exception as e2:
            self.printf (f"Failed to install {package}")
            raise Exception('InstallPackage', f"Failed to install {package}")

        Package = getattr(importlib.import_module(module), name)
        return Package

    # endregion


class CustomService(BaseService):
    def __init__(self, id, queue, config):
        self.id = id
        self.queue = queue
        self.config = config
        super(CustomService, self).__init__(id, queue)
       
    def GetPropertyValue(self, category, prop):
         ## newDict = dict(filter(lambda elem: elem[0] % 2 == 0, dictOfNames.items()))
        try:
            category = category + "Config"
            values = [config for config in self.config[category] if config['id'] == prop]
            if len(values) > 0:
                return values[0]['value']
            else:
                return "undefined"
        except Exception as e:
                print(e, flush=True)
                return "undefined"
        
    def GetState(self):
        try:
            state = self.GetPropertyValue("general","enabled")
            return state
        except Exception as e:
                print(e, flush=True)
                return "undefined"