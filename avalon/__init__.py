""" Avalon is a simulation framework.

    It might be useful for:

    - better logic testing of product;
    - creating reallife-like data to test statistic software;
    - spam data for develompent in real time;

    :copyright: 2013 by Kirill Klenov.
    :license: BSD, see LICENSE for more details.
"""

try:
    from .core import story, Actor
    from .engine import Avalon, Script, avalon
except ImportError:
    pass

# Module information
# ==================
__version__ = '0.1.0'
__project__ = 'avalon'
__author__ = "horneds <horneds@gmail.com>"
__license__ = "BSD"
