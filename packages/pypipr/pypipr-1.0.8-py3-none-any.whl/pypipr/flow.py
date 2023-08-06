'''
Runtutan prosedur untuk third party
'''


from .lib import *
from .console import *


def github_push(commit=None):
    """
    Menjalankan command status, add, commit dan push

    ```py
    github_push('Commit Message')
    ```
    """

    def console_input(prompt, default):
        print_colorize(prompt, text_end="")
        if default:
            print(default)
            return default
        else:
            return input()

    print_log("Menjalankan Github Push")
    console_run("Checking files", "git status")
    msg = console_input("Commit Message if any or empty to exit : ", commit)
    if msg:
        console_run("Mempersiapkan files", "git add .")
        console_run("Menyimpan files", f'git commit -m "{msg}"')
        console_run("Mengirim files", "git push")
    print_log("Selesai Menjalankan Github Push")


def github_pull():
    """
    Menjalankan command `git pull`

    ```py
    github_pull()
    ```
    """
    console_run("Git Pull", "git pull")



if __name__ == "__main__":
    print_colorize("Anda menjalankan module pypipr", color=colorama.Fore.RED)
