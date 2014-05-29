from neutron.openstack.common import policy
_POLICY_PATH = None
_POLICY_CACHE = {}
ADMIN_CTX_POLICY = 'context_is_admin'
def init():
    global _POLICY_PATH
    global _POLICY_CACHE
    if not _POLICY_PATH:
        _POLICY_PATH = utils.find_config_file({}, cfg.CONF.policy_file)
        if not _POLICY_PATH:
            raise exceptions.PolicyFileNotFound(path=cfg.CONF.policy_file)
    # pass _set_brain to read_cached_file so that the policy brain
    # is reset only if the file has changed
    utils.read_cached_file(_POLICY_PATH, _POLICY_CACHE,
                           reload_func=_set_rules)
