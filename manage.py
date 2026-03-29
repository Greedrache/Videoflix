#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# --- Windows RQ Monkey Patch ---
if sys.platform == "win32":
    import multiprocessing
    _orig_get_context = multiprocessing.get_context
    def _patched_get_context(method=None):
        if method == "fork":
            method = "spawn"
        return _orig_get_context(method)
    multiprocessing.get_context = _patched_get_context
# -------------------------------

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
