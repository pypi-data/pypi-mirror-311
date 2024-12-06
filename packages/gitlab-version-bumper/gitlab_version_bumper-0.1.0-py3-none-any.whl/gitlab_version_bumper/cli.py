"""
This python function is intended to be used in the CI chain
to bump the prerelase info for production pipeline
Return to stdout: The new version string or a error message
"""

import os
import subprocess
import semver

def get_current_version():
    """Returns the determined version based on previous tags and current branch"""
    commit_tag = os.environ.get("CI_COMMIT_TAG")
    is_protected = os.environ.get("CI_COMMIT_REF_PROTECTED") == "true"
    build_id = os.environ.get("CI_PIPELINE_IID")
    prerelease_id = "beta" if os.environ.get("CI_COMMIT_BRANCH") == "main" else "alpha"

    if commit_tag and is_protected:
        return commit_tag

    published_tag = semver.Version.parse(
        subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"])
        .decode("ascii")
        .strip()
    )
    current_tag = semver.Version.parse(
        subprocess.check_output(["git", "describe", "--tags"]).decode("ascii").strip()
    )

    current_version = published_tag.replace(prerelease=prerelease_id, build=build_id)

    # We are NOT on a tagged commit if published and current tag differ -> bump patch
    if published_tag.compare(current_tag):
        current_version = current_version.bump_patch()

    # double check, that we end up with a valid version
    return semver.Version.parse(str(current_version))


def main():
    """Main entry point"""
    # return the current version to stdout
    print(get_current_version())


if __name__ == "__main__":
    main()
