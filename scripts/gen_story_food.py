#!/usr/bin/env python3
import asyncio
import edge_tts
import subprocess
import os

BLOCKS = [
    {
        "name": "block_1",
        "story": [
            ("Σήμερα θέλω να φτιάξω ένα κέικ.", "Today I want to make a cake."),
            ("Βγάζω το αλεύρι, τη ζάχαρη και το αλάτι από το ντουλάπι.", "I take out the flour, sugar, and salt from the cupboard."),
            ("Χρειάζομαι επίσης γάλα, αυγά και βούτυρο.", "I also need milk, eggs, and butter."),
            ("Ανοίγω το ψυγείο και βγάζω τρία αυγά.", "I open the fridge and take out three eggs."),
            ("Λιώνω το βούτυρο σε χαμηλή φωτιά.", "I melt the butter on low heat."),
            ("Ανακατεύω το αλεύρι με τη ζάχαρη και τη μαγειρική σόδα.", "I mix the flour with the sugar and baking soda."),
            ("Προσθέτω βανίλια και λίγη κανέλα για άρωμα.", "I add vanilla and a little cinnamon for aroma."),
            ("Χτυπάω τα αυγά με το γάλα και το λιωμένο βούτυρο.", "I beat the eggs with the milk and the melted butter."),
            ("Ενώνω τα υγρά με τα στερεά υλικά και ανακατεύω καλά.", "I combine the wet with the dry ingredients and mix well."),
            ("Βάζω τη ζύμη στο ταψί και τη βάζω στον φούρνο.", "I put the batter in the pan and put it in the oven."),
            ("Μετά από μισή ώρα, το κέικ είναι έτοιμο!", "After half an hour, the cake is ready!"),
            ("Το πασπαλίζω με ζάχαρη άχνη και λίγη κανέλα.", "I sprinkle it with powdered sugar and a little cinnamon."),
        ],
    },
    {
        "name": "block_2",
        "story": [
            ("Σήμερα ξυπνάω νωρίς και πηγαίνω στην κουζίνα.", "Today I wake up early and go to the kitchen."),
            ("Πρώτα φτιάχνω ένα φλιτζάνι καφέ.", "First I make a cup of coffee."),
            ("Βάζω λίγη ζάχαρη στον καφέ μου.", "I put a little sugar in my coffee."),
            ("Μετά ετοιμάζω ομελέτα με τυρί για πρωινό.", "Then I prepare an omelette with cheese for breakfast."),
            ("Χτυπάω δύο αυγά με λίγο αλάτι.", "I beat two eggs with a little salt."),
            ("Τρώω την ομελέτα με φρέσκο ψωμί.", "I eat the omelette with fresh bread."),
            ("Το μεσημέρι μαγειρεύω σούπα και σαλάτα.", "At noon I cook soup and salad."),
            ("Για σαλάτα χρησιμοποιώ λίγο ελαιόλαδο.", "For the salad I use a little olive oil."),
            ("Το βράδυ φτιάχνω μακαρόνια με τυρί.", "In the evening I make pasta with cheese."),
            ("Τρώω επίσης γιαούρτι με μέλι για επιδόρπιο.", "I also eat yogurt with honey for dessert."),
            ("Πριν κοιμηθώ, πίνω ένα φλιτζάνι τσάι.", "Before going to sleep, I drink a cup of tea."),
            ("Ήταν μια νόστιμη μέρα!", "It was a delicious day!"),
        ],
    },
    {
        "name": "block_3",
        "story": [
            ("Σήμερα θέλω να μαγειρέψω μια παραδοσιακή ελληνική συνταγή.", "Today I want to cook a traditional Greek recipe."),
            ("Πρώτα κόβω τα λαχανικά σε μικρά κομμάτια.", "First I cut the vegetables into small pieces."),
            ("Ζεσταίνω το τηγάνι και προσθέτω λίγο ελαιόλαδο.", "I heat the pan and add a little olive oil."),
            ("Τηγανίζω τα λαχανικά για πέντε λεπτά.", "I fry the vegetables for five minutes."),
            ("Ανακατεύω συχνά για να μην κολλήσουν.", "I stir often so they don't stick."),
            ("Προσθέτω αλάτι και τα μπαχαρικά.", "I add salt and the spices."),
            ("Βάζω νερό στην κατσαρόλα και το βράζω.", "I put water in the pot and boil it."),
            ("Βράζω τα μακαρόνια σύμφωνα με τη συνταγή.", "I boil the pasta according to the recipe."),
            ("Παράλληλα, ψήνω ψωμί στον φούρνο.", "At the same time, I bake bread in the oven."),
            ("Ετοιμάζω τη ζύμη για το ψωμί από νωρίς.", "I prepare the bread dough early."),
            ("Ζυμώνω καλά και αφήνω τη ζύμη να φουσκώσει.", "I knead well and let the dough rise."),
            ("Στο τέλος, το φαγητό είναι έτοιμο και η κουζίνα μυρίζει υπέροχα!", "In the end, the food is ready and the kitchen smells wonderful!"),
        ],
    },
]

GREEK_VOICE = "el-GR-AthinaNeural"
ENGLISH_VOICE = "en-US-JennyNeural"
RATE = "-25%"
TEMP_DIR = "/tmp/greek_story_food"
OUTPUT_DIR = "content/vocabulary/food"


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
