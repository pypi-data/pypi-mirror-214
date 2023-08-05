"""Interface artificial intelligence."""

import collections
import functools
import random
import re
import textwrap

import black
import openai
import requests
import web
import webagt

app = web.application(__name__, prefix="ai")
ELEVENLABS_API = "https://api.elevenlabs.io/v1"
ELEVENLABS_KEY = app.cfg.get("ELEVENLABS")
openai.api_key = app.cfg.get("OPENAI")


@functools.cache
def get_voice():
    return [
        v
        for v in requests.get(
            f"{ELEVENLABS_API}/voices",
            headers={"Accept": "application/json", "xi-api-key": ELEVENLABS_KEY},
        ).json()["voices"]
        if v["name"] == "Angelo"
    ][0]["voice_id"]


@app.control("")
class AI:
    """AI."""

    def get(self):
        """Return an index of data sources."""
        models = openai.Model.list()
        return app.view.index(models)


@app.control("image")
class Image:
    """OpenAI image."""

    def get(self):
        """."""
        return app.view.image()

    def post(self):
        """."""
        form = web.form("request")
        image_resp = openai.Image.create(prompt=form.request, n=1, size="512x512")
        return image_resp


@app.control("chat")
class Chat:
    """OpenAI chat."""

    def get(self):
        """."""
        return app.view.chat()

    def post(self):
        """."""
        form = web.form("request")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": form.request},
            ],
            max_tokens=500,
        )
        response_text = response.choices[0].message.content

        def highlight(matchobj):
            language, _, code = matchobj.group(1).partition("\n")
            code = textwrap.dedent(code)
            filename = ".sh"
            if language == "python":
                code = black.format_str(code, mode=black.Mode())
                filename = ".py"
            return web.slrzd.highlight(code, filename)

        output = web.mkdn(
            re.sub("```(.+?)```", highlight, response_text, flags=re.DOTALL)
        )
        return app.view.chat_response(form.request, response, output)


@app.control("bot")
class PersonalBot:
    """OpenAI chat."""

    def get(self):
        """."""
        return app.view.bot()

    def post(self):
        """."""
        form = web.form("request")
        negative_response = random.choice(("huh?", "i don't understand.", "try again."))
        prompt = f"""You are going to respond as if you are Angelo Gladding.

                     Act like a nice person and be generally helpful but do not be
                     afraid to be cunningly witty and even sometimes pompously curt.

                     Keep your response to a single sentence or two. If you don't have
                     an answer respond with "{negative_response}"

                     Respond to the following: {form.request}"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
        )
        response_text = response.choices[0].message.content
        print(response_text)
        audio = requests.post(
            f"{ELEVENLABS_API}/text-to-speech/{get_voice()}/stream",
            headers={
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_KEY,
            },
            json={
                "text": response_text,
                "model_id": "eleven_multilingual_v1",
                "voice_settings": {"stability": 1, "similarity_boost": 1},
            },
        )
        web.header("Content-Type", "audio/mp3")
        return audio.content
