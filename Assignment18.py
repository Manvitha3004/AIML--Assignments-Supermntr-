"""
Assignment (20/03/2026)
Assignment Name : Text Challenges
Description :Collect 20 messy sentences and identify slang, emojis, typos; explain preprocessing needed.

"""
import re
import json

# ─────────────────────────────────────────────────────────────
# 1. 20 MESSY SENTENCES
# ─────────────────────────────────────────────────────────────
sentences = [
    "omg dis movie was soooo amazingg!! 😍😍 cant evn",
    "lol ur such a klutz bro 😂 y did u do tht??",
    "i luv pizza 2 much nd i cud eat it evry singel day!!",
    "brb gonna grab cofee, ttyl 😎☕",
    "she's goiing to the storee 2mrw for sum groceries",
    "WTF dude tht was crazyyy af 🤯🔥🔥",
    "i h8 mondays sooo much ughhh 😩😤",
    "plz send me teh report ASAP its vry imprtnt!!",
    "ngl this food hits different 🍔💯 bussin fr fr",
    "cant beleive u didnt come 2 the party smh 😒",
    "tbh i dnt rly care wat ppl think abt me lmao",
    "thsi is the wrst day of mai lyfe no cap 😭😭💀",
    "aye bro u seen the new Spiderman?? its slayin 🕷️✨",
    "she said she wnts 2 meat up latr 2day at thee park",
    "gotta rizz up b4 the date tonite wish me luck 😅🤞",
    "the wether outside is so niec today luving it 🌤️🌸",
    "my wifi keep disconncting every 5 mins so annoyingg 😡",
    "periodt!! tht dress is giving main character energy 💅👑",
    "i forgor to do my hmwrk agin oof rip my grades 📚💀",
    "no wayy they cancelled tha show it was lowkey goated 😤🐐",
]

