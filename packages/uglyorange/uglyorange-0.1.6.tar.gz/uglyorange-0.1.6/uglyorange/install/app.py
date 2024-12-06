from .types import AbstractInstaller
import codefast as cf


class AppInstaller(AbstractInstaller):
    def __init__(self, apps: list):
        self.apps = apps

    def update(self):
        cf.shell("apt update -y", print_str=True)

    def install(self):
        self.update()
        cf.info(f"Installing {self.apps}")
        for app in self.apps:
            try:
                cf.shell(f"apt install -y {app}", print_str=True)
            except Exception as e:
                cf.error(f"Failed to install {app}: {e}")


def app_install():
    apps = [
        "vim", "neofetch", "curl", "emacs", "fish", "docker.io", "docker-compose",
        "net-tools", "vnstat", "tree", "htop", "ttyd", "sysstat", "ufw", "lsb-release",
        "snapd", "cron", "unzip", "p7zip-full", "bmon"
    ]
    AppInstaller(apps).install()
