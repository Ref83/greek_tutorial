#!/usr/bin/env python3
import asyncio
import edge_tts
import subprocess
import os

BLOCKS = [
    {
        "output": "content/vocabulary/health_basic/story_block_1.mp3",
        "story": [
            ("Ο Γιώργης δεν αισθάνεται καλά σήμερα.", "Giorgis doesn't feel well today."),
            ("Έχει υψηλό πυρετό και δυνατό βήχα.", "He has a high fever and a strong cough."),
            ("Τηλεφωνεί στο ιατρείο και κλείνει ένα ραντεβού.", "He calls the clinic and makes an appointment."),
            ("Ο γιατρός τον εξετάζει με προσοχή.", "The doctor examines him carefully."),
            ("Έχεις βαρύ κρυολόγημα, λέει ο γιατρός.", "You have a heavy cold, says the doctor."),
            ("Ο γιατρός του γράφει μια συνταγή.", "The doctor writes him a prescription."),
            ("Ο Γιώργης πηγαίνει στο φαρμακείο και παίρνει το φάρμακο.", "Giorgis goes to the pharmacy and picks up the medicine."),
            ("Ο πόνος στο κεφάλι του σιγά σιγά φεύγει.", "The pain in his head slowly goes away."),
            ("Μετά από τρεις μέρες, αισθάνεται πολύ καλύτερα.", "After three days, he feels much better."),
        ],
    },
    {
        "output": "content/vocabulary/health_basic/story_block_2.mp3",
        "story": [
            ("Η Μαρία αισθάνεται πολύ άρρωστη από χθες.", "Maria has been feeling very sick since yesterday."),
            ("Είναι κουρασμένη και έχει δυνατό πονοκέφαλο.", "She is tired and has a strong headache."),
            ("Έχει επίσης πονόλαιμο και ζαλίζεται.", "She also has a sore throat and feels dizzy."),
            ("Έχει ναυτία και δεν μπορεί να φάει τίποτα.", "She has nausea and cannot eat anything."),
            ("Πηγαίνει στον γιατρό το πρωί.", "She goes to the doctor in the morning."),
            ("Πώς αισθάνεσαι; ρωτάει ο γιατρός.", "How do you feel? asks the doctor."),
            ("Ο γιατρός μετράει τη θερμοκρασία της.", "The doctor takes her temperature."),
            ("Έχετε υψηλή θερμοκρασία, τριάντα οκτώ και μισό βαθμοί, λέει.", "You have a high temperature, thirty eight point five degrees, he says."),
            ("Κάνει μια εξέταση αίματος.", "He does a blood test."),
            ("Έχετε γρίπη, λέει ο γιατρός.", "You have the flu, says the doctor."),
            ("Κάνει στη Μαρία μια ένεση για να της ανακουφίσει τον πόνο.", "He gives Maria an injection to relieve her pain."),
        ],
    },
    {
        "output": "content/vocabulary/health_basic/story_block_3.mp3",
        "story": [
            ("Ο Νίκος έχει μεγάλο φόβο από τους γιατρούς.", "Nikos has a great fear of doctors."),
            ("Κάθε φορά που πηγαίνει στο ιατρείο, αγχώνεται πολύ.", "Every time he goes to the clinic, he gets very anxious."),
            ("Ανησυχεί για την εξέταση και τα αποτελέσματα.", "He worries about the examination and the results."),
            ("Η ανησυχία του είναι μεγάλη.", "His concern is great."),
            ("Προσπαθήστε να είστε ήρεμος, λέει ο γιατρός με ήρεμη φωνή.", "Try to stay calm, says the doctor with a calm voice."),
            ("Πάρτε μια βαθιά αναπνοή.", "Take a deep breath."),
            ("Ο Νίκος χαλαρώνει λίγο.", "Nikos relaxes a little."),
            ("Εμπιστεύεται τον γιατρό του.", "He trusts his doctor."),
            ("Ο γιατρός ανακουφίζει τις ανησυχίες του.", "The doctor soothes his concerns."),
            ("Αντέχεις πολύ καλά, λέει η νοσοκόμα.", "You are handling it very well, says the nurse."),
            ("Μετά την επίσκεψη, ο Νίκος αισθάνεται πολύ καλύτερα.", "After the visit, Nikos feels much better."),
        ],
    },
]

GREEK_VOICE = "el-GR-AthinaNeural"
ENGLISH_VOICE = "en-US-JennyNeural"
RATE = "-25%"
TEMP_DIR = "/tmp/greek_story_health_basic"


async def gen(text, voice, path):
    c = edge_tts.Communicate(text, voice, rate=RATE)
    await c.save(path)


async def generate_block(block_idx, block):
    story = block["story"]
    output = block["output"]
    temp = f"{TEMP_DIR}/block{block_idx}"
    os.makedirs(temp, exist_ok=True)

    silence = f"{temp}/silence.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
         "-t", "3", "-acodec", "libmp3lame", "-q:a", "9", silence],
        check=True, capture_output=True,
    )

    print(f"\n[Block {block_idx}] Generating audio segments...")
    for i, (greek, english) in enumerate(story):
        for j in range(3):
            path = f"{temp}/g{i}_{j}.mp3"
            await gen(greek, GREEK_VOICE, path)
            print(f"  [{i+1}/{len(story)}] Greek #{j+1}")
        path_en = f"{temp}/e{i}.mp3"
        await gen(english, ENGLISH_VOICE, path_en)
        print(f"  [{i+1}/{len(story)}] English")

    list_file = f"{temp}/list.txt"
    with open(list_file, "w") as f:
        for i in range(len(story)):
            for j in range(3):
                f.write(f"file '{silence}'\n")
                f.write(f"file '{temp}/g{i}_{j}.mp3'\n")
            f.write(f"file '{silence}'\n")
            f.write(f"file '{temp}/e{i}.mp3'\n")

    print(f"[Block {block_idx}] Concatenating → {output}")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", list_file, "-acodec", "libmp3lame", "-q:a", "4", output],
        check=True,
    )
    print(f"[Block {block_idx}] Done → {output}")


async def main():
    os.makedirs(TEMP_DIR, exist_ok=True)
    for i, block in enumerate(BLOCKS, start=1):
        await generate_block(i, block)
    print("\nAll 3 blocks done.")


asyncio.run(main())
