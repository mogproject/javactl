from __future__ import division, print_function, absolute_import, unicode_literals

import os


#
# Path operation
#
def normalize_path(path, base_dir):
    return path if os.path.isabs(path) else os.path.join(base_dir, path)
