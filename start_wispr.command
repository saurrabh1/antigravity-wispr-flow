#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
# Use the python executable from the virtual environment explicitly and catch errors
./venv/bin/python3 main.py
if [ $? -ne 0 ]; then
    echo "------------------------------------------------"
    echo "ERROR: The app crashed. See errors above."
    echo "------------------------------------------------"
    # Keep window open if it crashes
    read -p "Press Enter to close..."
fi
