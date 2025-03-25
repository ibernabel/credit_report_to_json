# Credit Report to JSON API

A FastAPI service that converts PDF credit reports into structured JSON data. This service provides a simple REST API endpoint for uploading credit report PDFs and receiving parsed, structured data in return.

## Features

- PDF credit report processing
- Structured JSON output with credit report data
- RESTful API interface with Swagger documentation
- Docker support for easy deployment
- Automatic file cleanup after processing
- Health check endpoint for monitoring
- Comprehensive logging and monitoring system
- Automated backup and maintenance
- System metrics tracking

## Installation

### Local Development

1. System Dependencies:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3.9 python3.9-dev build-essential libmupdf-dev swig

# macOS
brew install mupdf swig
```

2. Python Dependencies:

```bash
# Create and activate virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

3. Start the development server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Installation

1. Requirements:

- Docker
- Docker Compose

2. Quick Start:

```bash
# Build and start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

## API Usage

### Endpoints

#### POST /api/v1/credit-report

Upload and process a credit report PDF file.

```bash
curl -X POST "http://localhost:8000/api/v1/credit-report" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@credit_report.pdf"
```

Response:

```json
{
  "credit_score": 750,
  "personal_info": {
    "name": "John Doe",
    "address": "123 Main St"
  },
  "accounts": [
    {
      "type": "Credit Card",
      "status": "Current",
      "balance": 1500
    }
  ]
}
```

#### GET /health

Health check endpoint to verify service status.

```bash
curl "http://localhost:8000/health"
```

Response:

```json
{
  "status": "healthy"
}
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Deployment

### Production Deployment

1. Build the production image:

```bash
docker build -t credit-report-api:latest .
```

2. Run the container:

```bash
docker run -d \
  --name credit-report-api \
  -p 8000:8000 \
  -v /path/to/credit_reports:/app/credit_reports \
  -v /path/to/output_text:/app/output_text \
  credit-report-api:latest
```

### Security Considerations

- Use HTTPS in production
- Implement rate limiting
- Set up proper file access permissions
- Regular security updates
- Comprehensive system monitoring and logging
- Automated security maintenance

### Volume Management

The service uses two volume mounts:

- `/app/credit_reports`: Temporary storage for uploaded PDFs
- `/app/output_text`: Temporary storage for extracted text

Both directories are automatically cleaned up after processing.

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|-----------|
| DEBUG | Enable debug mode | 0 | No |
| MAX_WORKERS | Number of Uvicorn workers | 4 | No |
| PYTHONPATH | Python path configuration | /app | Yes |
| PYTHONUNBUFFERED | Python output buffering | 1 | No |
| PYTHONDONTWRITEBYTECODE | Prevent Python from writing pyc files | 1 | No |
| LOG_LEVEL | Logging level (info/debug/warning/error) | info | No |
| MAX_LOG_SIZE_MB | Maximum log file size before rotation | 100 | No |
| BACKUP_RETENTION_DAYS | Number of days to keep backups | 7 | No |

## Monitoring and Maintenance

### Logging System

The service includes a comprehensive logging system with:
- Structured JSON logs for better parsing
- Request/response logging with timing information
- System metrics monitoring (CPU, memory, disk usage)
- Error tracking and reporting
- Automatic log rotation

Log files are stored in:
- `/app/logs/api.log`: API requests and application logs
- `/app/logs/monitoring.log`: System metrics and performance data

### Automated Maintenance

The service includes automated maintenance features:
- Daily backups at 2 AM
- Log rotation when files exceed configured size
- Automatic cleanup of old backups (configurable retention)
- System metrics collection and monitoring
- Health check monitoring

### Backup System

Automated backup system that handles:
- Log files rotation and archival
- Credit report files backup
- Output text files backup
- Environment configuration backup
- Automatic cleanup of old backups

Backup files are stored in `/app/backups/` with timestamp-based naming.

For detailed monitoring and maintenance setup, see [VPS Setup Guide](docs/vps_setup.md).

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Code Style

The project follows PEP 8 guidelines. Install and run flake8 for style checking:

```bash
pip install flake8
flake8 .
```

## Security

### File Handling

- Files are processed in isolated directories
- Temporary files are automatically cleaned up
- File size limits are enforced
- Only PDF files are accepted

### Data Privacy

- No credit report data is stored permanently
- All processing is done in memory
- Temporary files are securely deleted after processing

## License

Apache-2.0 license. See LICENSE file for details.
