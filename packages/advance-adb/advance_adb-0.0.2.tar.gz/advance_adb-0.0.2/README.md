AdvanceADB

AdvanceADB is a Python library that provides advanced tools and utilities for managing and interacting with Android devices using the Android Debug Bridge (ADB). The library includes functionalities for app management, file operations, device analytics, WhatsApp automation, and more.

Installation

To install the library, use pip:

pip install advance_adb

Features

Core Functionalities

    1.	Device Management:
    •	Start, stop, and restart the ADB server.
    •	Query connected devices.
    •	Get device-specific information like Android version, model, manufacturer, etc.
    2.	App Management:
    •	Install, uninstall, and clear app data.
    •	Launch and stop apps.
    •	Check app permissions and manage them.
    3.	File Operations:
    •	Transfer files between the device and the local system.
    •	List, rename, delete, and copy files or directories on the device.
    4.	Analytics:
    •	Retrieve and analyze call and SMS logs.
    •	Analyze screen time to identify the most used apps.
    5.	Miscellaneous:
    •	Capture screenshots and screen recordings.
    •	Retrieve device battery status and screen properties.
    •	Open URLs on the device.
    6.	Utilities:
    •	Backup and restore media files and apps.
    •	Manual app debloating by uninstalling unused apps.
    7.	WhatsApp Automation:
    •	Send single or bulk WhatsApp messages.
    •	Process CSV files for bulk messaging.

Usage

Initialize Modules

Each feature is encapsulated in its module. Initialize them as follows:

from advanceadb.adb import Adb
from advanceadb.files import files
from advanceadb.app import app
from advanceadb.analytics import Analytics
from advanceadb.misc import Misc
from advanceadb.whatsapp import whatsapp
from advanceadb.utilities import utils

# Example: Initialize ADB

adb = Adb(device_id='your_device_id')

Example: Sending a WhatsApp Message

from advanceadb.whatsapp import whatsapp

# Initialize WhatsApp automation

wa = whatsapp(device_id='your_device_id')

# Send a message to a single number

wa.send_msg('+1234567890', 'Hello from AdvanceADB!')

# Send bulk messages from a CSV file

wa.send_bulk_msg('contacts_and_messages.csv')

Example: Backup Files

from advanceadb.utilities import utils

# Initialize utilities

utility = utils(device_id='your_device_id')

# Backup all media files

utility.backup()

Version

Current version: 0.0.1

Contribution

Feel free to contribute to this project by submitting issues or pull requests on the project’s GitHub repository.