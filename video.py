import asyncio
import os
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip
import edge_tts


async def create_voice(text, output_audio):
    voice = "de-DE-KatjaNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio)


def create_reel(image_path, title, body, output_video):
    os.makedirs("reels", exist_ok=True)

    audio_path = output_video.replace(".mp4", ".mp3")

    script = f"{title}. {body}"

    asyncio.run(create_voice(script, audio_path))

    audio = AudioFileClip(audio_path)

    background = (
        ImageClip(image_path)
        .resize(height=1920)
        .crop(x_center=540, y_center=960, width=1080, height=1920)
        .set_duration(audio.duration)
    )

    headline = (
        TextClip(
            title,
            fontsize=70,
            color="white",
            font="DejaVu-Sans-Bold",
            method="caption",
            size=(950, None),
            align="center"
        )
        .set_position(("center", 180))
        .set_duration(audio.duration)
    )

    subtitle = (
        TextClip(
            "Kurioses aus aller Welt 🌍",
            fontsize=42,
            color="white",
            font="DejaVu-Sans-Bold",
            method="caption",
            size=(950, None),
            align="center"
        )
        .set_position(("center", 1700))
        .set_duration(audio.duration)
    )

    video = CompositeVideoClip([background, headline, subtitle])
    video = video.set_audio(audio)

    video.write_videofile(
        output_video,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return output_video
