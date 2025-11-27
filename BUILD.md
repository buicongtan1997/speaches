# Building Speaches as a Single Executable Binary

This guide explains how to build Speaches as a single executable binary file that can be embedded into another application.

## Prerequisites

- Python 3.12
- UV package manager (recommended) or pip
- All project dependencies installed

## Installation

First, install the build dependencies:

```bash
uv sync --group build
```

Or if using pip:

```bash
pip install pyinstaller>=6.11.1
```

## Building the Binary

### Using Task (recommended)

```bash
task build
```

### Using the build script directly

```bash
python scripts/build_binary.py
```

### Using PyInstaller directly

```bash
pyinstaller --clean speaches.spec
```

## Build Output

After a successful build, the binary will be located at:

```
dist/speaches
```

The binary is a self-contained executable that includes:
- All Python dependencies
- ML model handling code (faster-whisper, kokoro, piper, etc.)
- Static files (realtime-console)
- Configuration files

## Running the Binary

Simply execute the binary:

```bash
./dist/speaches
```

The server will start on the configured host and port (default: 0.0.0.0:8000).

## Configuration

The binary respects the same environment variables as the regular Python application:

- `SPEACHES_HOST`: Host to bind to (default: 0.0.0.0)
- `SPEACHES_PORT`: Port to bind to (default: 8000)
- `SPEACHES_LOG_LEVEL`: Logging level (default: INFO)
- `SPEACHES_API_KEY`: API key for authentication (optional)
- `SPEACHES_ENABLE_UI`: Enable Gradio UI (default: true)
- See `src/speaches/config.py` for all configuration options

Example:

```bash
SPEACHES_PORT=9000 SPEACHES_LOG_LEVEL=DEBUG ./dist/speaches
```

## Important Notes

### Model Downloads

The binary does not include pre-downloaded ML models. Models will be downloaded on first use from HuggingFace Hub. Make sure the environment where the binary runs has:
- Internet access for model downloads
- Sufficient disk space in the cache directory
- Write permissions to the HuggingFace cache directory

### GPU Support

For GPU support, ensure:
- CUDA toolkit is installed on the target system
- The `onnxruntime-gpu` package is properly included in the build
- The target system has compatible NVIDIA drivers

### Binary Size

The binary is quite large (typically 500MB - 1GB+) due to:
- Multiple ML frameworks (ONNX Runtime, CTranslate2)
- FastAPI and dependencies
- Gradio UI components

To reduce size, you can:
1. Exclude the Gradio UI by setting `SPEACHES_ENABLE_UI=false`
2. Remove unnecessary model executors in `speaches.spec`
3. Use UPX compression (already enabled in the spec file)

## Embedding in Another Application

To embed this binary in another application:

1. Copy the binary to your application's directory
2. Launch it as a subprocess:

```python
import subprocess

process = subprocess.Popen(
    ["./speaches"],
    env={
        "SPEACHES_HOST": "127.0.0.1",
        "SPEACHES_PORT": "8000",
        "SPEACHES_LOG_LEVEL": "INFO",
    }
)
```

3. Communicate with it via the OpenAI-compatible API at `http://localhost:8000/v1`

## Troubleshooting

### Build Fails

- Ensure all dependencies are installed: `uv sync --group build`
- Clean previous build artifacts: `rm -rf build dist`
- Check Python version: `python --version` (should be 3.12.x)

### Binary Crashes on Startup

- Check for missing system libraries: `ldd dist/speaches` (Linux)
- Verify environment variables are set correctly
- Run with `SPEACHES_LOG_LEVEL=DEBUG` for detailed logs

### Import Errors at Runtime

If you encounter import errors, you may need to add missing modules to the `hiddenimports` list in `speaches.spec`.

### Models Not Downloading

- Check internet connectivity
- Verify HuggingFace Hub access
- Set `HF_HOME` environment variable to specify cache location
- Check disk space and write permissions

## Platform-Specific Notes

### macOS

On macOS, you may need to:
- Allow the binary in System Preferences > Security & Privacy
- Sign the binary: `codesign -s - dist/speaches`

### Linux

Ensure all system libraries are available (especially CUDA for GPU support).

### Windows

Not currently tested. You may need to:
- Adjust paths in `speaches.spec`
- Install Visual C++ redistributables on target system
