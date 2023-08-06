# -*- coding: utf-8 -*-

"""mesh_sync provides entry point main()."""

__version__ = "1.1.1"

import argparse
import base64
import re
import sys
import os
import httpx
from vault import MeshVault
import traceback


def check_if_dot_git_exists() -> bool:
    # Scan the root directory for .git
    for root, dirs, files in os.walk(os.getcwd()):
        if '.git' in dirs:
            return True
    return False


def find_git_url() -> str or None:
    """
    Scan the .git folder for the repository url and name
    :return:
    """
    for root, dirs, files in os.walk(os.getcwd()):
        if '.git' in dirs or '.git' in files or '.git' in root:
            for file in files:
                if file == 'config':
                    with open(os.path.join(root, file), 'r') as f:
                        contents = f.read()
                        url = re.search(r'url\s*=\s*(.*)', contents).group(1)
                        path_and_project_name = url.replace("https://github.com/", "").replace(".git", "")
                        return path_and_project_name
    return None


async def download_and_replace_file(session, url, file_path: str, auth_token: str):
    """
    Download a file from an url and replace the file at the given path
    :param auth_token:
    :param session:
    :param url:
    :param file_path:
    :return:
    """
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Bearer {auth_token}',
        'Cookie': '_octo=GH1.1.613847517.1655532567; logged_in=no'
    }
    response = await session.request("GET", url, headers=headers)

    if response.status_code != 200:
        print("File_Get Error: %s" % response.text)
        return None

    # Make folder if it doesn't exist
    if '/' in file_path:
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

    with open(file_path, 'wb') as f:
        file_content = base64.b64decode(response.json()['content'])
        f.write(file_content)


async def get_update_file(auth_token: str, repo_url, force: bool) -> str or None:
    """
    Scan the .git folder for the latest commit hash
    :param force:
    :param auth_token:
    :param repo_url:
    :return:
    """
    # httpx client
    session = httpx.AsyncClient()

    try:
        url = f"https://api.github.com/repos/{repo_url}/contents/UPDATE_FILE"

        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'Bearer {auth_token}',
            'Cookie': '_octo=GH1.1.613847517.1655532567; logged_in=no'
        }

        response = await session.request("GET", url, headers=headers)
        download_tasks = []
        if response.status_code == 200:
            # Get the file content and since it's a base64 encoded string, decode it
            content = base64.b64decode(response.json()['content'])

            # Convert the content to a string
            content = content.decode('utf-8')
            # Use regex to get version:number, using a colon
            pattern = re.compile(r'version:(.*)')
            version_number = pattern.search(content)
            if version_number:
                version_number = version_number.group(1)
                print(">> Updating to version: %s" % version_number)

            if force:
                if len(content) > 0:
                    change_list = content.split('\n')

                    for change in change_list:
                        change_wanted = change.split(':')
                        if len(change_wanted) > 1:
                            change_action = change_wanted[0]
                            change_file = change_wanted[1]
                            if change_action == 'overwrite':
                                print("Overwrite/Download file: %s" % change_file)
                                link = f"https://api.github.com/repos/" \
                                       f"{repo_url}/contents/{change_file}"
                                download_tasks.append(asyncio.create_task(download_and_replace_file(session, link, change_file, auth_token)))
                                # await download_and_replace_file(session, link, change_file, auth_token)
            else:
                ask_for_confirmation = input("Do you want to replace the update/download files with the latest version? ["
                                             "y/n] ")
                if ask_for_confirmation.lower() == 'y':
                    if len(content) > 0:
                        change_list = content.split('\n')
                        for change in change_list:
                            change_wanted = change.split(':')
                            if len(change_wanted) > 1:
                                change_action = change_wanted[0]
                                change_file = change_wanted[1]
                                if change_action == 'overwrite':
                                    print("Overwrite/Download file: %s" % change_file)
                                    link = f"https://api.github.com/repos/" \
                                           f"{repo_url}/contents/{change_file}"
                                    download_tasks.append(asyncio.create_task(download_and_replace_file(session, link, change_file, auth_token)))
                                    # await download_and_replace_file(session, link, change_file, auth_token)
                else:
                    print("Aborting...")
                    sys.exit(0)


            # Use asyncio.as_completed to wait for all the tasks to be done
            for task in asyncio.as_completed(download_tasks):
                await task

            print(">> Download Complete, updated to version: %s" % version_number)
            await session.aclose()
        else:
            print("Auth Error: %s" % response.text)
            return None
    except Exception as e:
        print("Error: %s" % e)
        # Print traceback

        traceback.print_exc()
        return None



