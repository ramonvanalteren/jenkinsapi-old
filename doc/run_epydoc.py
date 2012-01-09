try:
    from epydoc.cli import cli
except ImportError:
    from pkg_resources import require
    require("epydoc>=3.0.1")
    from epydoc.cli import cli
    
cli()