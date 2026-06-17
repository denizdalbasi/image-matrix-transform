import os
import subprocess
from pathlib import Path

def run_analyzer(target_path):
    """
    Orchestrates the compilation of .jack files using the Java-based tool.
    """
    target = Path(target_path)
    
    # 1. Identify files to process
    if target.is_dir():
        files = list(target.glob("*.jack"))
    elif target.suffix == ".jack":
        files = [target]
    else:
        print(f"Error: {target_path} is not a .jack file or directory.")
        return

    if not files:
        print("No .jack files found to process.")
        return

    print(f"Found {len(files)} file(s). Starting analysis...")

    # 2. Process each file
    for jack_file in files:
        try:
            print(f"Analyzing: {jack_file.name}...")
            # Assuming you have compiled your Java files with 'javac *.java'
            # This triggers the Java JackAnalyzer entry point
            subprocess.run(["java", "JackAnalyzer", str(jack_file)], check=True)
            print(f"Successfully generated XML for {jack_file.name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to analyze {jack_file.name}: {e}")
        except FileNotFoundError:
            print("Error: 'java' command not found. Ensure JDK is in your PATH.")
            break

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_jack_file_or_directory>")
    else:
        run_analyzer(sys.argv[1])
