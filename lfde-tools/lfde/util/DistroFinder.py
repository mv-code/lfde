import subprocess

class DistroFinder:
    def distro_name(self):
        return subprocess.Popen(["lsb_release", "-si"], \
                stdout=subprocess.PIPE).communicate()[0].strip()

