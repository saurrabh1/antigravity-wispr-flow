from setuptools import setup

APP = ['main.py']
DATA_FILES = ['config.json']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['rumps', 'pynput', 'pyaudio', 'whisper', 'AppKit', 'Quartz', 'numpy', 'torch'],
    'plist': {
        'LSUIElement': True, # Agent app (no dock icon)
    }
}

setup(
    app=APP,
    name='SKDon',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
