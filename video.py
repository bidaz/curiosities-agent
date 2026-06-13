import asyncio
import os

from moviepy import (
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip
)

import edge_tts


async def create_voice(text, output_audio):
    voice = "de-DE-KatjaNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio)


def create_reel(image_url, title, body, output_video):

    os.makedirs("temp", exist_ok=True)
    os.makedirs("reels", exist_ok=True)

    image_path = image_url
    audio_path = "temp/audio.mp3"

    script = f"{title}. {body}"

    asyncio.run(create_voice(script, audio_path))

    audio = AudioFileClip(audio_path)

    background = (
        ImageClip(image_path)
        .with_duration(audio.duration)
        .resized(width=1080)
    )

    headline = (
        TextClip(
            text=title,
            font_size=70,
            color="white",
            size=(950, None),
            method="caption",
            text_align="center"
        )
        .with_position(("center", 180))
        .with_duration(audio.duration)
    )

    subtitle = (
        TextClip(
            text="🌍 Kurioses aus aller Welt",
            font_size=42,
            color="white",
            size=(950, None),
            method="caption",
            text_align="center"
        )
        .with_position(("center", 1700))
        .with_duration(audio.duration)
    )

    final_video = CompositeVideoClip(
        [
            background,
            headline,
            subtitle
        ],
        size=(1080, 1920)
    ).with_audio(audio)

    final_video.write_videofile(
        output_video,
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )

    audio.close()
    final_video.close()
