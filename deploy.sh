#!/bin/bash

# Cellmarker Annotation App Deployment Script
# Port: 6052

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
CONDA_ENV="cellmarkerAnno"
MAMBA_PATH="/home/hzl/miniforge3/bin/mamba"
PORT="6052"
APP_FILE="app.py"
REQUIREMENTS_FILE="requirements.txt"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Cellmarker Annotation App Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Function to install dependencies
install_dependencies() {
    echo -e "${YELLOW}Checking dependencies...${NC}"
    ${MAMBA_PATH} run -n ${CONDA_ENV} pip install -r ${REQUIREMENTS_FILE} --quiet
    echo -e "${GREEN}Dependencies installed successfully.${NC}"
}

# Check if we need to install dependencies
if [ "$1" == "--install" ]; then
    install_dependencies
    exit 0
fi

# Check if dependencies are already installed
echo -e "${YELLOW}Checking if dependencies are installed...${NC}"
if ! ${MAMBA_PATH} run -n ${CONDA_ENV} python -c "import streamlit, pandas, openpyxl" 2>/dev/null; then
    echo -e "${YELLOW}Dependencies not found. Installing...${NC}"
    install_dependencies
else
    echo -e "${GREEN}All dependencies are already installed.${NC}"
fi

echo ""
echo -e "${GREEN}Starting Cellmarker Annotation App on port ${PORT}...${NC}"
echo ""
echo -e "${YELLOW}App URL: http://localhost:${PORT}${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Run the app
${MAMBA_PATH} run -n ${CONDA_ENV} streamlit run ${APP_FILE} --server.port ${PORT}
