import subprocess
import sys
import os
import shutil

def clone_or_update_github_docs(target_dir, repo_url):
    if os.path.exists(target_dir):
        print(f"Repository already cloned in '{target_dir}'. Pulling latest changes...")
        return
        try:
            result = subprocess.run(
                ["git", "-C", target_dir, "pull"],
                check=True, capture_output=True, text=True
            )

            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error pulling latest changes: {e}")
            print(f"Error details: {e.stderr}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
    else:
        print("Cloning GitHub docs repository...")
        try:
            result = subprocess.run(
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--single-branch",
                    "--branch", "main",
                    repo_url,
                    target_dir,
                ],
                check=True, capture_output=True, text=True
            )
            print(f"Repository cloned successfully to '{target_dir}' directory!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e}")
            print(f"Error details: {e.stderr}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

def copy_md_files(src_dir, dest_dir):
    print(f"Copying markdown files from '{src_dir}' to '{dest_dir}'...")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.md'):
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)

                if not os.path.exists(dest_file) or os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                    shutil.copy2(src_file, dest_file)

def git_helper():
    repo_url = "https://github.com/github/docs.git"
    target_dir = "gh_docs"
    result = clone_or_update_github_docs(target_dir, repo_url)
    copy_md_files(f'{target_dir}/content', 'data')