#!/usr/bin/env python3
import asyncio
import edge_tts
import subprocess
import os

STORY = [
    ("Ο Ιβάν είναι προγραμματιστής από τη Ρωσία.", "Ivan is a software developer from Russia."),
    ("Έχει μια γυναίκα και δύο παιδιά.", "He has a wife and two children."),
    ("Η οικογένειά του μετακόμισε στην Κύπρο.", "His family moved to Cyprus."),
    ("Τώρα ζουν σε μια όμορφη πόλη κοντά στη θάλασσα.", "Now they live in a beautiful city near the sea."),
    ("Ο Ιβάν δουλεύει σε μια εταιρεία τεχνολογίας.", "Ivan works at a technology company."),
    ("Γράφει κώδικα στον υπολογιστή του κάθε μέρα.", "He writes code on his computer every day."),
    ("Η γυναίκα του λέγεται Μαρία.", "His wife's name is Maria."),
    ("Τα παιδιά τους πηγαίνουν στο σχολείο και μαθαίνουν ελληνικά.", "Their children go to school and learn Greek."),
    ("Τα Σαββατοκύριακα, η οικογένεια πηγαίνει στην παραλία.", "On weekends, the family goes to the beach."),
    ("Τους αρέσει πολύ η ζωή τους στην Κύπρο.", "They like their life in Cyprus very much."),
]

GREEK_VOICE = "el-GR-AthinaNeural"
ENGLISH_VOICE = "en-US-JennyNeural"
RATE = "-25%"
TEMP_DIR = "/tmp/greek_story"
OUTPUT = "content/story_developer.mp3"


async def gen(text, voice, path):
    c = edge_tts.Communicate(text, voice, rate=RATE)
    await c.save(path)


async def main():
    os.makedirs(TEMP_DIR, exist_ok=True)

    silence = f"{TEMP_DIR}/silence.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
         "-t", "3", "-acodec", "libmp3lame", "-q:a", "9", silence],
        check=True, capture_output=True,
    )

    print("Generating audio segments...")
    for i, (greek, english) in enumerate(STORY):
        for j in range(3):
            path = f"{TEMP_DIR}/g{i}_{j}.mp3"
            await gen(greek, GREEK_VOICE, path)
            print(f"  [{i+1}/{len(STORY)}] Greek #{j+1}")
        path_en = f"{TEMP_DIR}/e{i}.mp3"
        await gen(english, ENGLISH_VOICE, path_en)
        print(f"  [{i+1}/{len(STORY)}] English")

    # Build concat list: [pause][gr][pause][gr][pause][gr][pause][en]
    list_file = f"{TEMP_DIR}/list.txt"
    with open(list_file, "w") as f:
        for i in range(len(STORY)):
            for j in range(3):
                f.write(f"file '{silence}'\n")
                f.write(f"file '{TEMP_DIR}/g{i}_{j}.mp3'\n")
            f.write(f"file '{silence}'\n")
            f.write(f"file '{TEMP_DIR}/e{i}.mp3'\n")

    print("Concatenating...")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", list_file, "-acodec", "libmp3lame", "-q:a", "4", OUTPUT],
        check=True,
    )
    print(f"\nDone → {OUTPUT}")


asyncio.run(main())
