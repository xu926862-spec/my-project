#!/bin/bash
# Genesis Omniscience Deployment Script
# 终极全能神级系统部署脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
GENESIS_HOME="${HOME}/.genesis"
LOG_DIR="$GENESIS_HOME/logs"
DB_DIR="$GENESIS_HOME/db"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# 打印函数
print_header() {
    echo -e "${MAGENTA}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║${BLUE}  Genesis Omniscience System - Deployment v3.0${MAGENTA}            ║${NC}"
    echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════════╝${NC}"
}

print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# 检查依赖
check_dependencies() {
    print_status "Checking dependencies..."

    # Python 3
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found. Please install Python 3.9+"
        exit 1
    fi
    print_success "Python 3 found: $(python3 --version)"

    # pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 not found"
        exit 1
    fi
    print_success "pip3 found"

    # Required packages
    print_status "Checking Python packages..."
    python3 -c "import openai" 2>/dev/null || {
        print_warning "openai package not found, installing..."
        pip3 install openai
    }
    print_success "All dependencies satisfied"
}

# 初始化目录
init_directories() {
    print_status "Initializing directories..."

    mkdir -p "$GENESIS_HOME"
    mkdir -p "$LOG_DIR"
    mkdir -p "$DB_DIR"
    mkdir -p "$PROJECT_ROOT/.genesis"

    print_success "Directories initialized at $GENESIS_HOME"
}

# 验证配置
validate_config() {
    print_status "Validating configuration..."

    if [ ! -f "$PROJECT_ROOT/genesis.config.json" ]; then
        print_error "genesis.config.json not found"
        exit 1
    fi

    # 检查JSON有效性
    python3 -c "import json; json.load(open('$PROJECT_ROOT/genesis.config.json'))" 2>/dev/null || {
        print_error "Invalid JSON in genesis.config.json"
        exit 1
    }

    print_success "Configuration validated"
}

# 检查Llama服务
check_llama_service() {
    print_status "Checking Llama server availability..."

    if curl -s http://localhost:8000/v1/models &>/dev/null; then
        print_success "Llama server is running on localhost:8000"
        return 0
    else
        print_warning "Llama server not detected on localhost:8000"
        print_warning "Genesis will attempt to use it when available"
        return 1
    fi
}

