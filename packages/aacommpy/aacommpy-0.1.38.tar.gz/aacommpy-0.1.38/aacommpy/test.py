import clr
import os

from aacommpy.settings import AACOMM_SERVER_EXE_PATH, AACOMM_DLL_PATH
from aacommpy.AAComm import CommAPI, Services, Shared, ChannelType, ProductTypes, ConnectionData

# from AAComm import Services
# from AAComm import CommAPI
# from AAComm import Shared

api = CommAPI()

status = CommAPI.StartAACommServer(AACOMM_SERVER_EXE_PATH)

if status != "":
    print(status)
else:
    # Access the static variable IsAACommServerRunning
    is_running = CommAPI.IsAACommServerRunning
    print(f"AACommServer is running: {is_running}")

cData = Services.ConnectionData()
cData.ControllerType = Shared.ProductTypes.AGM800_ID
cData.CommChannelType = Shared.ChannelType.Ethernet
cData.ET_IP_1 = 172
cData.ET_IP_2 = 1
cData.ET_IP_3 = 1
cData.ET_IP_4 = 101
cData.ET_Port = 5000

res = api.Connect(cData)
print(res)
