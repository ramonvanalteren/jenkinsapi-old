import os, sys

try:
    from epydoc.cli import cli
except ImportError:
    from pkg_resources import require
    require("epydoc>=3.0.1")
    from epydoc.cli import cli
    
DOC_DIR, _ = os.path.split( os.path.abspath( __file__ ) )
PROJECT_DIR, _ = os.path.split( DOC_DIR )

sys.path.insert( 0, PROJECT_DIR )
    
cli()