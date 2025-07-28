#!/bin/bash

# Adobe Challenge 1B - Docker Execution Script
# This script provides easy commands to build and run the Docker container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    print_status "Docker is available"
}

# Function to build the Docker image
build_image() {
    print_status "Building Adobe Challenge 1B Docker image..."
    docker build -t adobe-challenge-1b:latest .
    if [ $? -eq 0 ]; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Function to run the container
run_container() {
    local input_dir=${1:-$(pwd)}
    local output_dir=${2:-$(pwd)/output}
    
    print_status "Running Adobe Challenge 1B container..."
    print_status "Input directory: $input_dir"
    print_status "Output directory: $output_dir"
    
    # Create output directory if it doesn't exist
    mkdir -p "$output_dir"
    
    docker run --rm \
        -v "$input_dir:/app/input:ro" \
        -v "$output_dir:/app/output" \
        adobe-challenge-1b:latest
    
    if [ $? -eq 0 ]; then
        print_success "Container execution completed"
        print_status "Check output directory: $output_dir"
    else
        print_error "Container execution failed"
        exit 1
    fi
}

# Function to run in interactive mode
run_interactive() {
    local input_dir=${1:-$(pwd)}
    local output_dir=${2:-$(pwd)/output}
    
    print_status "Running Adobe Challenge 1B container in interactive mode..."
    
    mkdir -p "$output_dir"
    
    docker run -it --rm \
        -v "$input_dir:/app/input" \
        -v "$output_dir:/app/output" \
        adobe-challenge-1b:latest /bin/bash
}

# Function to show usage
show_usage() {
    echo "Adobe Challenge 1B - Docker Execution Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  build                    Build the Docker image"
    echo "  run [INPUT] [OUTPUT]     Run the container with optional input/output directories"
    echo "  interactive [INPUT] [OUTPUT]  Run container in interactive mode"
    echo "  compose                  Run using docker-compose"
    echo "  clean                    Remove Docker image and cleanup"
    echo "  help                     Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build                           # Build the image"
    echo "  $0 run                             # Run with current directory as input"
    echo "  $0 run /data/input /data/output    # Run with custom directories"
    echo "  $0 interactive                     # Run in interactive mode for debugging"
    echo "  $0 compose                         # Run using docker-compose"
    echo ""
}

# Function to run with docker-compose
run_compose() {
    print_status "Running with docker-compose..."
    
    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml not found"
        exit 1
    fi
    
    docker-compose up --build
    
    if [ $? -eq 0 ]; then
        print_success "Docker-compose execution completed"
    else
        print_error "Docker-compose execution failed"
        exit 1
    fi
}

# Function to clean up
cleanup() {
    print_status "Cleaning up Docker resources..."
    
    # Remove container if it exists
    docker container rm adobe-challenge-1b 2>/dev/null || true
    
    # Remove image
    docker image rm adobe-challenge-1b:latest 2>/dev/null || true
    
    # Clean up docker-compose resources
    docker-compose down 2>/dev/null || true
    
    print_success "Cleanup completed"
}

# Main script logic
case "${1:-help}" in
    "build")
        check_docker
        build_image
        ;;
    "run")
        check_docker
        if ! docker image inspect adobe-challenge-1b:latest &> /dev/null; then
            print_warning "Image not found. Building first..."
            build_image
        fi
        run_container "$2" "$3"
        ;;
    "interactive"|"debug")
        check_docker
        if ! docker image inspect adobe-challenge-1b:latest &> /dev/null; then
            print_warning "Image not found. Building first..."
            build_image
        fi
        run_interactive "$2" "$3"
        ;;
    "compose")
        check_docker
        run_compose
        ;;
    "clean")
        check_docker
        cleanup
        ;;
    "help"|"--help"|"-h")
        show_usage
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_usage
        exit 1
        ;;
esac
