from setuptools import setup, find_packages

setup(
    name="logistics-notifier",
    version="0.1.0",
    description="A library to send notifications for logistics.",
    long_description="A library to handle notifications such as shipment assignments or status changes.",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/logistics-notifier",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
