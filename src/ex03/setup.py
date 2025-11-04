from setuptools import find_packages, setup

package_name = 'ex03'

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/turtle_tf2_demo.launch.py"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="capybariana",
    maintainer_email="novikova.polina.p@gmail.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "turtle_tf2_broadcaster = ex03.turtle_tf2_broadcaster:main",
            "turtle_tf2_broadcaster2 = ex03.turtle_tf2_broadcaster2:main",
            "turtle_tf2_listener_delay = ex03.turtle_tf2_listener_delay:main",
            "spawn_turtle = ex03.spawn_turtle:main",
        ],
    },
)
