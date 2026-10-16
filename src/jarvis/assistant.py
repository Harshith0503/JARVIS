from .commands import handle_command


class Assistant:
    def respond(self, command: str) -> str:
        return handle_command(command)

    @staticmethod
    def is_exit_command(command: str) -> bool:
        return command.strip().lower() in {
            "stop",
            "quit",
            "exit",
            "goodbye"
        }