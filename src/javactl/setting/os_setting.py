from __future__ import division, print_function, absolute_import, unicode_literals

import six
from mog_commons.functional import oget
from mog_commons.case_class import CaseClass


class OSSetting(CaseClass):
    def __init__(self, user=None, env=None):
        # constraints
        assert user is not None, 'os.user is required'
        assert isinstance(user, six.string_types), 'os.user must be a string'
        assert env is None or isinstance(env, dict), 'os.env must be a dict'

        d = dict((k, str(v)) for k, v in oget(env, {}).items())
        CaseClass.__init__(self, ('user', user), ('env', d))
