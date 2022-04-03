from mcdreforged.plugin.plugin_event import LiteralEvent

QBM_PID = 'quick_backup_multi'

TRIGGER_BACKUP_EVENT = LiteralEvent('{}.trigger_backup'.format(QBM_PID))  # <- source, comment
