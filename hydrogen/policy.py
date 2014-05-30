from openstack.common import policy
from common import exceptions
from common import utils
_POLICY_PATH = None
_POLICY_CACHE = {}
ADMIN_CTX_POLICY = 'context_is_admin'

def reset():
    global _POLICY_PATH
    global _POLICY_CACHE
    _POLICY_PATH = None
    _POLICY_CACHE = {}
    policy.reset()

def init():
    global _POLICY_PATH
    global _POLICY_CACHE
    if not _POLICY_PATH:
        #_POLICY_PATH = utils.find_config_file({}, cfg.CONF.policy_file)
        _POLICY_PATH = 'config/policy.json'
        if not _POLICY_PATH:
            raise exceptions.PolicyFileNotFound(path=cfg.CONF.policy_file)
    # pass _set_brain to read_cached_file so that the policy brain
    # is reset only if the file has changed
    return utils.read_cached_file(_POLICY_PATH, _POLICY_CACHE,
                           reload_func=_set_rules)

def _set_rules(data):
    default_rule = 'default'
    #LOG.debug(_("Loading policies from file: %s"), _POLICY_PATH)
    # Ensure backward compatibility with folsom/grizzly convention
    # for extension rules
    policies = policy.Rules.load_json(data, default_rule)
    '''
    for pol in policies.keys():
        if any([pol.startswith(depr_pol) for depr_pol in
                DEPRECATED_POLICY_MAP.keys()]):
            LOG.warn(_("Found deprecated policy rule:%s. Please consider "
                       "upgrading your policy configuration file"), pol)
            pol_name, action = pol.rsplit(':', 1)
            try:
                new_actions = DEPRECATED_ACTION_MAP[action]
                new_policies = DEPRECATED_POLICY_MAP[pol_name]
                # bind new actions and policies together
                for actual_policy in ['_'.join(item) for item in
                                      itertools.product(new_actions,
                                                        new_policies)]:
                    if actual_policy not in policies:
                        # New policy, same rule
                        LOG.info(_("Inserting policy:%(new_policy)s in place "
                                   "of deprecated policy:%(old_policy)s"),
                                 {'new_policy': actual_policy,
                                  'old_policy': pol})
                        policies[actual_policy] = policies[pol]
                # Remove old-style policy
                del policies[pol]
            except KeyError:
                LOG.error(_("Backward compatibility unavailable for "
                            "deprecated policy %s. The policy will "
                            "not be enforced"), pol)
    '''
    policy.set_rules(policies)
    return policies


def _build_match_rule(action, target):
    """Create the rule to match for a given action.

    The policy rule to be matched is built in the following way:
    1) add entries for matching permission on objects
    2) add an entry for the specific action (e.g.: create_network)
    3) add an entry for attributes of a resource for which the action
       is being executed (e.g.: create_network:shared)
    4) add an entry for sub-attributes of a resource for which the
       action is being executed
       (e.g.: create_router:external_gateway_info:network_id)
    """
    match_rule = policy.RuleCheck('rule', action)
    '''
    resource, is_write = get_resource_and_action(action)
    # Attribute-based checks shall not be enforced on GETs
    if is_write:
        # assigning to variable with short name for improving readability
        res_map = attributes.RESOURCE_ATTRIBUTE_MAP
        if resource in res_map:
            for attribute_name in res_map[resource]:
                if _is_attribute_explicitly_set(attribute_name,
                                                res_map[resource],
                                                target):
                    attribute = res_map[resource][attribute_name]
                    if 'enforce_policy' in attribute:
                        attr_rule = policy.RuleCheck('rule', '%s:%s' %
                                                     (action, attribute_name))
                        # Build match entries for sub-attributes, if present
                        validate = attribute.get('validate')
                        if (validate and any([k.startswith('type:dict') and v
                                              for (k, v) in
                                              validate.iteritems()])):
                            attr_rule = policy.AndCheck(
                                [attr_rule, _build_subattr_match_rule(
                                    attribute_name, attribute,
                                    action, target)])
                        match_rule = policy.AndCheck([match_rule, attr_rule])
    '''
    return match_rule


def _prepare_check(context, action, target):
    """Prepare rule, target, and credentials for the policy engine."""
    # Compare with None to distinguish case in which target is {}
    if target is None:
        target = {}
    match_rule = _build_match_rule(action, target)
    credentials = context.to_dict()
    return match_rule, target, credentials

def check(context, action, target, plugin=None, might_not_exist=False):
    """Verifies that the action is valid on the target in this context.

    :param context: neutron context
    :param action: string representing the action to be checked
        this should be colon separated for clarity.
    :param target: dictionary representing the object of the action
        for object creation this should be a dictionary representing the
        location of the object e.g. ``{'project_id': context.project_id}``
    :param plugin: currently unused and deprecated.
        Kept for backward compatibility.
    :param might_not_exist: If True the policy check is skipped (and the
        function returns True) if the specified policy does not exist.
        Defaults to false.

    :return: Returns True if access is permitted else False.
    """
    if might_not_exist and not (policy._rules and action in policy._rules):
        return True
    return policy.check(*(_prepare_check(context, action, target)))

def enforce(context, action, target, plugin=None):
    """Verifies that the action is valid on the target in this context.

    :param context: neutron context
    :param action: string representing the action to be checked
        this should be colon separated for clarity.
    :param target: dictionary representing the object of the action
        for object creation this should be a dictionary representing the
        location of the object e.g. ``{'project_id': context.project_id}``
    :param plugin: currently unused and deprecated.
        Kept for backward compatibility.

    :raises neutron.exceptions.PolicyNotAuthorized: if verification fails.
    """

    rule, target, credentials = _prepare_check(context, action, target)
    result = policy.check(rule, target, credentials, action=action)
    if not result:
        #LOG.debug(_("Failed policy check for '%s'"), action)
        raise exceptions.PolicyNotAuthorized(action=action)
    return result


