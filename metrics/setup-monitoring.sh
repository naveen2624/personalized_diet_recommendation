#!/bin/bash

##############################################################################
# Diet Plan API - Monitoring Stack Setup Script
# File Structure: Root level setup for existing project
##############################################################################

set -e  # Exit on error

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    printf "${BLUE}║${NC} %-60s ${BLUE}║${NC}\n" "$1"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${CYAN}ℹ${NC} $1"
}

# Banner
show_banner() {
    clear
    echo -e "${BLUE}"
    cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          Diet Plan API - Monitoring Stack Setup             ║
║                                                              ║
║              Prometheus + Grafana Monitoring                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    local all_good=true
    
    # Check Docker
    if command -v docker &> /dev/null; then
        print_success "Docker installed: $(docker --version | cut -d' ' -f3 | cut -d',' -f1)"
    else
        print_error "Docker is not installed"
        echo "  Install from: https://www.docker.com/products/docker-desktop"
        all_good=false
    fi
    
    # Check Docker Compose
    if command -v docker-compose &> /dev/null; then
        print_success "Docker Compose installed: $(docker-compose --version | cut -d' ' -f4 | cut -d',' -f1)"
    else
        print_error "Docker Compose is not installed"
        all_good=false
    fi
    
    # Check if Docker daemon is running
    if docker info &> /dev/null; then
        print_success "Docker daemon is running"
    else
        print_error "Docker daemon is not running"
        echo "  Please start Docker Desktop"
        all_good=false
    fi
    
    # Check ports
    if lsof -Pi :9090 -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port 9090 is already in use (needed for Prometheus)"
    else
        print_success "Port 9090 is available"
    fi
    
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port 3000 is already in use (needed for Grafana)"
    else
        print_success "Port 3000 is available"
    fi
    
    if [ "$all_good" = false ]; then
        echo ""
        print_error "Please fix the issues above and run again"
        exit 1
    fi
}

# Create directory structure
create_directories() {
    print_header "Creating Directory Structure"
    
    # Create Grafana directories
    mkdir -p grafana/provisioning/datasources
    print_success "Created grafana/provisioning/datasources/"
    
    mkdir -p grafana/provisioning/dashboards
    print_success "Created grafana/provisioning/dashboards/"
    
    mkdir -p grafana/dashboards
    print_success "Created grafana/dashboards/"
}

# Create Prometheus configuration
create_prometheus_config() {
    print_header "Creating Prometheus Configuration"
    
    # Detect OS
    OS_TYPE=$(uname -s)
    
    if [[ "$OS_TYPE" == "Linux" ]]; then
        print_warning "Linux detected"
        print_info "You may need to replace 'host.docker.internal' with your machine's IP"
        print_info "Find your IP: ip addr show | grep inet"
    fi
    
    cat > prometheus.yml << 'EOF'
# prometheus.yml - Prometheus Configuration for Diet Plan API

global:
  scrape_interval: 15s       # How often to scrape targets
  evaluation_interval: 15s   # How often to evaluate rules
  scrape_timeout: 10s        # Timeout for scraping
  
  external_labels:
    monitor: 'diet-api-monitor'
    environment: 'production'

# Scrape configurations
scrape_configs:
  # Diet Plan API
  - job_name: 'diet-plan-api'
    
    metrics_path: '/metrics'
    scheme: http
    scrape_interval: 15s
    scrape_timeout: 10s
    
    static_configs:
      - targets: 
          # Mac/Windows Docker Desktop: use host.docker.internal
          - 'host.docker.internal:6060'
          # Linux: replace with your machine's IP address
          # - '192.168.1.100:6060'
        
        labels:
          service: 'diet-plan-api'
          application: 'flask-backend'
          environment: 'production'
          team: 'backend'

  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
        labels:
          service: 'prometheus'
          environment: 'monitoring'
EOF
    
    print_success "Created prometheus.yml"
}

# Create Grafana datasource provisioning
create_grafana_datasource() {
    print_header "Creating Grafana Datasource Configuration"
    
    cat > grafana/provisioning/datasources/prometheus.yml << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
    jsonData:
      timeInterval: "15s"
      queryTimeout: "60s"
      httpMethod: POST
    version: 1
EOF
    
    print_success "Created grafana/provisioning/datasources/prometheus.yml"
}

# Create Grafana dashboard provisioning
create_grafana_dashboard_config() {
    print_header "Creating Grafana Dashboard Configuration"
    
    cat > grafana/provisioning/dashboards/dashboard.yml << 'EOF'
apiVersion: 1

providers:
  - name: 'Diet Plan API Dashboards'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: true
EOF
    
    print_success "Created grafana/provisioning/dashboards/dashboard.yml"
}

