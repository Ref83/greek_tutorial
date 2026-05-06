#!/usr/bin/env python3
import asyncio
import edge_tts
import subprocess
import os
import json

VOCAB_FILE = "content/vocabulary/numbers_dates/vocabulary.json"
GREEK_VOICE = "el-GR-AthinaNeural"
ENGLISH_VOICE = "en-US-JennyNeural"
RATE = "-25%"
TEMP_DIR = "/tmp/greek_story_numbers_dates"


async def gen(text, voice, path):
    c = edge_tts.Communicate(text, voice, rate=RATE)
    await c.save(path)


async def generate_block(block_index, sentences, silence):
    output = f"content/vocabulary/numbers_dates/story_block_{block_index + 1}.mp3"
    print(f"\nBlock {block_index + 1}: generating {len(sentences)} sentences...")

    for i, s in enumerate(sentences):
        greek = s["sentence"]
        english = s["translation"]
        for j in range(3):
            path = f"{TEMP_DIR}/b{block_index}_g{i}_{j}.mp3"
            await gen(greek, GREEK_VOICE, path)
            print(f"  [{i+1}/{len(sentences)}] Greek #{j+1}")
        path_en = f"{TEMP_DIR}/b{block_index}_e{i}.mp3"
        await gen(english, ENGLISH_VOICE, path_en)
        print(f"  [{i+1}/{len(sentences)}] English")

    list_file = f"{TEMP_DIR}/b{block_index}_list.txt"
    with open(list_file, "w") as f:
        for i in range(len(sentences)):
            for j in range(3):
                f.write(f"file '{silence}'\n")
                f.write(f"file '{TEMP_DIR}/b{block_index}_g{i}_{j}.mp3'\n")
            f.write(f"file '{silence}'\n")
            f.write(f"file '{TEMP_DIR}/b{block_index}_e{i}.mp3'\n")

    print(f"  Concatenating → {output}")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", list_file, "-acodec", "libmp3lame", "-q:a", "4", output],
        check=True,
    )
    print(f"  Done → {output}")


async def main():
    os.makedirs(TEMP_DIR, exist_ok=True)

    with open(VOCAB_FILE) as f:
        data = json.load(f)

    silence = f"{TEMP_DIR}/silence.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
         "-t", "3", "-acodec", "libmp3lame", "-q:a", "9", silence],
        check=True, capture_output=True,
    )

    for i, block in enumerate(data["blocks"]):
        sentences = block["story"]["sentences"]
        await generate_block(i, sentences, silence)

    print("\nAll blocks done!")


asyncio.run(main())
