import logging

log = logging.getLogger('magicfunc')
handler = logging.StreamHandler()
log.addHandler(handler)
log.setLevel(logging.WARNING)
