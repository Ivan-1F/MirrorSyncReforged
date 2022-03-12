import os
import shutil
import time
from typing import Any

from mcdreforged.api.all import *

from mirror_sync_reforged.config import Configure

PREFIX = '!!mirror'

server_inst: PluginServerInterface
metadata: Metadata
config: Configure

abort_sync = False


def tr(key: str, *args, **kwargs):
    return server_inst.tr('{}.{}'.format(metadata.id, key), *args, **kwargs)


def command_run(message: Any, hover: Any, command: str) -> RTextBase:
    fancy_text = message.copy() if isinstance(message, RTextBase) else RText(message)
    return fancy_text.set_hover_text(hover).set_click_event(RAction.run_command, command)


def show_help_message(source: CommandSource):
    source.reply(tr('help_message', name=metadata.name, version=metadata.version, prefix=PREFIX))
    pass


# From Quick Back Multi
def copy_worlds(src: str, dst: str):
    for world in config.world_names:
        src_path = os.path.join(src, world)
        dst_path = os.path.join(dst, world)

        while os.path.islink(src_path):
            server_inst.logger.info('copying {} -> {} (symbolic link)'.format(src_path, dst_path))
            dst_dir = os.path.dirname(dst_path)
            if not os.path.isdir(dst_dir):
                os.makedirs(dst_dir)
            link_path = os.readlink(src_path)
            os.symlink(link_path, dst_path)
            src_path = link_path if os.path.isabs(link_path) else os.path.normpath(
                os.path.join(os.path.dirname(src_path), link_path))
            dst_path = os.path.join(dst, os.path.relpath(src_path, src))

        server_inst.logger.info('copying {} -> {}'.format(src_path, dst_path))
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
        elif os.path.isfile(src_path):
            dst_dir = os.path.dirname(dst_path)
            if not os.path.isdir(dst_dir):
                os.makedirs(dst_dir)
            shutil.copy(src_path, dst_path)
        else:
            server_inst.logger.warning(
                '{} does not exist while copying ({} -> {})'.format(src_path, src_path, dst_path))


# From Quick Back Multi
def remove_worlds(folder: str):
    for world in config.world_names:
        target_path = os.path.join(folder, world)

        while os.path.islink(target_path):
            link_path = os.readlink(target_path)
            os.unlink(target_path)
            target_path = link_path if os.path.isabs(link_path) else os.path.normpath(
                os.path.join(os.path.dirname(target_path), link_path))

        if os.path.isdir(target_path):
            shutil.rmtree(target_path)
        elif os.path.isfile(target_path):
            os.remove(target_path)
        else:
            ServerInterface.get_instance().logger.warning('{} does not exist while removing'.format(target_path))


def check_paths(source: CommandSource) -> bool:
    success = True

    # check if a path is existed and is a directory
    def check_dir(path: str) -> bool:
        if not os.path.exists(path):
            source.get_server().say(tr('sync.path_checking.not_exist', path))
            return False
        if not os.path.isdir(path):
            source.get_server().say(tr('sync.path_checking.not_a_dir', path))
            return False
        return True

    def check_server_path(path: str):
        if not check_dir(path):
            return False
        for world in config.world_names:
            world_path = os.path.join(path, world)
            if not check_dir(world_path):
                return False
        return True

    success = success and check_server_path(config.survival_server_path)
    success = success and check_server_path(config.mirror_server_path)

    return success


def sync(source: CommandSource):
    global abort_sync
    abort_sync = False
    if not check_paths(source):
        return
    source.get_server().say(tr('sync.echo_action'))
    source.get_server().say(
        command_run(tr('sync.confirm_hint', PREFIX), tr('sync.confirm_hover'),
                    '{0} confirm'.format(PREFIX))
        + ', '
        + command_run(tr('sync.abort_hint', PREFIX), tr('sync.abort_hover'),
                      '{0} abort'.format(PREFIX))
    )


@new_thread('MSR')
def _sync(source: CommandSource):
    source.get_server().say(tr('sync.countdown.intro', config.count_down))
    for countdown in range(1, config.count_down):
        source.get_server().say(command_run(
            tr('sync.countdown.text', config.count_down - countdown),
            tr('sync.countdown.hover'),
            '{} abort'.format(PREFIX)
        ))
        for i in range(10):
            time.sleep(0.1)
            global abort_sync
            if abort_sync:
                source.get_server().say(tr('sync.aborted'))
                return

    source.get_server().stop()
    server_inst.logger.info('Wait for server to stop')
    source.get_server().wait_for_start()

    server_inst.logger.info('Deleting world')
    remove_worlds(config.mirror_server_path)

    server_inst.logger.info('Copying survival worlds to the mirror server')
    copy_worlds(config.survival_server_path, config.mirror_server_path)
    server_inst.logger.info('Sync done, starting the server')
    source.get_server().start()


def confirm(source: CommandSource):
    _sync(source)


def abort(source: CommandSource):
    global abort_sync
    abort_sync = True
    source.get_server().say(tr('sync.abort'))


def register_command(server: PluginServerInterface):
    def get_literal_node(literal):
        return (
            Literal(literal)
                .requires(lambda src: src.has_permission(config.permission_level), lambda: tr('permission_denied'))
        )

    server.register_command(
        Literal(PREFIX)
            .runs(show_help_message)
            .then(get_literal_node('sync').runs(sync))
            .then(get_literal_node('confirm').runs(confirm))
            .then(get_literal_node('abort').runs(abort))
    )


def load_config():
    global config
    config = server_inst.load_config_simple(target_class=Configure)


def on_load(server: PluginServerInterface, old):
    global server_inst, metadata
    server_inst = server
    metadata = server.get_self_metadata()
    load_config()
    register_command(server)
