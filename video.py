import asyncio
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import edge_tts


async def create_voice(text, output_audio):
    voice = "de-DE-KatjaNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_audio)


def get_font(size):
    try:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            size
        )
    except:
        return ImageFont.load_default()


def draw_centered_text(draw, text, y, font, max_width=950):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            lines.append(line)
            line = word

    if line:
        lines.append(line)

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        x = (1080 - (bbox[2] - bbox[0])) / 2
        draw.text((x, y), line, font=font, fill="white")
        y += font.size + 12


def create_reel(image_url, title, body, output_video):
    os.makedirs("temp", exist_ok=True)
    os.makedirs("reels", exist_ok=True)

    image_path = image_url
    audio_path = "temp/audio.mp3"
    frame_path = "temp/frame.png"

    script = f"{title}. {body}"
    asyncio.run(create_voice(script, audio_path))

    img = Image.open(image_path).convert("RGB")
    img = img.resize((1080, 1920))

    overlay = Image.new("RGB", (1080, 1920), (0, 0, 0))
    overlay.paste(img, (0, 0))

    draw = ImageDraw.Draw(overlay)

    title_font = get_font(70)
    subtitle_font = get_font(42)

    draw_centered_text(draw, title, 160, title_font)
    draw_centered_text(draw, "🌍 Kurioses aus aller Welt", 1650, subtitle_font)

    overlay.save(frame_path)

    command = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", frame_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        output_video
    ]

    subprocess.run(command, check=True)

    return output_video
