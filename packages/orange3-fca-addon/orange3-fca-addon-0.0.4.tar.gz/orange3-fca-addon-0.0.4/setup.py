from setuptools import setup, find_packages


setup(
    packages=find_packages(),
    package_data={
        'orangecontrib.orange3_fca.widgets': ['icons/*'],
    },
    # @todo: `entry-points` defined outside of `pyproject.toml` would be ignored.
    # To prevent this warning, you can list `entry-points` under `dynamic` or alternatively
    # remove the `[project]` table from your file and rely entirely on other means of
    # configuration.
    entry_points={
        'orange3.addon': [
            'orange3-fca-addon = orangecontrib.orange3_fca'
        ],
        # Entry point used to specify packages containing tutorials accessible
        # from welcome screen. Tutorials are saved Orange Workflows (.ows files).
        'orange.widgets.tutorials': [
            # Syntax: any_text = path.to.package.containing.tutorials
        ],
        # Entry point used to specify packages containing widgets.
        'orange.widgets': [
            'orange3-fca-addon = orangecontrib.orange3_fca.widgets',
        ],
    },
)
