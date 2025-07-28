# Adobe Challenge 1B - Docker Setup 🐳

## 📦 Docker Image for Document Analysis Solution

This Docker setup packages the Adobe Hackathon Challenge 1B solution for easy deployment and execution across different environments.

## 🚀 Quick Start

### 1. Build the Docker Image

```bash
docker build -t adobe-challenge-1b .
```

### 2. Run with Sample Data (Current Collections)

```bash
docker run -v "$(pwd):/app/input" -v "$(pwd)/output:/app/output" adobe-challenge-1b
```

### 3. Run with Custom Data Directory

```bash
docker run -v "/path/to/your/collections:/app/input" -v "/path/to/output:/app/output" adobe-challenge-1b
```

## 📁 Input Structure Required

The input directory must contain collection folders with this structure:

```
input/
├── Collection 1/
│   ├── challenge1b_input.json
│   └── PDFs/
│       ├── document1.pdf
│       ├── document2.pdf
│       └── ...
├── Collection 2/
│   ├── challenge1b_input.json
│   └── PDFs/
│       ├── document1.pdf
│       └── ...
└── Collection N/
    ├── challenge1b_input.json
    └── PDFs/
        └── ...
```

### Input JSON Format (`challenge1b_input.json`)

```json
{
  "persona": {
    "role": "Travel Planner",
    "description": "A professional travel planner specializing in group trips"
  },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends",
    "context": "Budget-conscious group travel with focus on experiences"
  },
  "documents": [
    {
      "filename": "Document1.pdf",
      "title": "Document Title"
    }
  ]
}
```

## 📤 Output Structure

The solution generates output files in each collection directory:

```
output/
├── Collection 1/
│   └── challenge1b_solution_output.json
├── Collection 2/
│   └── challenge1b_solution_output.json
└── Collection N/
    └── challenge1b_solution_output.json
```

### Output JSON Format

```json
{
  "metadata": {
    "persona": { ... },
    "job_to_be_done": { ... },
    "documents": [ ... ],
    "timestamp": "2025-07-28T22:13:13.191100",
    "analysis_summary": "Extracted 5 sections using dynamic content analysis for travel domain"
  },
  "extracted_sections": [
    {
      "document": "Document.pdf",
      "section_title": "Dynamic Section Title",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "Document.pdf",
      "refined_text": "Dynamically extracted and refined content...",
      "page_number": 1
    }
  ]
}
```

## 🔧 Docker Commands Reference

### Build Image
```bash
docker build -t adobe-challenge-1b .
```

### Run Container (Linux/Mac)
```bash
docker run -v "$(pwd):/app/input" -v "$(pwd)/output:/app/output" adobe-challenge-1b
```

### Run Container (Windows PowerShell)
```powershell
docker run -v "${PWD}:/app/input" -v "${PWD}/output:/app/output" adobe-challenge-1b
```

### Run Container (Windows CMD)
```cmd
docker run -v "%cd%:/app/input" -v "%cd%/output:/app/output" adobe-challenge-1b
```

### Interactive Mode (for debugging)
```bash
docker run -it -v "$(pwd):/app/input" -v "$(pwd)/output:/app/output" adobe-challenge-1b /bin/bash
```

### Run with Custom Working Directory
```bash
docker run -v "/custom/input:/app/input" -v "/custom/output:/app/output" adobe-challenge-1b
```

## 🎯 Usage Examples

### Example 1: Process Current Collections
```bash
# Navigate to directory containing Collection 1, Collection 2, Collection 3
cd /path/to/adobe-challenge-data

# Build image
docker build -t adobe-challenge-1b .

# Run analysis
docker run -v "$(pwd):/app/input" -v "$(pwd)/output:/app/output" adobe-challenge-1b
```

### Example 2: Process Custom Collections
```bash
# Build image
docker build -t adobe-challenge-1b .

# Run with custom data
docker run \
  -v "/my/collections:/app/input" \
  -v "/my/results:/app/output" \
  adobe-challenge-1b
```

### Example 3: Development Mode
```bash
# Run in interactive mode for development
docker run -it \
  -v "$(pwd):/app/input" \
  -v "$(pwd)/output:/app/output" \
  adobe-challenge-1b /bin/bash

# Inside container, run manually
python main.py
```

## 📊 Expected Output

After running, you'll see console output like:

```
🚀 Starting Adobe Challenge 1B Solution with Dynamic Content Analysis
======================================================================
📁 Found 3 collections
📂 Processing Collection 1:
   📝 Persona: Travel Planner
   🎯 Job: Plan a trip of 4 days for a group of 10 college friends.
   🎭 Domain: travel
     📄 Processing: Document1.pdf
     📄 Processing: Document2.pdf
     🔍 Found 20 potential sections
     ✅ Selected: Section Title -> Document.pdf (page 1, score: 141.0)
   ✅ Successfully processed! Generated 5 sections
   💾 Output saved to: /app/input/Collection 1/challenge1b_solution_output.json
🎉 Processing complete!
```

## 🔍 Troubleshooting

### Common Issues

1. **No collections found**
   - Ensure input directory contains folders starting with "Collection"
   - Check that each folder has `challenge1b_input.json` and `PDFs/` directory

2. **Permission errors**
   - Ensure Docker has permission to read input directory
   - Check that output directory is writable

3. **PDF processing errors**
   - Verify PDFs are not corrupted
   - Check that PDFs contain extractable text

### Debug Commands

```bash
# Check container logs
docker logs <container_id>

# Run with verbose output
docker run -e PYTHONUNBUFFERED=1 -v "$(pwd):/app/input" adobe-challenge-1b

# Inspect container filesystem
docker run -it adobe-challenge-1b /bin/bash
```

## 🎯 Features

- **Dynamic Analysis**: No hardcoded mappings - adapts to any PDF collection
- **Multi-Domain**: Supports travel, HR, food, and general domains
- **Intelligent Scoring**: Uses multiple factors for relevance ranking
- **Robust Processing**: Handles various PDF formats and structures
- **Containerized**: Consistent execution across all environments

## 📋 Requirements

- Docker installed on your system
- Input collections with proper structure
- Minimum 512MB RAM for container
- Disk space for temporary PDF processing

## 🚀 Production Deployment

For production use:

```bash
# Build optimized image
docker build --no-cache -t adobe-challenge-1b:latest .

# Run with resource limits
docker run --memory=1g --cpus=1 \
  -v "/data/input:/app/input" \
  -v "/data/output:/app/output" \
  adobe-challenge-1b:latest
```