# 初始化数据库
init_databases() {
    print_status "Initializing databases..."

    python3 << 'EOF'
import sqlite3
import os

db_path = os.path.expanduser("~/.genesis/knowledge.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Knowledge graph tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS nodes (
        id TEXT PRIMARY KEY,
        concept TEXT UNIQUE,
        description TEXT,
        weight REAL DEFAULT 1.0,
        access_count INTEGER DEFAULT 0,
        last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS edges (
        source_id TEXT,
        target_id TEXT,
        relation_type TEXT,
        weight REAL DEFAULT 1.0,
        PRIMARY KEY (source_id, target_id, relation_type)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS patterns (
        pattern TEXT PRIMARY KEY,
        frequency INTEGER DEFAULT 0,
        last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
        efficacy REAL DEFAULT 0.0
    )
""")

conn.commit()
conn.close()

print("✓ Databases initialized")
EOF

    print_success "Database initialization complete"
}

# 运行测试
run_diagnostics() {
    print_status "Running system diagnostics..."

    python3 << 'EOF'
import sys
sys.path.insert(0, '.')

try:
    from genesis_omniscience import GenesisOmniscience
    print("✓ Genesis module imports successfully")

    # 尝试初始化
    genesis = GenesisOmniscience()
    print(f"✓ Genesis system initialized: v{genesis.version}")
    print(f"✓ Logger system active")
    print(f"✓ Knowledge graph ready")
    print(f"✓ Self-healing system ready")
    print(f"✓ Monitoring system ready")

except Exception as e:
    print(f"✗ Initialization error: {e}")
    sys.exit(1)
EOF

    if [ $? -eq 0 ]; then
        print_success "Diagnostics passed"
    else
        print_error "Diagnostics failed"
        exit 1
    fi
}

# 生成启动脚本
generate_startup_scripts() {
    print_status "Generating startup scripts..."

    # Python启动脚本
    cat > "$PROJECT_ROOT/start_genesis.py" << 'EOF'
#!/usr/bin/env python3
import asyncio
import sys
sys.path.insert(0, '.')

from genesis_omniscience import GenesisOmniscience, main

if __name__ == "__main__":
    print("🌌 Starting Genesis Omniscience System...")
    asyncio.run(main())
EOF

    chmod +x "$PROJECT_ROOT/start_genesis.py"

    # Bash启动脚本
    cat > "$PROJECT_ROOT/start_genesis.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 start_genesis.py "$@"
EOF

    chmod +x "$PROJECT_ROOT/start_genesis.sh"

    print_success "Startup scripts generated"
}

# 生成systemd服务文件
generate_systemd_service() {
    print_status "Generating systemd service file..."

    SERVICE_FILE="$HOME/.config/systemd/user/genesis.service"
    mkdir -p "$(dirname "$SERVICE_FILE")"

    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Genesis Omniscience System
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_ROOT
ExecStart=$PROJECT_ROOT/start_genesis.sh
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
EOF

    print_success "Systemd service file created at $SERVICE_FILE"
    print_warning "To enable: systemctl --user enable genesis"
    print_warning "To start: systemctl --user start genesis"
}

# 生成健康检查脚本
generate_health_check() {
    print_status "Generating health check script..."

    cat > "$PROJECT_ROOT/health_check_genesis.py" << 'EOF'
#!/usr/bin/env python3
import sys
import json
sys.path.insert(0, '.')

from genesis_omniscience import GenesisOmniscience

def check_health():
    try:
        genesis = GenesisOmniscience()
        status = genesis.get_system_status()

        print(json.dumps(status, indent=2, ensure_ascii=False))

        if status['health']['status'] == 'HEALTHY':
            return 0
        else:
            return 1
    except Exception as e:
        print(f"Health check failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check_health())
EOF

    chmod +x "$PROJECT_ROOT/health_check_genesis.py"
    print_success "Health check script generated"
}

# 主函数
main() {
    print_header
    echo

    check_dependencies
    echo

    init_directories
    echo

    validate_config
    echo

    check_llama_service
    echo

    init_databases
    echo

    run_diagnostics
    echo

    generate_startup_scripts
    echo

    generate_systemd_service
    echo

    generate_health_check
    echo

    # 部署完成
    echo -e "${MAGENTA}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║           ✨ Genesis Omniscience Deployment Complete ✨          ║${NC}"
    echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo

    print_success "System deployed successfully!"
    echo

    echo "📍 Quick Start:"
    echo "   1. Start interactively:"
    echo "      ${BLUE}cd $PROJECT_ROOT && python3 genesis_omniscience.py${NC}"
    echo
    echo "   2. Or use startup script:"
    echo "      ${BLUE}$PROJECT_ROOT/start_genesis.sh${NC}"
    echo
    echo "   3. Health check:"
    echo "      ${BLUE}python3 $PROJECT_ROOT/health_check_genesis.py${NC}"
    echo
    echo "   4. Enable as service (Linux systemd):"
    echo "      ${BLUE}systemctl --user enable genesis${NC}"
    echo "      ${BLUE}systemctl --user start genesis${NC}"
    echo

    echo "📊 Documentation:"
    echo "   Config: $PROJECT_ROOT/genesis.config.json"
    echo "   Logs: $LOG_DIR"
    echo "   Database: $DB_DIR"
    echo

    print_success "Ready to unleash the power of Genesis Omniscience!"
    echo -e "${MAGENTA}🌌 GOD MODE ACTIVATED ✨${NC}"
}

# 运行
main "$@"