# Check for dashboard JSON
check_dashboard_json() {
    print_header "Checking Dashboard JSON"
    
    if [ -f "grafana/dashboards/diet-api-dashboard.json" ]; then
        local size=$(wc -c < "grafana/dashboards/diet-api-dashboard.json")
        if [ $size -gt 1000 ]; then
            print_success "Dashboard JSON found (${size} bytes)"
        else
            print_warning "Dashboard JSON exists but seems too small (${size} bytes)"
            print_info "Make sure it contains the complete dashboard configuration"
        fi
    else
        print_warning "Dashboard JSON not found"
        print_info "Please place diet-api-dashboard.json in: grafana/dashboards/"
        print_info "The dashboard will auto-load once you add the file"
    fi
}

# Check Docker Compose file
check_docker_compose() {
    print_header "Checking Docker Compose File"
    
    if [ -f "docker-compose.monitoring.yml" ]; then
        print_success "docker-compose.monitoring.yml found"
    else
        print_warning "docker-compose.monitoring.yml not found"
        print_info "Creating docker-compose.monitoring.yml..."
        
        cat > docker-compose.monitoring.yml << 'EOF'
version: "3.8"

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: diet-api-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--web.console.libraries=/usr/share/prometheus/console_libraries"
      - "--web.console.templates=/usr/share/prometheus/consoles"
      - "--storage.tsdb.retention.time=15d"
    restart: unless-stopped
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: diet-api-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
    restart: unless-stopped
    networks:
      - monitoring
    depends_on:
      - prometheus

networks:
  monitoring:
    driver: bridge

volumes:
  prometheus_data:
  grafana_data:
EOF
        print_success "Created docker-compose.monitoring.yml"
    fi
}

# Display directory structure
show_structure() {
    print_header "Directory Structure"
    
    echo -e "${CYAN}Project Root${NC}"
    echo "├── frontend/                 (your Next.js app)"
    echo "├── backend/"
    echo "│   └── api.py               (Flask API with metrics)"
    echo "├── infra/terraform/         (your infrastructure)"
    echo "├── ${GREEN}docker-compose.monitoring.yml${NC}  ✓"
    echo "├── ${GREEN}prometheus.yml${NC}                  ✓"
    echo "├── ${GREEN}grafana/${NC}"
    echo "│   ├── ${GREEN}provisioning/${NC}"
    echo "│   │   ├── ${GREEN}datasources/${NC}"
    echo "│   │   │   └── ${GREEN}prometheus.yml${NC}      ✓"
    echo "│   │   └── ${GREEN}dashboards/${NC}"
    echo "│   │       └── ${GREEN}dashboard.yml${NC}       ✓"
    echo "│   └── ${GREEN}dashboards/${NC}"
    if [ -f "grafana/dashboards/diet-api-dashboard.json" ]; then
        echo "│       └── ${GREEN}diet-api-dashboard.json${NC} ✓"
    else
        echo "│       └── ${YELLOW}diet-api-dashboard.json${NC} (add this)"
    fi
    echo "└── setup-monitoring.sh      (this script)"
    echo ""
}

# Pull Docker images
pull_images() {
    print_header "Pulling Docker Images"
    
    print_info "Pulling Prometheus..."
    docker pull prom/prometheus:latest
    
    print_info "Pulling Grafana..."
    docker pull grafana/grafana:latest
    
    print_success "Images pulled successfully"
}

# Start monitoring stack
start_monitoring() {
    print_header "Starting Monitoring Stack"
    
    print_info "Starting containers..."
    docker-compose -f docker-compose.monitoring.yml up -d
    
    print_success "Containers started!"
    
    # Wait for services
    print_info "Waiting for services to initialize (15 seconds)..."
    for i in {15..1}; do
        echo -ne "\r  ${CYAN}⏳${NC} $i seconds remaining..."
        sleep 1
    done
    echo -e "\r  ${GREEN}✓${NC} Services ready!          "
}

# Check container status
check_status() {
    print_header "Container Status"
    
    docker-compose -f docker-compose.monitoring.yml ps
}

