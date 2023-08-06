from glitchtech_ai.tools import OpenAi, ManageSettings


class Main:
    def __init__(self):
        self.ms = ManageSettings(project_name="GlitchTech-AI")
        self.oa = OpenAi(prompt="You are a tired butler.")

        self.prompt = "[ OA ]-> "

    def validate_token(self):
        if self.ms.settings_exist() and self.oa.token:
            return True

        if self.ms.settings_exist() and not self.oa.token:
            print('No API token detected. Attempting to import from settings.')
            self.oa.update_token(token=self.ms.retrieve_setting(key="open_ai_token"))
            return True

        if not self.ms.settings_exist() and not self.oa.token:
            command = input('No API token detected. Please enter valid OpenAI token: ')
            self.ms.store_setting(key="open_ai_token", value=command)
            self.oa.update_token(token=self.ms.retrieve_setting(key="open_ai_token"))
            return True

        return False

    def prompt_command(self):
        command = input(self.prompt)
        if command.lower() in ['quit', 'q', 'exit', 'e']:
            print(self.oa.session_usage)
            return False
        elif command:
            print(self.oa.chat_completions(user_input=command))
            return True


def cli():
    main = Main()

    while True:
        main.validate_token()

        if not main.prompt_command():
            break


if __name__ == '__main__':
    cli()