async def get_all_files(auth_token: str, tree_url, repo_url, force: bool) -> None:
    # Httpx session
    session = httpx.AsyncClient()
    try:
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'Bearer {auth_token}',
            'Cookie': '_octo=GH1.1.613847517.1655532567; logged_in=no'
        }

        response = await session.request("GET", tree_url, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            download_tasks = []
            for file in response_json['tree']:
                if file['type'] == 'blob':
                    print(">> Downloading file: %s" % file['path'])
                    url = f"https://api.github.com/repos/{repo_url}/contents/" + file['path']
                    download_tasks.append(asyncio.create_task(download_and_replace_file(session, url, file['path'], auth_token)))
                    # await download_and_replace_file(session, url, file['path'], auth_token)

            # Use asyncio.as_completed to wait for all the tasks to be done
            for task in asyncio.as_completed(download_tasks):
                await task

            await session.aclose()
        else:
            print("Auth Error: %s" % response.text)
            return None
    except Exception as e:
        print("Error: %s" % e)
        return None



def get_token_from_env() -> str or None:
    """
    Get the token from the environment variable
    :return:
    """
    token = os.getenv('GITHUB_TOKEN')
    if token is None:
        print(">> [GITHUB_TOKEN] No token found in environment variable 'GITHUB_TOKEN'")
        return None
    return token



async def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Downloads the latest version of the update files from the github repo')
    parser.add_argument('-p', help='Project ID', required=False)

    # Add argument called update that requires no arguments
    parser.add_argument('-u', help='Update files', action='store_true')

    # Add argument called -f that forces without asking for confirmation
    parser.add_argument('-f', help='Force update', action='store_true')

    # Add argument for the auth token
    parser.add_argument('-t', help='Auth token', required=False)

    parser.add_argument('-o', help='Organization prefix', required=False)

    args = parser.parse_args()
    project_id = args.p
    prefix = args.o
    vault = MeshVault()
    secs = await asyncio.create_task(vault.get_secrets())
    master_token = None
    if secs is None:
        print("[MeshVault] Access denied.")
    else:
        print("[MeshVault] Access granted, Secrets will be used directly.")
        master_token = secs['github_token']

    print("Project ID: %s" % project_id)

    # Check if user wrote the -u argument
    if args.u:
        print(">> Updating files...")
        # Check if UPDATE_FILE exists in the root of the folder
        if os.path.exists('UPDATE_FILE'):
            print(">> Found UPDATE_FILE")
            # Check if 'project' is in the UPDATE_FILE
            with open('UPDATE_FILE', 'r') as f:
                content = f.read()
                if 'project' in content:
                    # Get the project name using regex
                    project_name = re.search(r'project:(.*)', content).group(1)
                    print(">> Project name: %s" % project_name)
                    github_token = get_token_from_env()
                    if not args.t and github_token is None and master_token is None:
                        token = input("Enter your GitHub token: ")
                    elif github_token is not None or master_token is None:
                        token = github_token or master_token
                    else:
                        token = args.t

                    git_url_input = project_name.rstrip('/')

                    # Remove spaces from all the sides of the string
                    git_url_input = git_url_input.strip()

                    if '/' not in git_url_input:
                        # Single Project ID given, add prefix 'MeshMonitors-Remote-1/' if no -o argument is given
                        if prefix is None:
                            git_url_input = 'MeshMonitors-Remote-1/' + git_url_input
                        else:
                            git_url_input = prefix + '/' + git_url_input

                    if git_url_input is not None:
                        is_empty = os.listdir(os.getcwd()) == []
                        if is_empty:
                            print(">> No files found in the current directory, downloading latest version...")
                            await get_all_files(token,
                                          f"https://api.github.com/repos/{git_url_input}/git/trees/master?recursive=1",
                                          git_url_input, force=args.f)
                        else:
                            print(">> Found files in the current directory, updating latest version...")
                            await get_update_file(auth_token=token, repo_url=git_url_input, force=args.f)

                else:
                    print(">> No project found in the UPDATE_FILE")
        else:
            print(">> No UPDATE_FILE found in root of folder")
    else:
        try:
            if master_token is None:
                github_token = get_token_from_env()
                git_token = ""
                if github_token is None:
                    git_token = input("Enter your GitHub token: ")
                elif github_token is not None:
                    git_token = github_token
            else:
                git_token = master_token

            print(">> Executing mesh_sync version %s." % __version__)
            if check_if_dot_git_exists():
                print(">> Found .git folder, checking for updates...")
                git_url = find_git_url()
                if git_url is not None:
                    print(">> Found git url: %s" % git_url)
                    await get_update_file(auth_token=git_token, repo_url=git_url, force=args.f)
            else:

                print(">> Could not find .git url")
                if project_id is None:
                    git_url_input = input("Please enter the [Project ID] that was given to you: ")
                else:
                    git_url_input = project_id

                git_url_input = git_url_input.rstrip('/')

                # Remove spaces from all the sides of the string
                git_url_input = git_url_input.strip()

                if '/' not in git_url_input:
                    # Single Project ID given, add prefix 'MeshMonitors-Remote-1/'
                    if prefix is None:
                        git_url_input = 'MeshMonitors-Remote-1/' + git_url_input
                    else:
                        git_url_input = prefix + '/' + git_url_input

                if git_url_input is not None:
                    is_empty = os.listdir(os.getcwd()) == []
                    if is_empty:
                        print(">> No files found in the current directory, downloading latest version...")
                        await get_all_files(git_token,
                                          f"https://api.github.com/repos/{git_url_input}/git/trees/master?recursive=1",
                                          git_url_input, force=args.f)
                    else:
                        print(">> Found files in the current directory, updating latest version...")
                        await get_update_file(auth_token=git_token, repo_url=git_url_input, force=args.f)
        except KeyboardInterrupt:
            print("Aborting...")
            sys.exit(0)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())