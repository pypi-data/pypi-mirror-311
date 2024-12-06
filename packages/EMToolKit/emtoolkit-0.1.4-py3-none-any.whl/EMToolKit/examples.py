import webbrowser
import subprocess
import time
import os

def examples():
    url = "https://emtoolkit.readthedocs.io/en/latest/examples/GALLERY_HEADER.html"
    webbrowser.open(url)

def start_jupyter_notebook(notebook_dir=None, open_browser=True):
    # Set the notebook directory
    if notebook_dir is None:
        notebook_dir = os.getcwd()

    # Construct the command to start Jupyter server
    command = ["jupyter", "notebook", "--notebook-dir", notebook_dir]

    # Start the Jupyter server
    process = subprocess.Popen(command)

    # Give the server some time to start
    time.sleep(2)

    # Open the default notebook URL if requested
    if open_browser:
        url = f"http://localhost:8888"
        webbrowser.open(url)

    return process

def stop_jupyter_notebook(process):
    process.terminate()

def run_example():
    # Start the Jupyter notebook
    jupyter_process = start_jupyter_notebook()

    # To keep the script running and the server open
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the Jupyter server...")
        stop_jupyter_notebook(jupyter_process)


if __name__ == "__main__":
    examples()
