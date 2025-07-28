@echo off
REM Adobe Challenge 1B - Docker Execution Script for Windows
REM This script provides easy commands to build and run the Docker container

setlocal enabledelayedexpansion

REM Function to print colored output (Windows doesn't support colors easily, so using simple text)
:print_status
echo [INFO] %~1
goto :eof

:print_success
echo [SUCCESS] %~1
goto :eof

:print_warning
echo [WARNING] %~1
goto :eof

:print_error
echo [ERROR] %~1
goto :eof

REM Function to check if Docker is installed
:check_docker
docker --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker is not installed or not in PATH"
    exit /b 1
)
call :print_status "Docker is available"
goto :eof

REM Function to build the Docker image
:build_image
call :print_status "Building Adobe Challenge 1B Docker image..."
docker build -t adobe-challenge-1b:latest .
if errorlevel 1 (
    call :print_error "Failed to build Docker image"
    exit /b 1
)
call :print_success "Docker image built successfully"
goto :eof

REM Function to run the container
:run_container
set input_dir=%~1
set output_dir=%~2

if "%input_dir%"=="" set input_dir=%cd%
if "%output_dir%"=="" set output_dir=%cd%\output

call :print_status "Running Adobe Challenge 1B container..."
call :print_status "Input directory: !input_dir!"
call :print_status "Output directory: !output_dir!"

REM Create output directory if it doesn't exist
if not exist "!output_dir!" mkdir "!output_dir!"

docker run --rm -v "!input_dir!:/app/input:ro" -v "!output_dir!:/app/output" adobe-challenge-1b:latest

if errorlevel 1 (
    call :print_error "Container execution failed"
    exit /b 1
)
call :print_success "Container execution completed"
call :print_status "Check output directory: !output_dir!"
goto :eof

REM Function to run in interactive mode
:run_interactive
set input_dir=%~1
set output_dir=%~2

if "%input_dir%"=="" set input_dir=%cd%
if "%output_dir%"=="" set output_dir=%cd%\output

call :print_status "Running Adobe Challenge 1B container in interactive mode..."

if not exist "!output_dir!" mkdir "!output_dir!"

docker run -it --rm -v "!input_dir!:/app/input" -v "!output_dir!:/app/output" adobe-challenge-1b:latest /bin/bash
goto :eof

REM Function to show usage
:show_usage
echo Adobe Challenge 1B - Docker Execution Script for Windows
echo.
echo Usage: %~nx0 [COMMAND] [OPTIONS]
echo.
echo Commands:
echo   build                    Build the Docker image
echo   run [INPUT] [OUTPUT]     Run the container with optional input/output directories
echo   interactive [INPUT] [OUTPUT]  Run container in interactive mode
echo   compose                  Run using docker-compose
echo   clean                    Remove Docker image and cleanup
echo   help                     Show this help message
echo.
echo Examples:
echo   %~nx0 build                           # Build the image
echo   %~nx0 run                             # Run with current directory as input
echo   %~nx0 run C:\data\input C:\data\output    # Run with custom directories
echo   %~nx0 interactive                     # Run in interactive mode for debugging
echo   %~nx0 compose                         # Run using docker-compose
echo.
goto :eof

REM Function to run with docker-compose
:run_compose
call :print_status "Running with docker-compose..."

if not exist "docker-compose.yml" (
    call :print_error "docker-compose.yml not found"
    exit /b 1
)

docker-compose up --build

if errorlevel 1 (
    call :print_error "Docker-compose execution failed"
    exit /b 1
)
call :print_success "Docker-compose execution completed"
goto :eof

REM Function to clean up
:cleanup
call :print_status "Cleaning up Docker resources..."

REM Remove container if it exists
docker container rm adobe-challenge-1b >nul 2>&1

REM Remove image
docker image rm adobe-challenge-1b:latest >nul 2>&1

REM Clean up docker-compose resources
docker-compose down >nul 2>&1

call :print_success "Cleanup completed"
goto :eof

REM Main script logic
set command=%~1
if "%command%"=="" set command=help

if "%command%"=="build" (
    call :check_docker
    if errorlevel 1 exit /b 1
    call :build_image
) else if "%command%"=="run" (
    call :check_docker
    if errorlevel 1 exit /b 1
    docker image inspect adobe-challenge-1b:latest >nul 2>&1
    if errorlevel 1 (
        call :print_warning "Image not found. Building first..."
        call :build_image
        if errorlevel 1 exit /b 1
    )
    call :run_container "%~2" "%~3"
) else if "%command%"=="interactive" (
    call :check_docker
    if errorlevel 1 exit /b 1
    docker image inspect adobe-challenge-1b:latest >nul 2>&1
    if errorlevel 1 (
        call :print_warning "Image not found. Building first..."
        call :build_image
        if errorlevel 1 exit /b 1
    )
    call :run_interactive "%~2" "%~3"
) else if "%command%"=="debug" (
    call :check_docker
    if errorlevel 1 exit /b 1
    docker image inspect adobe-challenge-1b:latest >nul 2>&1
    if errorlevel 1 (
        call :print_warning "Image not found. Building first..."
        call :build_image
        if errorlevel 1 exit /b 1
    )
    call :run_interactive "%~2" "%~3"
) else if "%command%"=="compose" (
    call :check_docker
    if errorlevel 1 exit /b 1
    call :run_compose
) else if "%command%"=="clean" (
    call :check_docker
    if errorlevel 1 exit /b 1
    call :cleanup
) else if "%command%"=="help" (
    call :show_usage
) else if "%command%"=="--help" (
    call :show_usage
) else if "%command%"=="-h" (
    call :show_usage
) else (
    call :print_error "Unknown command: %command%"
    echo.
    call :show_usage
    exit /b 1
)

endlocal
