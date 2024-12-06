import typer
import git
import os
import shutil
from tempfile import mkdtemp
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import time
from rich.logging import RichHandler
import logging
from pathspec import PathSpec
import signal
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler()]
)
logger = logging.getLogger("wip")

app = typer.Typer()

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, repo, pathspec):
        self.repo = repo
        self.pathspec = pathspec
        self.change_detected = False

    def on_modified(self, event):
        self.process_event(event)

    def on_created(self, event):
        self.process_event(event)

    def on_deleted(self, event):
        self.process_event(event)

    def process_event(self, event):
        if not event.is_directory and not self.pathspec.match_file(event.src_path):
            logger.info(f"Change detected: {event.src_path}")
            self.change_detected = True

def load_gitignore():
    patterns = ['.git']
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as gitignore:
            patterns.extend(gitignore.readlines())
    return PathSpec.from_lines('gitwildmatch', patterns)

def clear_directory(exclude='.git'):
    logger.info("Clearing working directory (except .git)...")
    for item in os.listdir(os.getcwd()):
        if item != exclude:
            path = os.path.join(os.getcwd(), item)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    logger.info("Working directory cleared.")

def switch_to_branch(repo, branch_name):
    try:
        if branch_name == 'wip':
            clear_directory()
        repo.git.checkout(branch_name)
        repo.git.restore('.')
    except Exception:
        if branch_name == 'wip':
            logger.info("Creating initial commit for 'wip' branch.")
            repo.git.add('.')
            repo.git.commit('-m', 'wip: initial')
        repo.git.checkout('-b', branch_name)
        repo.git.push('--set-upstream', 'origin', branch_name)
    logger.info(f"Switched to branch {branch_name}.")

def copy_directory(src, dest, exclude='.git'):
    logger.info(f"Copying files from {src} to {dest} (excluding {exclude})")
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s) and os.path.basename(s) != exclude:
            shutil.copytree(s, d, symlinks=True)
        elif not os.path.isdir(s):
            shutil.copy2(s, d)

def graceful_exit(signal_num, frame):
    logger.info("Received termination signal, exiting...")
    sys.exit(0)

@app.command()
def watch():
    signal.signal(signal.SIGINT, graceful_exit)
    signal.signal(signal.SIGTERM, graceful_exit)

    repo = git.Repo(os.getcwd())
    switch_to_branch(repo, 'wip')
    repo.git.pull()
    logger.info("Pulled latest changes.")

    gitignore_spec = load_gitignore()

    event_handler = ChangeHandler(repo, gitignore_spec)
    observer = Observer()
    observer.schedule(event_handler, path=os.getcwd(), recursive=True)
    observer.start()
    logger.info("Started watching for changes.")

    temp_dir = None

    try:
        while True:
            if event_handler.change_detected:
                logger.info("Adding changes and committing...")
                repo.git.add('.')
                commit_message = f"wip: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                repo.git.commit('-am', commit_message)
                repo.git.push()
                logger.info("Changes committed and pushed.")
                event_handler.change_detected = False

            time.sleep(5)

    except KeyboardInterrupt:
        logger.info("Watch interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        observer.stop()
        observer.join()
        logger.info("Stopped watching.")
        
        try:
            temp_dir = mkdtemp()
            copy_directory(os.getcwd(), temp_dir)
            switch_to_branch(repo, 'main')
            clear_directory()
            copy_directory(temp_dir, os.getcwd())
            logger.info("Switched back to main branch and restored changes.")
        except Exception as e:
            logger.error(f"Failed to clean up correctly: {e}")
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

if __name__ == "__main__":
    app()