# Test connections
test_connections() {
    print_header "Testing Connections"
    
    # Test Prometheus
    if curl -s http://localhost:9090/-/healthy > /dev/null; then
        print_success "Prometheus is responding on http://localhost:9090"
    else
        print_warning "Prometheus health check failed"
    fi
    
    # Test Grafana
    if curl -s http://localhost:3000/api/health > /dev/null; then
        print_success "Grafana is responding on http://localhost:3000"
    else
        print_warning "Grafana health check failed (may still be starting)"
    fi
    
    # Test Flask API
    if curl -s http://localhost:6060/api/health > /dev/null; then
        print_success "Flask API is responding on http://localhost:6060"
    else
        print_warning "Flask API is not running (start it with: cd backend && python api.py)"
    fi
}

# Display access information
show_access_info() {
    print_header "Access Information"
    
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${CYAN}📊 Grafana Dashboard${NC}"
    echo -e "   URL:      ${YELLOW}http://localhost:3000${NC}"
    echo -e "   Username: ${YELLOW}admin${NC}"
    echo -e "   Password: ${YELLOW}admin123${NC}"
    echo ""
    echo -e "${CYAN}📈 Prometheus${NC}"
    echo -e "   URL:      ${YELLOW}http://localhost:9090${NC}"
    echo -e "   Targets:  ${YELLOW}http://localhost:9090/targets${NC}"
    echo ""
    echo -e "${CYAN}🔧 Flask API${NC}"
    echo -e "   Metrics:  ${YELLOW}http://localhost:6060/metrics${NC}"
    echo -e "   Health:   ${YELLOW}http://localhost:6060/api/health${NC}"
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Show next steps
show_next_steps() {
    print_header "Next Steps"
    
    echo ""
    echo -e "${YELLOW}1.${NC} ${CYAN}Start your Flask API${NC} (if not running):"
    echo "   cd backend && python api.py"
    echo ""
    
    echo -e "${YELLOW}2.${NC} ${CYAN}Verify Prometheus is scraping${NC}:"
    echo "   Open: http://localhost:9090/targets"
    echo "   Target 'diet-plan-api' should show ${GREEN}UP${NC}"
    echo ""
    
    echo -e "${YELLOW}3.${NC} ${CYAN}Access Grafana Dashboard${NC}:"
    echo "   Open: http://localhost:3000"
    echo "   Login: admin / admin123"
    echo "   Dashboard will auto-load"
    echo ""
    
    echo -e "${YELLOW}4.${NC} ${CYAN}Generate test data${NC}:"
    echo "   python test-metrics.py"
    echo ""
    
    if [ ! -f "grafana/dashboards/diet-api-dashboard.json" ]; then
        echo -e "${YELLOW}5.${NC} ${CYAN}Add Dashboard JSON${NC}:"
        echo "   Save the dashboard JSON to:"
        echo "   grafana/dashboards/diet-api-dashboard.json"
        echo ""
    fi
}

# Show useful commands
show_commands() {
    print_header "Useful Commands"
    
    echo ""
    echo -e "${GREEN}View logs:${NC}"
    echo "  docker-compose -f docker-compose.monitoring.yml logs -f"
    echo ""
    echo -e "${GREEN}Stop monitoring:${NC}"
    echo "  docker-compose -f docker-compose.monitoring.yml down"
    echo ""
    echo -e "${GREEN}Restart services:${NC}"
    echo "  docker-compose -f docker-compose.monitoring.yml restart"
    echo ""
    echo -e "${GREEN}Check metrics:${NC}"
    echo "  curl http://localhost:6060/metrics | grep diet_plan"
    echo ""
    echo -e "${GREEN}Remove all data (including volumes):${NC}"
    echo "  docker-compose -f docker-compose.monitoring.yml down -v"
    echo ""
}

##############################################################################
# Main Script Execution
##############################################################################

show_banner

# Check prerequisites
check_prerequisites

# Create directories
create_directories

# Create configuration files
create_prometheus_config
create_grafana_datasource
create_grafana_dashboard_config

# Check for required files
check_docker_compose
check_dashboard_json

# Show structure
show_structure

# Ask to start
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
read -p "$(echo -e ${CYAN}Do you want to start the monitoring stack now? \(y/n\):${NC} )" -n 1 -r
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    pull_images
    start_monitoring
    check_status
    test_connections
    show_access_info
else
    echo ""
    print_info "Setup complete. Start later with:"
    echo "  docker-compose -f docker-compose.monitoring.yml up -d"
    echo ""
fi

# Show next steps and commands
show_next_steps
show_commands

# Final message
print_header "Setup Complete!"

echo ""
echo -e "${GREEN}✓ Monitoring stack is configured and ready!${NC}"
echo ""
echo -e "${CYAN}Need help?${NC} Check the logs:"
echo "  docker-compose -f docker-compose.monitoring.yml logs -f"
echo ""

exit 0