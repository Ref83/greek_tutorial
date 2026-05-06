#!/usr/bin/env python3
import asyncio
import edge_tts
import subprocess
import os

STORIES = [
    {
        "block": 1,
        "output": "content/vocabulary/shopping/story_block_1.mp3",
        "sentences": [
            ("Κάθε πρωί πηγαίνω στον φούρνο.", "Every morning I go to the bakery."),
            ("Αγοράζω μια φρέσκια φραντζόλα.", "I buy a fresh loaf of bread."),
            ("Παίρνω και δύο ψωμάκια για τα παιδιά.", "I also take two bread rolls for the children."),
            ("Σήμερα υπάρχουν φρέσκα κουλούρια.", "Today there are fresh sesame rings."),
            ("Αγοράζω ένα κουλούρι για τον καφέ μου.", "I buy a sesame ring for my coffee."),
            ("Ο φούρνος έχει και μπαγκέτ.", "The bakery also has baguettes."),
            ("Παίρνω ένα τραγανό μπαγκέτ.", "I take a crispy baguette."),
            ("Τρώω μια πίτα με τυρί.", "I eat a pita with cheese."),
            ("Κόβω το ψωμί σε φέτες.", "I cut the bread into slices."),
            ("Προτιμώ το ψωμί ολικής άλεσης γιατί είναι υγιεινό.", "I prefer whole grain bread because it is healthy."),
            ("Αγοράζω επίσης σταρένιο ψωμί.", "I also buy wheat bread."),
            ("Κάνω τοστ για πρωινό.", "I make toast for breakfast."),
        ],
    },
    {
        "block": 2,
        "output": "content/vocabulary/shopping/story_block_2.mp3",
        "sentences": [
            ("Σήμερα πηγαίνω στο ζαχαροπλαστείο.", "Today I go to the pastry shop."),
            ("Βλέπω πολλά γλυκά στη βιτρίνα.", "I see many sweets in the display case."),
            ("Θέλω ένα κρουασάν βουτύρου.", "I want a butter croissant."),
            ("Αγοράζω και ένα τσουρέκι.", "I also buy a tsoureki."),
            ("Ο μπακλαβάς με καρύδια φαίνεται νόστιμος.", "The baklava with walnuts looks delicious."),
            ("Παίρνω δύο μπισκότα σοκολάτας.", "I take two chocolate biscuits."),
            ("Αγοράζω ένα ντόνατ για τα παιδιά.", "I buy a donut for the children."),
            ("Παραγγέλνω ένα κέικ βανίλιας.", "I order a vanilla cake."),
            ("Η τούρτα σοκολάτας είναι η πιο ακριβή.", "The chocolate cake is the most expensive."),
            ("Η μηλόπιτα μυρίζει κανέλα.", "The apple pie smells like cinnamon."),
            ("Αγοράζω ένα ρολό με κρέμα.", "I buy a cream roll."),
            ("Το κανταΐφι είναι το αγαπημένο μου γλυκό.", "Kataifi is my favorite sweet."),
        ],
    },
    {
        "block": 3,
        "output": "content/vocabulary/shopping/story_block_3.mp3",
        "sentences": [
            ("Πηγαίνω στον φούρνο να κάνω ψώνια.", "I go to the bakery to go shopping."),
            ("Ρωτάω τον αρτοποιό: Πόσο κάνει το ψωμί;", "I ask the baker: How much does the bread cost?"),
            ("Δύο ευρώ το κιλό, λέει.", "Two euros per kilo, he says."),
            ("Θέλω να αγοράσω ψωμί και γλυκά.", "I want to buy bread and sweets."),
            ("Παραγγέλνω μια τούρτα για τα γενέθλια.", "I order a cake for the birthday."),
            ("Ο αρτοποιός ζυγίζει τα μπισκότα.", "The baker weighs the biscuits."),
            ("Αγοράζω μισό κιλό μπισκότα.", "I buy half a kilo of biscuits."),
            ("Η τιμή είναι λογική.", "The price is reasonable."),
            ("Πληρώνω με κάρτα.", "I pay by card."),
            ("Παίρνω την απόδειξη.", "I take the receipt."),
            ("Ο φούρνος βάζει όλα σε μια χάρτινη σακούλα.", "The bakery puts everything in a paper bag."),
            ("Φεύγω χαρούμενος με τη σακούλα μου.", "I leave happy with my bag."),
        ],
    },
]

GREEK_VOICE = "el-GR-AthinaNeural"
ENGLISH_VOICE = "en-US-JennyNeural"
RATE = "-25%"
TEMP_DIR = "/tmp/greek_story_shopping"


async def gen(text, voice, path):
    c = edge_tts.Communicate(text, voice, rate=RATE)
    await c.save(path)


async def generate_story(story):
    block = story["block"]
    output = story["output"]
    sentences = story["sentences"]

    os.makedirs(TEMP_DIR, exist_ok=True)

    silence = f"{TEMP_DIR}/silence.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
         "-t", "3", "-acodec", "libmp3lame", "-q:a", "9", silence],
        check=True, capture_output=True,
    )

    print(f"Generating audio segments for block {block}...")
    for i, (greek, english) in enumerate(sentences):
        for j in range(3):
            path = f"{TEMP_DIR}/b{block}_g{i}_{j}.mp3"
            await gen(greek, GREEK_VOICE, path)
            print(f"  [{i+1}/{len(sentences)}] Greek #{j+1}")
        path_en = f"{TEMP_DIR}/b{block}_e{i}.mp3"
        await gen(english, ENGLISH_VOICE, path_en)
        print(f"  [{i+1}/{len(sentences)}] English")

    list_file = f"{TEMP_DIR}/b{block}_list.txt"
    with open(list_file, "w") as f:
        for i in range(len(sentences)):
            for j in range(3):
                f.write(f"file '{silence}'\n")
                f.write(f"file '{TEMP_DIR}/b{block}_g{i}_{j}.mp3'\n")
            f.write(f"file '{silence}'\n")
            f.write(f"file '{TEMP_DIR}/b{block}_e{i}.mp3'\n")

    print(f"Concatenating block {block}...")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", list_file, "-acodec", "libmp3lame", "-q:a", "4", output],
        check=True,
    )
    print(f"Done → {output}")


async def main():
    for story in STORIES:
        await generate_story(story)
    print("\nAll stories generated!")


asyncio.run(main())
