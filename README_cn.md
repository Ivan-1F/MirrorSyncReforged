MirrorSyncReforged
-----

[English](./README.md) | **中文**

一个用于同步生存服存档至镜像服的插件

由 [MirrorSync](https://github.com/Ivan-1F/MCDReforged-Plugins/tree/master/MirrorSync) 重置

把它放在镜像服务器里

## 配置

配置文件：`config/mirror_sync_reforged/config.json`

### `permission_level`

默认值：`4`

使用命令的最低权限等级

### `survival_server_path`

默认值：`../survival/server`

生存服务器的路径（源）

### `mirror_server_path`

默认值：`./server`

镜像服务器的路径（目标）

### `world_names`

默认值：`['world']`

需要同步的世界列表

对于原版服务端：`["world"]`

对于 Spigot 服务端： `['world', 'world_nether', 'world_the_end']`

### `count_down`

默认值：`10`

执行 `!!mirror confirm` 后的倒数时间

### `backup`

默认值：`false`

如果启用，此插件将依赖 [QuickBackupM](https://github.com/TISUnion/QuickBackupM)

在同步存档前将使用 [QuickBackupM](https://github.com/TISUnion/QuickBackupM) 进行备份

### `ignore_session_lock`

如果启用，拷贝世界时将忽略 `session.lock` 文件

### 例子

文件结构：

```
root/
    survival_mcdr/
        plugins/
        server/
            world/
            minecraft_server.jar
        ...
    mirror_mcdr/
        config/
            mirror_sync_reforged/
                config.json
        plugins/
            mirror_sync_reforged.mcdr
        server/
            world/
            minecraft_server.jar
        ...
    ...
```

则 `survival_server_path` 应该为 `../survival_mcdr/server`，`mirror_server_path` 应该为 `./server`

## 命令

`!!mirror`: 显示帮助信息

`!!mirror sync`: 同步存档

`!!mirror confirm`: 再次确认是否进行同步

`!!mirror abort`: 在任何时候键入此指令可中断同步

`!!mirror reload`: 重新加载配置文件

