# -*- coding: utf-8 -*-
import subprocess
import traceback

from cloudinit import CloudConfig, util

frequency = CloudConfig.per_instance


def yum_install(packages):
    cmd = ["yum", "--quiet", "--assumeyes", "install"]
    cmd.extend(packages)
    cmd.append("--enablerepo=epel")
    subprocess.check_call(cmd, env={"http_proxy": "http://proxy01.globoi.com:3128", "https_proxy": ""})


def handle(_name, cfg, _cloud, log, args):
    pkglist = util.get_cfg_option_list_or_str(cfg, "packages", [])

    if pkglist:
        try:
            yum_install(pkglist)
        except subprocess.CalledProcessError:
            log.warn("Failed to install yum packages: %s" % pkglist)
            log.debug(traceback.format_exc())
            raise

    return True
