from setuptools import setup, find_packages

setup(
    name="AdvAssist",               # Name of the package
    version="0.1.0",             # Version number
    author="Adan Saikia",          # Replace with your name
    description="A Python package for automation tasks",  # Short description
    packages=find_packages(),    # Automatically finds the 'AdvAssist' package
    install_requires=[          # Add external dependencies here
        'keyboard==0.13.5',
        'protobuf==5.29.1',
        'PyAutoGUI==0.9.54',
        'pygame==2.6.1',
        'pyttsx3==2.98',
        'pywhatkit==5.4',
        'Requests==2.32.3',
        'selenium==4.27.1',
        'setuptools==75.6.0',
        'webdriver_manager==4.0.2',
        'wikipedia==1.4.0',
        'yt_dlp==2024.12.13'
    ],
    python_requires=">=3.9",     # Minimum Python version requirement
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
)