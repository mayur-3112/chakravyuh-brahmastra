#!/bin/bash
# Chakravyuh-Brahmastra - Kali Linux Installation Script
# Optimized for Kali's pre-installed security tools

set -e

echo "🔱 Chakravyuh-Brahmastra - Kali Linux Setup"
echo "=============================================="
echo "Date: $(date)"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Kali
if [ ! -f /etc/os-release ] || ! grep -q "Kali" /etc/os-release; then
    echo -e "${YELLOW}⚠️  Warning: This script is optimized for Kali Linux${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update package lists
echo -e "${GREEN}📦 Updating package lists...${NC}"
sudo apt-get update -qq

# Check and install Python 3 (usually pre-installed on Kali)
echo -e "${GREEN}🐍 Verifying Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "Installing Python 3..."
    sudo apt-get install -y python3 python3-pip python3-venv
else
    python3 --version
fi

# Install system dependencies (most are pre-installed on Kali)
echo -e "${GREEN}📚 Installing system dependencies...${NC}"
sudo apt-get install -y \
    nmap \
    redis-server \
    python3-dev \
    libpcap-dev \
    build-essential \
    git \
    curl

# Verify Kali-specific tools
echo -e "${GREEN}✓ Verifying Kali tools...${NC}"
command -v nmap >/dev/null 2>&1 && echo "  ✓ Nmap: $(nmap --version | head -n1)"
command -v masscan >/dev/null 2>&1 && echo "  ✓ Masscan available" || echo "  ⚠ Masscan not found (optional)"

# Create Python virtual environment
echo -e "${GREEN}🔧 Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo -e "${GREEN}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel -q

# Install Python dependencies
echo -e "${GREEN}📦 Installing Python packages...${NC}"
pip install -r requirements.txt

# Start Redis
echo -e "${GREEN}🚀 Configuring Redis...${NC}"
sudo systemctl start redis-server
sudo systemctl enable redis-server
redis-cli ping > /dev/null 2>&1 && echo "  ✓ Redis is running"

# Create project directories
echo -e "${GREEN}📁 Creating project structure...${NC}"
mkdir -p logs reports data/scans data/intel

# Create .env if doesn't exist
if [ ! -f .env ]; then
    echo -e "${GREEN}📝 Creating .env configuration...${NC}"
    cat > .env << 'EOF'
# Chakravyuh-Brahmastra Configuration (Kali Linux)
APP_NAME=Chakravyuh-Brahmastra
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=CHANGE_THIS_IN_PRODUCTION
SCAN_TIMEOUT=300
MAX_CONCURRENT_SCANS=5
DEFAULT_PORT_RANGE=1-1000
REDIS_HOST=localhost
REDIS_PORT=6379
LOG_LEVEL=INFO
LOG_FORMAT=json
EOF
    echo "  ✓ Created .env (remember to customize!)"
fi

# Set permissions
chmod +x scripts/*.sh

echo ""
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo ""
echo "Next Steps:"
echo "  1. Activate environment:    ${YELLOW}source venv/bin/activate${NC}"
echo "  2. Edit configuration:      ${YELLOW}nano .env${NC}"
echo "  3. Run tests:               ${YELLOW}pytest tests/ -v${NC}"
echo "  4. Start API server:        ${YELLOW}uvicorn api.app:app --reload${NC}"
echo ""
echo "🔱 [translate:Jai Shree Ram!] May your scans be swift and your defenses impenetrable."
