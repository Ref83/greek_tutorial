#!/usr/bin/env python3
import asyncio
import edge_tts
import subprocess
import os

BLOCKS = [
    {
        "name": "block_1",
        "story": [
            ("Με λένε Ελένη.", "My name is Eleni."),
            ("Το επίθετό μου είναι Παπαδοπούλου.", "My surname is Papadopoulou."),
            ("Είμαι τριάντα χρονών.", "I am thirty years old."),
            ("Η εθνικότητά μου είναι ελληνική.", "My nationality is Greek."),
            ("Η χώρα μου είναι η Ελλάδα.", "My country is Greece."),
            ("Μένω σε μια μεγάλη πόλη.", "I live in a big city."),
            ("Η διεύθυνσή μου είναι Οδός Αθηνάς πέντε.", "My address is 5 Athenas Street."),
            ("Το τηλέφωνό μου είναι εννέα εννέα ένα δύο τρία.", "My phone number is 99123."),
            ("Στέλνω email στη δουλειά κάθε μέρα.", "I send emails at work every day."),
            ("Είμαι παντρεμένη με έναν υπέροχο άνδρα.", "I am married to a wonderful man."),
            ("Ο αδελφός μου είναι ελεύθερος.", "My brother is single."),
            ("Γεννήθηκα στην Αθήνα.", "I was born in Athens."),
        ],
    },
    {
        "name": "block_2",
        "story": [
            ("Η οικογένειά μου είναι πολυπληθής.", "My family is large."),
            ("Ο σύζυγός μου λέγεται Γιώργης.", "My husband's name is Giorgis."),
            ("Η γυναίκα του φίλου μου είναι δασκάλα.", "My friend's wife is a teacher."),
            ("Έχουμε τρία παιδιά.", "We have three children."),
            ("Ο αδελφός μου ζει στην Αθήνα.", "My brother lives in Athens."),
            ("Η αδελφή μου είναι γιατρός.", "My sister is a doctor."),
            ("Οι γονείς μου μένουν στην Κρήτη.", "My parents live in Crete."),
            ("Ο πατέρας μου λέγεται Μιχάλης.", "My father's name is Michalis."),
            ("Η μητέρα μου είναι πολύ καλή μαγείρισσα.", "My mother is a very good cook."),
            ("Κατάγομαι από τη Θεσσαλονίκη.", "I come from Thessaloniki."),
            ("Τώρα μένω στη Λεμεσό.", "Now I live in Limassol."),
            ("Μιλώ δύο γλώσσες, ελληνικά και αγγλικά.", "I speak two languages, Greek and English."),
        ],
    },
    {
        "name": "block_3",
        "story": [
            ("Το επάγγελμά μου είναι μηχανικός.", "My profession is engineer."),
            ("Η εργασία μου είναι πολύ ενδιαφέρουσα.", "My work is very interesting."),
            ("Δουλεύω κάθε μέρα από τις εννέα το πρωί.", "I work every day from nine in the morning."),
            ("Η εταιρεία μου έχει πολλούς υπαλλήλους.", "My company has many employees."),
            ("Πήγα σε ένα καλό σχολείο στην Αθήνα.", "I went to a good school in Athens."),
            ("Μετά σπούδασα στο πανεπιστήμιο.", "Then I studied at the university."),
            ("Σπουδάζω τώρα ελληνική γλώσσα.", "I am studying the Greek language now."),
            ("Τα χόμπι μου είναι η φωτογραφία και η μουσική.", "My hobbies are photography and music."),
            ("Μιλώ ελληνικά, αγγλικά και λίγο γαλλικά.", "I speak Greek, English, and a little French."),
            ("Μαθαίνω νέες λέξεις κάθε μέρα.", "I learn new words every day."),
            ("Το διαβατήριό μου είναι ελληνικό.", "My passport is Greek."),
            ("Η ταυτότητά μου έχει όλες τις πληροφορίες μου.", "My ID card has all my information."),
        ],
    },
]

GREEK_VOICE = "el-GR-AthinaNeural"
ENGLISH_VOICE = "en-US-JennyNeural"
RATE = "-25%"
TEMP_DIR = "/tmp/greek_story_personal_information"
OUTPUT_DIR = "content/vocabulary/personal_information"


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
