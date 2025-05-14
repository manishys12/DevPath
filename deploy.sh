#!/bin/bash
# Deployment script for EdgeRoute application

# Exit on error
set -e

# Configuration
APP_NAME="edgeroute"
DEPLOY_DIR="/var/www/$APP_NAME"
VENV_DIR="$DEPLOY_DIR/venv"
GIT_REPO="https://github.com/manish12ys/EdgeRoute.git"
BRANCH="main"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting deployment of $APP_NAME...${NC}"

# Check if deployment directory exists
if [ ! -d "$DEPLOY_DIR" ]; then
    echo -e "${GREEN}Creating deployment directory...${NC}"
    mkdir -p "$DEPLOY_DIR"
    git clone "$GIT_REPO" "$DEPLOY_DIR"
    cd "$DEPLOY_DIR"
else
    echo -e "${GREEN}Updating existing deployment...${NC}"
    cd "$DEPLOY_DIR"
    git fetch
    git reset --hard origin/$BRANCH
fi

# Create or update virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment and install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

# Set up environment variables
echo -e "${GREEN}Setting up environment variables...${NC}"
if [ ! -f "$DEPLOY_DIR/.env" ]; then
    echo -e "${RED}Warning: .env file not found. Creating a sample one.${NC}"
    cp "$DEPLOY_DIR/.env.example" "$DEPLOY_DIR/.env"
    echo -e "${RED}Please update the .env file with your configuration.${NC}"
fi

# Run database migrations
echo -e "${GREEN}Running database migrations...${NC}"
flask db upgrade

# Restart services
echo -e "${GREEN}Restarting services...${NC}"
if [ -f "/etc/systemd/system/$APP_NAME.service" ]; then
    sudo systemctl restart "$APP_NAME"
else
    echo -e "${RED}Warning: Systemd service not found. Please set it up manually.${NC}"
fi

echo -e "${GREEN}Deployment completed successfully!${NC}"
