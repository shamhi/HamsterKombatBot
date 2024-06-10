#!/bin/bash

install_python() {
    echo "Select the Python version to install:"
    echo "1) Python 3.9"
    echo "2) Python 3.10"
    echo "3) Python 3.11"
    echo "4) Python 3.12"
    read -p "Enter the number of your choice: " choice

    case $choice in
        1) version="3.9" ;;
        2) version="3.10" ;;
        3) version="3.11" ;;
        4) version="3.12" ;;
        *) echo "Invalid choice"; exit 1 ;;
    esac

    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python$version python$version-venv python$version-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y https://repo.ius.io/ius-release-el$(rpm -E %{rhel}).rpm
        sudo yum install -y python$version python$version-venv python$version-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python$version python$version-venv python$version-pip
    else
        echo "Package manager not supported. Please install Python manually."
        exit 1
    fi
}

if ! command -v python3 &> /dev/null; then
    install_python
fi

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Copying .env-example to .env..."
cp .env-example .env

echo "Please edit the .env file to add your API_ID and API_HASH."
read -p "Press any key to continue..."