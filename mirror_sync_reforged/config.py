from typing import List

from mcdreforged.api.all import *


class Configure(Serializable):
    permission_level: int = PermissionLevel.PHYSICAL_SERVER_CONTROL_LEVEL
    survival_server_path: str = '../survival/server'
    mirror_server_path: str = './server'
    world_names: List[str] = ['world']
    count_down: int = 10
    backup: bool = False
