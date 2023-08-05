from glitchtech_ai.tools import OpenAi, ManageSettings


def validate_token(ms: ManageSettings, oa: OpenAi):
    if not ms.settings_exist() and not oa.token:
        command = input('No API token detected. Please enter valid OpenAI token: ')
        ms.store_setting(key="open_ai_token", value=command)
        oa.update_token(token=ms.retrieve_setting(key="open_ai_token"))

    if ms.settings_exist() and oa.token:
        return True


def main():
    ms = ManageSettings(project_name="GlitchTech-AI")
    oa = OpenAi(prompt="You are a tired butler.")

    prompt = "[ OA ]-> "

    validate_token(ms=ms, oa=oa)

    while True:
        validate_token(ms=ms, oa=oa)

        command = input(prompt)
        if command.lower() in ['quit', 'q', 'exit', 'e']:
            print(oa.session_usage)
            break
        elif command:
            print(oa.chat_completions(user_input=command))


if __name__ == '__main__':
    validate_token()
