# 🐳 Docker Setup Guide for Adobe Challenge 1B

## 📋 Prerequisites

1. **Docker Desktop** installed and running
   - Download from: https://www.docker.com/products/docker-desktop
   - Ensure Docker Desktop is started before running commands

2. **Sufficient System Resources**
   - At least 2GB free RAM
   - 1GB free disk space
   - Windows 10/11 with WSL2 enabled (for Windows users)

## 🚀 Quick Start Commands

### Option 1: Using Docker Directly

```bash
# 1. Build the image
docker build -t adobe-challenge-1b .

# 2. Run with current directory (Windows PowerShell)
docker run --rm -v "${PWD}:/app/input:ro" -v "${PWD}/output:/app/output" adobe-challenge-1b

# 2. Run with current directory (Linux/Mac)
docker run --rm -v "$(pwd):/app/input:ro" -v "$(pwd)/output:/app/output" adobe-challenge-1b

# 2. Run with current directory (Windows CMD)
docker run --rm -v "%cd%:/app/input:ro" -v "%cd%/output:/app/output" adobe-challenge-1b
```

### Option 2: Using Docker Compose (Recommended)

```bash
# Build and run in one command
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop and cleanup
docker-compose down
```

### Option 3: Using Helper Scripts

**Linux/Mac:**
```bash
# Make script executable
chmod +x run-docker.sh

# Build and run
./run-docker.sh build
./run-docker.sh run

# Interactive mode for debugging
./run-docker.sh interactive
```

**Windows:**
```cmd
# Build and run
run-docker.bat build
run-docker.bat run

# Interactive mode for debugging
run-docker.bat interactive
```

## 📁 Input/Output Structure

### Expected Input Structure:
```
your-directory/
├── Collection 1/
│   ├── challenge1b_input.json
│   └── PDFs/
│       ├── document1.pdf
│       └── document2.pdf
├── Collection 2/
│   ├── challenge1b_input.json
│   └── PDFs/
│       └── documents...
└── Collection N/
    ├── challenge1b_input.json
    └── PDFs/
        └── documents...
```

### Generated Output Structure:
```
output/
├── Collection 1/
│   └── challenge1b_solution_output.json
├── Collection 2/
│   └── challenge1b_solution_output.json
└── Collection N/
    └── challenge1b_solution_output.json
```

## 🔧 Docker Commands Reference

### Building the Image
```bash
# Basic build
docker build -t adobe-challenge-1b .

# Build without cache (for updates)
docker build --no-cache -t adobe-challenge-1b .

# Build with specific tag
docker build -t adobe-challenge-1b:v1.0 .
```

### Running the Container

**Basic Run:**
```bash
docker run --rm adobe-challenge-1b
```

**With Volume Mounts:**
```bash
# Windows PowerShell
docker run --rm -v "${PWD}:/app/input:ro" -v "${PWD}/output:/app/output" adobe-challenge-1b

# Linux/Mac
docker run --rm -v "$(pwd):/app/input:ro" -v "$(pwd)/output:/app/output" adobe-challenge-1b

# Windows CMD
docker run --rm -v "%cd%:/app/input:ro" -v "%cd%/output:/app/output" adobe-challenge-1b
```

**With Custom Directories:**
```bash
docker run --rm \
  -v "/path/to/input:/app/input:ro" \
  -v "/path/to/output:/app/output" \
  adobe-challenge-1b
```

**Interactive Mode (for debugging):**
```bash
docker run -it --rm \
  -v "$(pwd):/app/input" \
  -v "$(pwd)/output:/app/output" \
  adobe-challenge-1b /bin/bash
```

### Docker Compose Commands

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop containers
docker-compose stop

# Stop and remove containers
docker-compose down

# Cleanup everything
docker-compose down --volumes --remove-orphans
```

## 🛠️ Development Commands

### Development with Live Code Changes
```bash
# Run development service with code mounting
docker-compose --profile dev up adobe-challenge-1b-dev

# Or directly with Docker
docker run -it --rm \
  -v "$(pwd):/app/input" \
  -v "$(pwd)/output:/app/output" \
  -v "$(pwd)/main.py:/app/main.py" \
  adobe-challenge-1b /bin/bash
```

### Debugging
```bash
# Check container logs
docker logs <container_id>

# Run with verbose Python output
docker run --rm \
  -e PYTHONUNBUFFERED=1 \
  -v "$(pwd):/app/input:ro" \
  -v "$(pwd)/output:/app/output" \
  adobe-challenge-1b

