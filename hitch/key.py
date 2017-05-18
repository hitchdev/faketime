from hitchstory import StoryCollection, BaseEngine, StorySchema
from hitchrun import Path
from hitchvm import StandardBox, Vagrant
from pathquery import pathq
import sys
from pexpect import EOF
import hitchrun
from strictyaml import MapPattern, Str, Enum
import hitchvm


KEYPATH = Path(__file__).abspath().dirname()

class Paths(object):
    def __init__(self, keypath):
        from hitchrun import genpath
        self.keypath = keypath
        self.project = keypath.parent
        self.state = genpath.joinpath("state")

        if not self.state.exists():
            self.state.mkdir()


class Engine(BaseEngine):
    def __init__(self, keypath):
        self.path = Paths(keypath)

    schema = StorySchema(
        preconditions={
            "operating system": Enum([
                "macos-sierra", "ubuntu-trusty-64", "macos-elcapitan"]),
            "files": MapPattern(Str(), Str()),
        },
    )

    def set_up(self):
        self.path.example = self.path.project.joinpath("example")
        operating_sys = self.preconditions['operating system']

        if self.path.example.exists():
            self.path.example.rmtree(ignore_errors=True)
        self.path.example.mkdir()

        for filename, content in self.preconditions.get("files", {}).items():
            self.path.example.joinpath(filename).write_text(content)

        recipes = {
            "macos-sierra": hitchvm.recipes.MacPython(),
            "macos-elcapitan": hitchvm.recipes.MacPython(),
            "ubuntu-trusty-64": hitchvm.recipes.AptGet(
                "python-setuptools", "build-essential",
                "python-pip", "python-virtualenv", "python3",
            ),
        }

        box = StandardBox(Path("~/.hitchpkg").expand(), operating_sys, recipes[operating_sys])
        self.vm = Vagrant("faketime", box, self.path.state)
        self.vm = self.vm.synced_with(self.path.project, "/faketime/")

        if not self.vm.snapshot_exists("faketime-{0}-ready".format(operating_sys)):
            self.vm.up()
            self.long_run("sudo pip install commandlib")
            self.vm.take_snapshot("faketime-{0}-ready".format(operating_sys))
            self.vm.halt()

        self.vm.restore_snapshot("faketime-{0}-ready".format(operating_sys))
        self.vm.sync()
        self.run("cd /faketime ; sudo pip install .")

    def long_run(self, cmd):
        self.run(cmd, timeout=600)

    def pause(self):
        import IPython
        IPython.embed()

    def run(self, cmd=None, expect=None, timeout=240):
        self.process = self.vm.cmd(cmd).pexpect()

        if sys.stdout.isatty():
            self.process.logfile = sys.stdout.buffer
        else:
            self.process.logfile = sys.stdout


        if expect is not None:
            self.process.expect(expect, timeout=timeout)
        self.process.expect(EOF, timeout=timeout)
        self.process.close()

    def tear_down(self):
        """Clean out the state directory."""
        if hasattr(self, 'vm'):
            self.vm.halt()


def test(name):
    print(StoryCollection(pathq(KEYPATH).ext("story"), Engine(KEYPATH)).shortcut(name).play().report())


def lint():
    print("placeholder")

def hitch(*args):
    """
    Use 'h hitch --help' to get help on these commands.
    """
    hitchrun.hitch_maintenance(*args)



def clean():
    print("destroy all created vms")