import os

def parse_large_file(filepath, buffersize=1024*1024):
    """
    Reads a file line-by-line using a Generator.
    
    Why: This allows us to process files larger than RAM (e.g., 100GB logs)
    without crashing the memory. It streams data essentially 'lazily'.
    """
    try:
        # OPEN THE FILE SAFELY
        # encoding='utf-8': Ensures we don't crash on standard text.
        # errors='replace': Resilience. If a byte is corrupted, we get a  character
        # instead of crashing the whole pipeline.
        # NOTE: You forgot to pass 'buffering=buffersize' here! (See review below)
        with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
            
            # THE STREAMING LOOP
            # We iterate over the file object itself. This is memory efficient
            # because 'file' is an iterator that reads chunks as needed.
            for line in file:
                # YIELD (The Magic)
                # Instead of building a massive list (memory bomb), we hand 
                # one line back to the caller and pause execution here.
                yield line.strip()

    # ERROR HANDLING (Resilience)
    # Specific catches allow us to log exactly what went wrong.
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' does not exist.")
    except PermissionError:
        print(f"Error: Access denied. Check permissions for '{filepath}'.")
    except Exception as e:
        # Catch-all for unexpected issues (like disk full, I/O errors)
        print(f"Critical Failure: Unexpected error {e}")

def process_logs():
    """
    The Consumer function.
    It requests data from the generator one item at a time.
    """
    # 1. Initialize the Generator
    # This does NOT read the file yet. It just sets up the pointer.
    line_gen = parse_large_file("filetxt.log")
    
    # 2. Consume the Data
    # The loop pulls one line, prints it, and discards it from RAM.
    # Memory usage remains flat/constant regardless of file size.
    for line in line_gen:
        print(f"Processing log entry: {line}")

if __name__ == "__main__":
    # Entry point for the script
    process_logs()
