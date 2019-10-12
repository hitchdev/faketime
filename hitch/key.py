PROJECT_NAME = "faketime"


def deploy(version):
    """
    Deploy to pypi as specified version.
    """
    hitchpylibrarytoolkit.deploy(DIR.project, PROJECT_NAME, version)
