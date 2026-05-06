#!/usr/bin/env python3
import asyncio
import edge_tts
import subprocess
import os

BLOCKS = [
    [
        ("Ο Μάρκος ξυπνά κάθε πρωί στις επτά.", "Markos wakes up every morning at seven."),
        ("Σηκώνεται από το κρεβάτι και πλένεται γρήγορα.", "He gets up from bed and washes quickly."),
        ("Μετά ντύνεται και τρώει πρωινό.", "Then he gets dressed and has breakfast."),
        ("Στις οκτώ φεύγει για τη δουλειά.", "At eight he leaves for work."),
        ("Βιάζεται γιατί το λεωφορείο φεύγει σύντομα.", "He is in a hurry because the bus leaves soon."),
        ("Το βράδυ επιστρέφει σπίτι κουρασμένος.", "In the evening he returns home tired."),
        ("Μαγειρεύει μια απλή συνταγή και δειπνά.", "He cooks a simple recipe and has dinner."),
        ("Μετά χαλαρώνει στον καναπέ και κοιμάται νωρίς.", "Then he relaxes on the sofa and goes to sleep early."),
    ],
    [
        ("Κάθε Σάββατο, η Ελένη καθαρίζει το σπίτι.", "Every Saturday, Eleni cleans the house."),
        ("Πρώτα σκουπίζει το πάτωμα με την ηλεκτρική σκούπα.", "First she vacuums the floor."),
        ("Μετά ανοίγει τα παράθυρα για να αερίσει το σπίτι.", "Then she opens the windows to air out the house."),
        ("Πλένει τα πιάτα και μαζεύει τα πράγματά της.", "She washes the dishes and tidies up her things."),
        ("Τακτοποιεί τα βιβλία και βάζει πλυντήριο.", "She arranges the books and runs the washing machine."),
        ("Μετά ψωνίζει στο σούπερ μάρκετ.", "Then she goes shopping at the supermarket."),
        ("Το απόγευμα ετοιμάζεται για έξοδο.", "In the afternoon she gets ready to go out."),
        ("Έκλεισε ραντεβού με φίλες και σχεδιάζουν να πάνε σινεμά.", "She made an appointment with friends and they are planning to go to the cinema."),
    ],
    [
        ("Ο Νίκος έχει πολλά χόμπι και αγαπά τον ελεύθερο χρόνο του.", "Nikos has many hobbies and loves his free time."),
        ("Ασχολείται με τη φωτογραφία εδώ και χρόνια.", "He has been into photography for years."),
        ("Κάθε πρωί κάνει βόλτα στο πάρκο και γυμνάζεται.", "Every morning he goes for a walk in the park and works out."),
        ("Ακούει μουσική ενώ περπατά.", "He listens to music while walking."),
        ("Τα βράδια διαβάζει ή βλέπει μια ταινία.", "In the evenings he reads or watches a movie."),
        ("Το Σαββατοκύριακο βγαίνει έξω με φίλους.", "At the weekend he goes out with friends."),
        ("Περνά πάντα καλά και απολαμβάνει κάθε στιγμή.", "He always has a good time and enjoys every moment."),
        ("Το βράδυ ξεκουράζεται και παίζει κιθάρα.", "In the evening he rests and plays guitar."),
    ],
]

GREEK_VOICE = "el-GR-AthinaNeural"
ENGLISH_VOICE = "en-US-JennyNeural"
RATE = "-25%"
TEMP_DIR = "/tmp/greek_story_daily_activities"
OUTPUT_DIR = "content/vocabulary/daily_activities"


async def gen(text, voice, path):
    c = edge_tts.Communicate(text, voice, rate=RATE)
    await c.save(path)


async def generate_block(block_index, story):
    block_num = block_index + 1
    output = f"{OUTPUT_DIR}/story_block_{block_num}.mp3"
    tmp = f"{TEMP_DIR}/block_{block_num}"
    os.makedirs(tmp, exist_ok=True)

    silence = f"{TEMP_DIR}/silence.mp3"

    print(f"\n=== Block {block_num} ===")
    for i, (greek, english) in enumerate(story):
        for j in range(3):
            path = f"{tmp}/g{i}_{j}.mp3"
            await gen(greek, GREEK_VOICE, path)
            print(f"  [{i+1}/{len(story)}] Greek #{j+1}")
        path_en = f"{tmp}/e{i}.mp3"
        await gen(english, ENGLISH_VOICE, path_en)
        print(f"  [{i+1}/{len(story)}] English")

    list_file = f"{tmp}/list.txt"
    with open(list_file, "w") as f:
        for i in range(len(story)):
            for j in range(3):
                f.write(f"file '{silence}'\n")
                f.write(f"file '{tmp}/g{i}_{j}.mp3'\n")
            f.write(f"file '{silence}'\n")
            f.write(f"file '{tmp}/e{i}.mp3'\n")

    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", list_file, "-acodec", "libmp3lame", "-q:a", "4", output],
        check=True,
    )
    print(f"Done → {output}")


async def main():
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    silence = f"{TEMP_DIR}/silence.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
         "-t", "3", "-acodec", "libmp3lame", "-q:a", "9", silence],
        check=True, capture_output=True,
    )

    for i, story in enumerate(BLOCKS):
        await generate_block(i, story)

    print("\nAll blocks done.")


asyncio.run(main())
