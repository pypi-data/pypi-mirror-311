"""
A Python API client and database driver to interact with Honu replicas. The Honu
database is a scalable geographic distributed data store that uses smart anti-entropy
replication to maintain consistency across multiple replicas. The HonuDB is intended
to store documents and vectors for AI/ML workloads.
"""

##########################################################################
## Module Info
##########################################################################

# Import the version number at the top level
from .version import get_version, __version_info__


##########################################################################
## Package Version
##########################################################################

__version__ = get_version(short=True)
