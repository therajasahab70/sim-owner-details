#!/bin/bash
echo "🚀 Setting up SIM Checker in Termux..."

# Install everything
pkg update -y && pkg upgrade -y
pkg install python git curl wget -y
pip install requests pandas phonenumbers flask

# Download scripts
curl -O https://raw.githubusercontent.com/your-repo/sim-checker/main/sim_checker.py
curl -O https://raw.githubusercontent.com/your-repo/sim-checker/main/bulk_sim.py

chmod +x *.py
echo "✅ Setup complete! Run: python sim_checker.py"
