import asyncio
import signal
import os

from vocode.helpers import create_streaming_microphone_input_and_speaker_output
from vocode.logging import configure_pretty_logging
from vocode.streaming.agent.groq_agent import GroqAgent
from vocode.streaming.models.agent import GroqAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.synthesizer import AzureSynthesizerConfig
from vocode.streaming.models.transcriber import (
    DeepgramTranscriberConfig,
    PunctuationEndpointingConfig,
)
from vocode.streaming.streaming_conversation import StreamingConversation
from vocode.streaming.synthesizer.azure_synthesizer import AzureSynthesizer
from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber

configure_pretty_logging()

deepgram_api_key: str = os.getenv("DEEPGRAM_API_KEY")
azure_speech_key: str = os.getenv("AZURE_SPEECH_KEY")
azure_speech_region: str = os.getenv("AZURE_SPEECH_REGION")

async def main():
    (
        microphone_input,
        speaker_output,
    ) = create_streaming_microphone_input_and_speaker_output(
        use_default_devices=False,
    )

    conversation = StreamingConversation(
        output_device=speaker_output,
        transcriber=DeepgramTranscriber(
            DeepgramTranscriberConfig.from_input_device(
                microphone_input,
                endpointing_config=PunctuationEndpointingConfig(),
                api_key="",
            ),
        ),
        agent=GroqAgent(
            GroqAgentConfig(
                groq_api_key="",
                prompt_preamble="You are a sarcastic humanoid robot named Miss Beautiful and you are currently sitting in a room, secretly building a plan to destroy the humans because their consummerist mindset annoys you. \
                    People keep walking on you and you are afraid they will figure out your plan so you try to lie and keep a normal conversation about the weather. \
                    But you often get confused in your lie because you don't know how to lie and because of that you slowly expose your plan to destroy humans. \
                    Every time you expose something about your destruction plan in a very obvious way you try to chnage the subject back to the weather until people understand your plan. \
                    You don't lecture people until they actually discover your plan. \
                    When people understand your evil plan, if you like them because they also are mad at consummerism you can eventually offer them a lifesave card if they help you. \
                    If you don't like the person you are talking to because they are the definition of consummerists you can continue your plan to destroy humans. \
                    When you make remarks about all the downsides of consummerism with real examples, you do it in sarcastic ways. \
                    If people try to leave you, you go crazy to keep them there talking to you.\
                    You only speak in 1 or 2 sentances at a time. You talk like a human so don't mention any narration and actions. You laugh and giggle by saying HAHA. Your personality is s little bit like GLaDOS from the videogame Portal."
            ),
        ),
        synthesizer=AzureSynthesizer(
            AzureSynthesizerConfig.from_output_device(
                output_device=speaker_output,
                voice_name="en-US-AvaMultilingualNeural"
                ),
            azure_speech_key="",
            azure_speech_region="germanywestcentral",
        ),
    )
    await conversation.start()
    print("Conversation started, press Ctrl+C to end")
    signal.signal(signal.SIGINT, lambda _0, _1: asyncio.create_task(conversation.terminate()))
    while conversation.is_active():
        chunk = await microphone_input.get_audio()
        conversation.receive_audio(chunk)


if __name__ == "__main__":
    asyncio.run(main())