#!/bin/bash
# ==============================================
# 🚀 Project Setup Script
# Author: Jun Official
# ==============================================

# Colors
GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
CYAN="\e[36m"
RESET="\e[0m"

clear
echo -e "${CYAN}"
echo "=============================================="
echo "        🚀 Welcome to the Setup Wizard 🚀       "
echo "=============================================="
echo -e "${RESET}"

# Step 0: Update & install dependencies
echo -e "${YELLOW}[*] Updating and upgrading Termux packages...${RESET}"
pkg update -y && pkg upgrade -y

echo -e "${YELLOW}[*] Installing required packages...${RESET}"
pkg install -y python python-pip git curl wget nano

# Step 1: Check requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}[ERROR] requirements.txt not found!${RESET}"
    exit 1
fi

# Step 2: Installing Python dependencies
echo -e "${YELLOW}[*] Installing Python dependencies from requirements.txt...${RESET}"
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to install Python dependencies.${RESET}"
    exit 1
fi

# Step 3: Success message
echo -e "${GREEN}[OK] All dependencies installed successfully!${RESET}"

# Loading effect
echo -ne "${CYAN}>>> Preparing to launch start.sh"
for i in {1..3}; do
    echo -ne "."
    sleep 1
done
echo -e "${RESET}\n"

# Step 4: Run start.sh
if [ -f "start.sh" ]; then
    echo -e "${GREEN}[INFO] Starting the project...${RESET}"
    bash start.sh
else
    echo -e "${RED}[ERROR] start.sh not found!${RESET}"
    exit 1
fi