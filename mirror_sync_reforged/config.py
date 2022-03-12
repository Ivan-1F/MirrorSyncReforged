from mcdreforged.api.all import *


class Configure(Serializable):
    permission_level = PermissionLevel.PHYSICAL_SERVER_CONTROL_LEVEL
    survival_server_path = '../survival/server'
    mirror_server_path = './server'
    world_names = ['world']
    count_down = 10
