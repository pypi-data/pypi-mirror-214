categories = [
    {"from": "AAComm", "name": "ComAPI", "enable": True},
    {"from": "AAComm", "name": "CommAPIWrapper", "enable": False}, #example of no import
]
SharedCategories = [
    {"from": "AAComm.Shared", "name": "ChannelType", "enable": True},
    {"from": "AAComm.Shared", "name": "ConnectResult", "enable": True},
]
Servicescategories = [
    {"from": "AAComm.Services", "name": "ConnectionData", "enable": True},
]
Extensionscategories = [
    {"from":"AAComm.Extensions", "name":"AACommDownloadFW","enable": True},
    {"from":"AAComm.Extensions", "name":"AACommDownloadUP","enable": True},
]
categories.extend(SharedCategories)
categories.extend(Servicescategories)
categories.extend(Extensionscategories)