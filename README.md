# Server Performance Monitor

## Description
This repository contains a simple script `perf_graph.py` that monitors server performance over a defined period. It logs CPU and memory usage statistics at regular intervals and provides aggregated statistics for evaluation. Additionally, the script generates graphs to visualize the performance metrics.

## Requirements
- Python 3.6 or higher
- Required Python packages:
  - `psutil`
  - `matplotlib`
  - `argparse`
  - `logging`
- `pyinstaller` for building Windows executables

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/Rojo200-b/server_perf.git
   cd server_perf
   ```

2. Create a virtual environment and activate it:
   ```sh
   python3 -m pyenv env
   source pyenv/bin/activate
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Build and Execution
### Building Executables
You can build the executables for both Linux and Windows using the provided Makefile.

1. Install `pyinstaller`:
   ```sh
   pip install pyinstaller
   ```

2. Create the executables:
   ```sh
   make all
   ```

### Running the Script
To run the script directly using Python:

```sh
python src/perf_graph.py <timeout_in_seconds>
```

For example, to run the script for 60 seconds:
```sh
python src/perf_graph.py 60
```

### Running the Executables
After building, you can run the executables as follows:

#### Linux
```sh
./dist/linux/perf_graph <timeout_in_seconds>
```

#### Windows
Double-click the executable in the `dist/win` directory, or run it from the command line:
```cmd
perf_graph.exe <timeout_in_seconds>
```

## Example Usage
Here is an example of how to use the script:

```sh
python src/perf_graph.py 60
```

This will monitor the server's CPU and memory usage for 60 seconds, log the data, and generate performance graphs in an image.

## Clean Up
To clean up the build directories, you can use the `make clean` command:

```sh
make clean
```
