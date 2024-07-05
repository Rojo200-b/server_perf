# Define variables
PYINSTALLER = pyinstaller
# Source file
SRC = src/perf_graph.py

# Output directories
DIST_LINUX = dist/linux
DIST_WIN = dist/win

# Targets
.PHONY: all clean linux win

all: linux win

linux:
	# Create Linux executable
	$(PYINSTALLER) --onefile --distpath $(DIST_LINUX) $(SRC)
	@echo "Linux executable created in $(DIST_LINUX)"

win:
	# Create Windows executable 
	$(PYINSTALLER) --onefile --distpath $(DIST_WIN) $(SRC)
	@echo "Windows executable created in $(DIST_WIN)"

clean:
	# Clean up build directories
	rm -rf build dist/*.spec
	@echo "Cleaned up build directories"
