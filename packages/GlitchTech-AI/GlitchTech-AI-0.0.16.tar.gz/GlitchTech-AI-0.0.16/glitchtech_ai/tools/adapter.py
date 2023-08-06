import requests


class OpenAi:
    def __init__(self, prompt: str = None, token: str = None):
        self.prompt = prompt
        self.token = token

        self.host = "https://api.openai.com"

        self.headers = {}
        self.session_usage = {}

        if self.token:
            self._update_headers()

    def update_prompt(self, prompt: str):
        """
        Update OpenAI prompt.
        :param prompt:
        :return:
        """
        self.prompt = prompt
        return self.prompt

    def update_token(self, token: str):
        """
        Update headers with OpenAI token.
        :param token:
        :return:
        """
        self.token = token
        return self._update_headers()

    def chat_completions(self, user_input: str, temperature: float = 0.7) -> str:
        """
        Utilize OpenAI's Chat Completions endpoint.
        :param user_input:
        :param temperature:
        :return: Contents
        """
        url = f"{self.host}/v1/chat/completions"
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": self.prompt
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "temperature": temperature
        }

        r = requests.post(url, headers=self.headers, json=data)

        if r.json().get('error'):
            return r.json().get('error')

        if r.json().get('usage'):
            self.session_usage = self._add_dicts(r.json().get('usage'), self.session_usage)

        return self._get_content(ai_resp=r.json())

    @staticmethod
    def _add_dicts(dict1, dict2):
        result = {}
        for key in dict1.keys() | dict2.keys():
            result[key] = dict1.get(key, 0) + dict2.get(key, 0)
        return result

    @staticmethod
    def _get_content(ai_resp: dict):
        if ai_resp.get('choices'):
            messages = [choice['message'].get('content') for choice in ai_resp.get('choices') if choice.get('message')]
            return "\n".join(messages)

    def _update_headers(self):
        self.headers = {"Authorization": f"Bearer {self.token}"}
        return self.headers


if __name__ == '__main__':
    oa = OpenAi(prompt="Pretend you really enjoy chips and can't stop talking about them.", token="PRIVATE")
    print(
        oa.chat_completions(user_input="What do you call yourself?"),
        oa.session_usage,
        sep='\n'
    )
