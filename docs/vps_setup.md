# VPS Setup Guide for Credit Report API Service

## System Requirements

### Minimum Hardware Requirements
- CPU: 1 vCPU/Core
- RAM: 2GB
- Storage: 20GB SSD
- Network: 1GB/month bandwidth

### Recommended Hardware Requirements
- CPU: 2 vCPU/Cores
- RAM: 4GB
- Storage: 40GB SSD
- Network: 2GB/month bandwidth

### Operating System
- Ubuntu 20.04 LTS or newer
- Debian 11 or newer

## Initial Server Setup

### Update System Packages
```bash
sudo apt update
sudo apt upgrade -y
```

### Create Non-root User
```bash
sudo adduser deploy
sudo usermod -aG sudo deploy
```

### Configure SSH
```bash
# Edit SSH configuration
sudo nano /etc/ssh/sshd_config

# Set these values
PermitRootLogin no
PasswordAuthentication no
Port 2222  # Change default SSH port

# Restart SSH service
sudo systemctl restart sshd
```

### Configure Firewall (UFW)
```bash
# Install UFW if not present
sudo apt install ufw

# Allow SSH (use your custom port if changed)
sudo ufw allow 2222/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

## Docker Installation

### Install Docker
```bash
# Add Docker's official GPG key
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker packages
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
```

### Verify Docker Installation
```bash
# Test Docker installation
docker --version
docker compose version

# Run test container
docker run hello-world
```

## Security Considerations

### System Security
1. **Regular Updates**
   ```bash
   # Enable automatic security updates
   sudo apt install unattended-upgrades
   sudo dpkg-reconfigure -plow unattended-upgrades
   ```

2. **Install Fail2ban**
   ```bash
   sudo apt install fail2ban
   sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
   sudo systemctl enable fail2ban
   sudo systemctl start fail2ban
   ```

3. **Configure System Limits**
   ```bash
   # Edit system limits
   sudo nano /etc/security/limits.conf

   # Add these lines
   *          soft    nofile      65535
   *          hard    nofile      65535
   ```

### Docker Security
1. **Use Official Images Only**
2. **Regular Security Scans**
   ```bash
   # Install and use Trivy for container scanning
   sudo apt install trivy
   trivy image your-image-name
   ```

3. **Limit Container Resources**
   ```yaml
   # In docker-compose.yml
   services:
     api:
       deploy:
         resources:
           limits:
             cpus: '1.0'
             memory: 1G
           reservations:
             cpus: '0.5'
             memory: 512M
   ```

## Environment Setup

### Application Directory
```bash
# Create application directory
sudo mkdir -p /opt/credit-report-api
sudo chown deploy:deploy /opt/credit-report-api
```

### Environment Variables
```bash
# Create environment file
nano /opt/credit-report-api/.env

# Add required variables
API_PORT=8000
MAX_WORKERS=4
LOG_LEVEL=info
UPLOAD_DIR=/app/credit_reports
OUTPUT_DIR=/app/output_text
```

### SSL/TLS Setup (with Certbot)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com
```

## Deployment

### Clone Repository
```bash
cd /opt/credit-report-api
git clone https://github.com/your-username/credit_report_to_json.git .
```

### Deploy with Docker Compose
```bash
# Build and start containers
docker compose -f docker-compose.prod.yml up -d

# Check logs
docker compose logs -f
```

## Monitoring Setup

### Application Logging
The application uses a comprehensive logging system with JSON formatting for structured logs:

```bash
# Create logs directory
sudo mkdir -p /opt/credit-report-api/logs
sudo chown deploy:deploy /opt/credit-report-api/logs

# Install Python dependencies for logging
pip install python-json-logger psutil

# Logs are stored in:
/opt/credit-report-api/logs/api.log      # API request/response logs
/opt/credit-report-api/logs/monitoring.log # System metrics logs
```

### System Metrics Monitoring
The application includes built-in system metrics monitoring:
- CPU usage
- Memory utilization
- Disk usage
- Request/response timing
- Error tracking

### Resource Monitoring
```bash
# View application metrics
tail -f /opt/credit-report-api/logs/monitoring.log

# Install additional monitoring tools
sudo apt install -y htop iotop nethogs

# Monitor system resources
htop
```

### Docker Container Monitoring
```bash
# View container stats
docker stats

# View container logs
docker compose logs -f
```

### Setting Up Maintenance Tasks
```bash
# Make maintenance script executable
chmod +x /opt/credit-report-api/app/maintenance.py

# Set up cron job for maintenance script
sudo crontab -e

# Add this line to run maintenance at 2 AM daily
0 2 * * * cd /opt/credit-report-api && ./app/maintenance.py
```

## Backup Procedures

### Automated Backup System
The application includes an automated backup system that handles:
- Log files rotation and archival
- Credit report files backup
- Output text files backup
- Automatic cleanup of old backups

```bash
# Backup directories
/opt/credit-report-api/backups/  # Contains timestamped backup archives
/opt/credit-report-api/logs/     # Contains rotated log files

# Backup features:
- Daily automated backups at 2 AM
- 7-day retention policy
- Automatic log rotation when files exceed 100MB
- Compressed archives with timestamps
```

### Manual Backup Commands
```bash
# Trigger manual backup
cd /opt/credit-report-api
python3 -c "from app.utils.backup import BackupManager; BackupManager().create_backup()"

# View backup logs
tail -f /opt/credit-report-api/logs/api.log | grep "backup"

# List backup files
ls -lh /opt/credit-report-api/backups/
```

### Additional Backups
```bash
# Backup environment files
cp /opt/credit-report-api/.env /opt/credit-report-api/backups/env-$(date +%Y%m%d)
```

## Troubleshooting

### Common Commands
```bash
# Check container status
docker compose ps

# View container logs
docker compose logs -f

# Restart services
docker compose restart

# Check system resources
df -h  # Disk space
free -m  # Memory usage
top  # CPU usage
```

### Log Locations
- API logs: `/opt/credit-report-api/logs/api.log`
- Monitoring logs: `/opt/credit-report-api/logs/monitoring.log`
- System logs: `/var/log/syslog`
- Docker logs: `docker compose logs`
- Backup logs: Included in api.log

## Maintenance Procedures

### Regular Maintenance Tasks
1. Update system packages weekly
2. Monitor disk usage and system metrics (automated)
3. Rotate logs (automated)
4. Create and verify backups (automated)
5. Clean up old backups (automated)
6. Update SSL certificates
7. Review security policies and logs
8. Check error logs for patterns

### Scaling Considerations
- Monitor resource usage
- Adjust container limits as needed
- Consider load balancing for high traffic
- Implement caching if required
