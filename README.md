# MissBVoice

Steps:
1. create a virtual environment: `python -m venv venv`
2. activate venv: `venv/Scripts/activate`
3. install vocode: `pip install vocode`
4. install groq: `pip install groq`
5. get api keys for:
   - deepgram: https://developers.deepgram.com/docs/create-additional-api-keys
   - groq: https://console.groq.com/docs/quickstart
   - azure speech key & region: https://docs.merkulov.design/how-to-get-microsoft-azure-tts-api-key/
you can place them in an env but it didn't work for me so you might as well just place them directly in chat.py
6. run the script: `python chat.py`
7. install any other dependencies needed that i might have forgotten about but the project will let you know they are missing, sorry :)
