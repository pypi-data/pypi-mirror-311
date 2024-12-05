from __future__ import annotations

import logging
import shutil

from vortex.workspace import Workspace

logger = logging.getLogger("vortex")


def clean(workspace: Workspace) -> int:
    cloned_apps = workspace.listapps()
    if cloned_apps:
        host_dirs = set(workspace.path / app.host for app in cloned_apps)
        print(host_dirs)
        with workspace.exclusive_lock():
            for host_dir in host_dirs:
                shutil.rmtree(host_dir)
                logger.debug(f"Deleted directory '{host_dir}'")
            workspace.update_vscode_settings()
    logger.info("Workspace cleaned")
    return 0
