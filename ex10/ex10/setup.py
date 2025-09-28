from setuptools import find_packages, setup

package_name = "ex10"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="capybariana",
    maintainer_email="novikova.polina.p@gmail.com",
    description="Text to cmd_vel node for turtlesim",
    license="MIT",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": ["text_to_cmd_vel = ex10.text_to_cmd_vel:main"],
    },
)
