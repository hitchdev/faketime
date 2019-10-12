import hitchpylibrarytoolkit
from hitchrun import DIR, expected
from commandlib import CommandError
import hitchbuildpy


PROJECT_NAME = "faketime"

@expected(AssertionError)
@expected(CommandError)
def smoketest():
    """
    Run the code in a virtualenv against date.
    """
    pylibrary = hitchpylibrarytoolkit.project_build(
        PROJECT_NAME, DIR, "3.7.0"
    )
    pylibrary.bin.pip("uninstall", "faketime", "-y").ignore_errors().run()
    pylibrary.bin.pip("install", DIR.project).run()
    output = pylibrary.bin.python(DIR.key / "example.py").run()
    output = pylibrary.bin.python(DIR.key / "example.py").output()
    assert "2050" in output, "output should have contained 2050, instead:\n\n{}".format(output)
    

def deploy(version):
    """
    Deploy to pypi as specified version.
    """
    hitchpylibrarytoolkit.deploy(DIR.project, PROJECT_NAME, version)
