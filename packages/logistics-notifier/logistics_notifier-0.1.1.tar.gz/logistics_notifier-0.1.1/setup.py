from setuptools import setup, find_packages

setup(
    name="logistics-notifier",
    version="0.1.1",
    install_requires=["schedule"],
    description="A library to send notifications for logistics.",
    long_description="A library to handle notifications such as shipment assignments or status changes.",
    author="Paras Sunny",
    author_email="your_email@example.com",
    url="https://github.com/psunny25/logistics-notifier",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