# ─────────────────────────────────────────────────────────────
# 2. ANNOTATION — Issues per sentence
# ─────────────────────────────────────────────────────────────
annotations = [
    {
        "slang":   ["omg", "dis", "soooo", "evn"],
        "emojis":  ["😍😍"],
        "typos":   ["amazingg", "cant evn (incomplete)"],
        "preprocess": "Expand slang → 'oh my god', 'this', 'so', 'even'; remove emojis; fix repeated chars; complete sentence"
    },
    {
        "slang":   ["lol", "ur", "bro", "y", "tht"],
        "emojis":  ["😂"],
        "typos":   [],
        "preprocess": "Expand: 'laughing out loud', 'your', 'brother/friend', 'why', 'that'; remove emoji"
    },
    {
        "slang":   ["luv", "2", "nd", "cud", "evry"],
        "emojis":  [],
        "typos":   ["singel"],
        "preprocess": "Expand: 'love', 'too', 'and', 'could', 'every'; fix typo 'singel'→'single'"
    },
    {
        "slang":   ["brb", "ttyl"],
        "emojis":  ["😎", "☕"],
        "typos":   ["cofee"],
        "preprocess": "Expand: 'be right back', 'talk to you later'; fix 'cofee'→'coffee'; remove emojis"
    },
    {
        "slang":   ["2mrw", "sum"],
        "emojis":  [],
        "typos":   ["goiing", "storee"],
        "preprocess": "Fix typos 'goiing'→'going', 'storee'→'store'; expand '2mrw'→'tomorrow', 'sum'→'some'"
    },
    {
        "slang":   ["WTF", "tht", "af"],
        "emojis":  ["🤯", "🔥🔥"],
        "typos":   ["crazyyy"],
        "preprocess": "Remove/replace profanity; fix 'crazyyy'→'crazy'; lowercase; remove emojis; expand 'af'→'as hell'"
    },
    {
        "slang":   ["h8", "sooo", "ughhh"],
        "emojis":  ["😩", "😤"],
        "typos":   [],
        "preprocess": "Expand: 'hate', 'so'; remove filler 'ughhh'; remove emojis; normalise repeated chars"
    },
    {
        "slang":   ["plz", "ASAP", "vry", "imprtnt"],
        "emojis":  [],
        "typos":   ["teh"],
        "preprocess": "Fix 'teh'→'the'; expand: 'please', 'as soon as possible', 'very', 'important'"
    },
    {
        "slang":   ["ngl", "hits different", "bussin", "fr fr"],
        "emojis":  ["🍔", "💯"],
        "typos":   [],
        "preprocess": "Expand: 'not gonna lie'; replace 'hits different'→'tastes great'; 'bussin'→'delicious'; 'fr fr'→'for real'; remove emojis"
    },
    {
        "slang":   ["smh", "2"],
        "emojis":  ["😒"],
        "typos":   ["beleive"],
        "preprocess": "Fix 'beleive'→'believe'; expand: 'shaking my head', 'to'; remove emoji"
    },
    {
        "slang":   ["tbh", "dnt", "rly", "wat", "ppl", "lmao"],
        "emojis":  [],
        "typos":   [],
        "preprocess": "Expand: 'to be honest', 'don't', 'really', 'what', 'people', 'laughing my head off'"
    },
    {
        "slang":   ["no cap", "mai", "lyfe"],
        "emojis":  ["😭😭", "💀"],
        "typos":   ["thsi", "wrst"],
        "preprocess": "Fix 'thsi'→'this', 'wrst'→'worst'; expand 'mai'→'my', 'lyfe'→'life', 'no cap'→'honestly'; remove emojis"
    },
    {
        "slang":   ["aye", "bro", "slayin"],
        "emojis":  ["🕷️", "✨"],
        "typos":   [],
        "preprocess": "Expand 'slayin'→'excellent'; remove 'aye'→'hey'; 'bro'→'friend'; remove emojis; fix punctuation"
    },
    {
        "slang":   ["wnts", "2", "latr", "2day", "thee"],
        "emojis":  [],
        "typos":   ["wnts", "meat", "latr", "thee"],
        "preprocess": "Fix 'meat'→'meet', 'thee'→'the'; expand '2'→'to', '2day'→'today', 'latr'→'later'"
    },
    {
        "slang":   ["gotta", "rizz up", "b4", "tonite"],
        "emojis":  ["😅", "🤞"],
        "typos":   [],
        "preprocess": "Expand: 'got to', 'impress/charm', 'before', 'tonight'; remove emojis"
    },
    {
        "slang":   ["luving"],
        "emojis":  ["🌤️", "🌸"],
        "typos":   ["wether", "niec"],
        "preprocess": "Fix 'wether'→'weather', 'niec'→'nice'; expand 'luving'→'loving'; remove emojis"
    },
    {
        "slang":   ["keep"],
        "emojis":  ["😡"],
        "typos":   ["disconncting", "annoyingg"],
        "preprocess": "Fix 'disconncting'→'disconnecting', 'annoyingg'→'annoying'; fix grammar 'keep'→'keeps'; remove emoji"
    },
    {
        "slang":   ["periodt", "giving main character energy"],
        "emojis":  ["💅", "👑"],
        "typos":   ["tht"],
        "preprocess": "Replace 'periodt'→'period/absolutely'; 'giving main character energy'→'looks stunning'; fix 'tht'→'that'; remove emojis"
    },
    {
        "slang":   ["forgor", "agin", "oof", "rip"],
        "emojis":  ["📚", "💀"],
        "typos":   ["forgor", "hmwrk", "agin"],
        "preprocess": "Fix 'forgor'→'forgot', 'hmwrk'→'homework', 'agin'→'again'; remove 'oof'; expand 'rip'→'goodbye to'; remove emojis"
    },
    {
        "slang":   ["no wayy", "tha", "lowkey", "goated"],
        "emojis":  ["😤", "🐐"],
        "typos":   ["wayy"],
        "preprocess": "Fix 'wayy'→'way'; expand 'tha'→'the', 'lowkey'→'somewhat', 'goated'→'greatest of all time'; remove emojis"
    },
]

# ─────────────────────────────────────────────────────────────
# 3. STATISTICS
# ─────────────────────────────────────────────────────────────
total_slang  = sum(len(a["slang"])  for a in annotations)
total_emojis = sum(len(a["emojis"]) for a in annotations)
total_typos  = sum(len(a["typos"])  for a in annotations)

print("=" * 62)
print("  TEXT CHALLENGES — NLP Preprocessing Analysis")
print("=" * 62)
print(f"\n  Total sentences : {len(sentences)}")
print(f"  Slang instances : {total_slang}")
print(f"  Emoji instances : {total_emojis}")
print(f"  Typo instances  : {total_typos}")
print()

for i, (sent, ann) in enumerate(zip(sentences, annotations), 1):
    print(f"[{i:02d}] {sent}")
    if ann["slang"]:   print(f"      SLANG  : {', '.join(ann['slang'])}")
    if ann["emojis"]:  print(f"      EMOJIS : {', '.join(ann['emojis'])}")
    if ann["typos"]:   print(f"      TYPOS  : {', '.join(ann['typos'])}")
    print(f"      FIX    : {ann['preprocess']}")
    print()

# Save JSON for the Word doc builder
with open("/tmp/text_challenges_data.json", "w", encoding="utf-8") as f:
    json.dump({"sentences": sentences, "annotations": annotations,
               "stats": {"slang": total_slang,
                         "emojis": total_emojis,
                         "typos": total_typos}}, f, ensure_ascii=False, indent=2)

print("✅ Data saved → /tmp/text_challenges_data.json")