# Inspect the built image
docker run -it --rm adobe-challenge-1b /bin/bash
```

## 🎯 Example Execution Workflows

### Workflow 1: First Time Setup
```bash
# 1. Ensure Docker Desktop is running
# 2. Navigate to project directory
cd /path/to/adobe-challenge-1b

# 3. Build the image
docker build -t adobe-challenge-1b .

# 4. Run analysis
docker run --rm -v "$(pwd):/app/input:ro" -v "$(pwd)/output:/app/output" adobe-challenge-1b

# 5. Check results
ls output/*/
```

### Workflow 2: Using Helper Scripts
```bash
# Linux/Mac
./run-docker.sh build
./run-docker.sh run

# Windows
run-docker.bat build
run-docker.bat run
```

### Workflow 3: Docker Compose
```bash
# One command to build and run
docker-compose up --build

# Check output
ls output/*/challenge1b_solution_output.json
```

### Workflow 4: Custom Data Processing
```bash
# Prepare custom data directory
mkdir -p /my/custom/input
cp -r my-collections/* /my/custom/input/

# Run with custom paths
docker run --rm \
  -v "/my/custom/input:/app/input:ro" \
  -v "/my/custom/output:/app/output" \
  adobe-challenge-1b

# Check results
ls /my/custom/output/*/
```

## 🔍 Troubleshooting

### Common Issues and Solutions

**1. Docker Desktop not running**
```
Error: Cannot connect to Docker daemon
Solution: Start Docker Desktop application
```

**2. Permission errors (Linux/Mac)**
```bash
# Fix permissions
sudo chown -R $USER:$USER output/
```

**3. Volume mount issues (Windows)**
```bash
# Ensure path format is correct
# Use forward slashes or properly escaped backslashes
docker run --rm -v "C:/path/to/data:/app/input:ro" adobe-challenge-1b
```

**4. No collections found**
```
Check that input directory contains:
- Folders starting with "Collection"
- Each folder has challenge1b_input.json
- Each folder has PDFs/ subdirectory
```

**5. Memory issues**
```bash
# Run with memory limit
docker run --memory=1g --rm -v "$(pwd):/app/input:ro" adobe-challenge-1b
```

### Debug Commands
```bash
# Check image exists
docker images | grep adobe-challenge-1b

# Check container status
docker ps -a

# Remove containers and images for fresh start
docker container prune
docker image rm adobe-challenge-1b
docker build -t adobe-challenge-1b .
```

## 📊 Expected Output

### Console Output:
```
🚀 Starting Adobe Challenge 1B Solution with Dynamic Content Analysis
======================================================================
📁 Found 3 collections
📂 Processing Collection 1:
   📝 Persona: Travel Planner
   🎯 Job: Plan a trip of 4 days for a group of 10 college friends.
   🎭 Domain: travel
     📄 Processing: Document1.pdf
     🔍 Found 20 potential sections
     ✅ Selected: Section Title -> Document.pdf (page 1, score: 141.0)
   ✅ Successfully processed! Generated 5 sections
   💾 Output saved to: /app/input/Collection 1/challenge1b_solution_output.json
🎉 Processing complete!
```

### File Output:
- `output/Collection 1/challenge1b_solution_output.json`
- `output/Collection 2/challenge1b_solution_output.json`
- `output/Collection 3/challenge1b_solution_output.json`

## 🚀 Production Deployment

### Optimized Production Run
```bash
# Build optimized image
docker build --no-cache -t adobe-challenge-1b:prod .

# Run with resource limits
docker run --rm \
  --memory=1g \
  --cpus=1 \
  --read-only \
  --tmpfs /tmp \
  -v "/data/input:/app/input:ro" \
  -v "/data/output:/app/output" \
  adobe-challenge-1b:prod
```

### CI/CD Integration
```yaml
# Example GitHub Actions step
- name: Run Adobe Challenge 1B Analysis
  run: |
    docker build -t adobe-challenge-1b .
    docker run --rm \
      -v "${{ github.workspace }}/input:/app/input:ro" \
      -v "${{ github.workspace }}/output:/app/output" \
      adobe-challenge-1b
```

## 📋 Requirements Summary

- **Docker Desktop**: Latest version installed and running
- **System Resources**: 2GB RAM, 1GB disk space
- **Input Data**: Properly structured collections with PDFs
- **Output Directory**: Writable location for results

## 🎯 Features Summary

- **Containerized Execution**: Consistent across all environments
- **Dynamic Analysis**: No hardcoded mappings
- **Multi-Platform**: Windows, macOS, Linux support
- **Easy Deployment**: Single command execution
- **Development Friendly**: Interactive debugging mode
- **Production Ready**: Resource limits and optimization options
