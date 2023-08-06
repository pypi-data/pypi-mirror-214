import subprocess


class NTTCommandLine:
    @classmethod
    def run_command(cls, command: str, folder_path: str = None) -> None:
        options = {} if folder_path is None else {
            'cwd': folder_path,
        }
        subprocess.run(args=command.split(' '), **options)