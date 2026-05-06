#!/usr/bin/env python3
import asyncio
import edge_tts
import subprocess
import os

BLOCKS = [
    {
        "name": "block_1",
        "story": [
            ("Μένω σε ένα διαμέρισμα στην Αθήνα.", "I live in an apartment in Athens."),
            ("Το κτίριο έχει πέντε ορόφους και υπόγειο γκαράζ.", "The building has five floors and an underground garage."),
            ("Το διαμέρισμά μου είναι στον τρίτο όροφο.", "My apartment is on the third floor."),
            ("Έχει μεγάλα παράθυρα και ένα μπαλκόνι με θέα στον κήπο.", "It has large windows and a balcony with a view of the garden."),
            ("Η εξώπορτα του κτιρίου είναι πάντα κλειδωμένη.", "The front door of the building is always locked."),
            ("Η είσοδος είναι στα δεξιά.", "The entrance is on the right."),
            ("Κάποτε ήθελα να μένω σε μονοκατοικία με μεγάλο κήπο.", "Once I wanted to live in a detached house with a large garden."),
            ("Ένα διώροφο σπίτι με ταράτσα θα ήταν τέλειο!", "A two-story house with a roof terrace would be perfect!"),
        ],
    },
    {
        "name": "block_2",
        "story": [
            ("Το σπίτι μας έχει πολλά δωμάτια.", "Our house has many rooms."),
            ("Η κουζίνα είναι μεγάλη και φωτεινή.", "The kitchen is large and bright."),
            ("Το σαλόνι έχει μεγάλο καναπέ και τηλεόραση.", "The living room has a big sofa and a TV."),
            ("Η τραπεζαρία είναι δίπλα στην κουζίνα.", "The dining room is next to the kitchen."),
            ("Έχουμε δύο κρεβατοκάμαρες, ένα μπάνιο και μια ξεχωριστή τουαλέτα.", "We have two bedrooms, a bathroom and a separate toilet."),
            ("Ο διάδρομος συνδέει όλα τα δωμάτια.", "The hallway connects all the rooms."),
            ("Η αποθήκη είναι κάτω από τη σκάλα.", "The storage room is under the staircase."),
            ("Το γραφείο μου είναι ήσυχο — τέλειο για εργασία!", "My home office is quiet — perfect for work!"),
        ],
    },
    {
        "name": "block_3",
        "story": [
            ("Στην κρεβατοκάμαρά μου έχω ένα άνετο κρεβάτι και ένα κομοδίνο.", "In my bedroom I have a comfortable bed and a bedside table."),
            ("Το γραφείο μου είναι δίπλα στο παράθυρο.", "My desk is next to the window."),
            ("Η ντουλάπα μου είναι γεμάτη ρούχα.", "My wardrobe is full of clothes."),
            ("Στο σαλόνι υπάρχει ένας μεγάλος καναπές και μια άνετη πολυθρόνα.", "In the living room there is a big sofa and a comfortable armchair."),
            ("Οι κουρτίνες είναι λευκές και φωτίζουν το δωμάτιο.", "The curtains are white and brighten the room."),
            ("Ο μεγάλος καθρέφτης στον τοίχο κάνει το δωμάτιο να φαίνεται μεγαλύτερο.", "The large mirror on the wall makes the room look bigger."),
            ("Τα βιβλία μου είναι τακτοποιημένα στη βιβλιοθήκη.", "My books are neatly arranged in the bookcase."),
            ("Ένα μαλακό χαλί στο πάτωμα κάνει το δωμάτιο πιο ζεστό.", "A soft rug on the floor makes the room warmer."),
        ],
    },
]

GREEK_VOICE = "el-GR-AthinaNeural"
ENGLISH_VOICE = "en-US-JennyNeural"
RATE = "-25%"
TEMP_DIR = "/tmp/greek_story_home"
OUTPUT_DIR = "content/vocabulary/home"


async def gen(text, voice, path):
    c = edge_tts.Communicate(text, voice, rate=RATE)
    await c.save(path)


async def generate_block(block, silence):
    name = block["name"]
    story = block["story"]
    output = f"{OUTPUT_DIR}/story_{name}.mp3"

    print(f"\n=== Generating {name} ===")
    for i, (greek, english) in enumerate(story):
        for j in range(3):
            path = f"{TEMP_DIR}/{name}_g{i}_{j}.mp3"
            await gen(greek, GREEK_VOICE, path)
            print(f"  [{i+1}/{len(story)}] Greek #{j+1}")
        path_en = f"{TEMP_DIR}/{name}_e{i}.mp3"
        await gen(english, ENGLISH_VOICE, path_en)
        print(f"  [{i+1}/{len(story)}] English")

    list_file = f"{TEMP_DIR}/{name}_list.txt"
    with open(list_file, "w") as f:
        for i in range(len(story)):
            for j in range(3):
                f.write(f"file '{silence}'\n")
                f.write(f"file '{TEMP_DIR}/{name}_g{i}_{j}.mp3'\n")
            f.write(f"file '{silence}'\n")
            f.write(f"file '{TEMP_DIR}/{name}_e{i}.mp3'\n")

    print(f"  Concatenating {name}...")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", list_file, "-acodec", "libmp3lame", "-q:a", "4", output],
        check=True,
    )
    print(f"  Done → {output}")


async def main():
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    silence = f"{TEMP_DIR}/silence.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
         "-t", "3", "-acodec", "libmp3lame", "-q:a", "9", silence],
        check=True, capture_output=True,
    )

    for block in BLOCKS:
        await generate_block(block, silence)

    print("\nAll blocks done!")


asyncio.run(main())
