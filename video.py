import asyncio
import os
from PIL import Image, ImageDraw, ImageFont

from moviepy import ImageClip, AudioFileClip, CompositeVideoClip
import edge_tts


async def create_voice(text, output_audio):
    voice = "de-DE-KatjaNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio)


def make_text_image(text, output_path, font_size=70, width=950):
    img = Image.new("RGB", (1080, 400), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    lines = []
    words = text.split()
    line = ""

    for word in words:
        test = line + " " + word if line else word
        if draw.textlength(test, font=font) <= width:
            line = test
        else:
            lines.append(line)
            line = word

    if line:
        lines.append(line)

    y = 20
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        x = (1080 - (bbox[2] - bbox[0])) / 2
        draw.text((x, y), line, font=font, fill=(255, 255, 255)
        y += font_size + 10

    img.save(output_path)


def create_reel(image_url, title, body, output_video):
    os.makedirs("temp", exist_ok=True)
    os.makedirs("reels", exist_ok=True)

    image_path = image_url
    audio_path = "temp/audio.mp3"
    title_img = "temp/title.png"
    subtitle_img = "temp/subtitle.png"

    script = f"{title}. {body}"

    asyncio.run(create_voice(script, audio_path))

    audio = AudioFileClip(audio_path)

    make_text_image(title, title_img, font_size=70)
    make_text_image("🌍 Kurioses aus aller Welt", subtitle_img, font_size=42)

    background = (
        ImageClip(image_path)
        .with_duration(audio.duration)
        .resized((1080, 1920))
    )

    headline = (
        ImageClip(title_img)
        .with_duration(audio.duration)
        .with_position(("center", 180))
    )

    subtitle = (
        ImageClip(subtitle_img)
        .with_duration(audio.duration)
        .with_position(("center", 1650))
    )

    final_video = CompositeVideoClip(
        [background, headline, subtitle],
        size=(1080, 1920)
    ).with_audio(audio)

    final_video.write_videofile(
        output_video,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        ffmpeg_params=[
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart"
        ]
    )

    audio.close()
    final_video.close()
