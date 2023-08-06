import os
#this array define all of the folder name contain AAComm.dll file of AAComm nuget package
NET_FRAMEWORK_CHOICES = ['net40', 'net46', 'net48', 'netcoreapp3.1', 'net5.0', 'net6.0','net7.0']
# there will be 2 constants add into this file name "AACOMM_DLL_PATH" and "AACOMM_SERVER_EXE_PATH" when run "aacommpy install" and "aacommpy update"
dll_filename = 'AAComm.dll'
exe_filename = 'AACommServer.exe'
current_dir = os.path.dirname(__file__)
AACOMM_DLL_PATH = os.path.join(current_dir, 'AAComm.dll')
AACOMM_SERVER_EXE_PATH = os.path.join(current_dir, 'AACommServer.exe')