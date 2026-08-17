import json
import os
import re
import shutil
import unicodedata

import imageio_ffmpeg
import whisper

BASE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(BASE, "static", "audio", "leonora.mp3")
OUT = os.path.join(BASE, "static", "lyrics_timestamps.json")

LYRIC_LINES = [
    "'Tong alay kong harana, para sa dalagang",
    "Walang kasingganda, amoy-rosas ang halimuyak",
    "Kung nanaisin ng tadhanang mapanlinlang",
    "'Di hahayaang mawala pa",
    "'Tong liham na umaasang mata mo ang makabasa",
    "Handang gawin lahat, maging pamilya'y liligawan",
    "Ngayon lang nakadama ng wagas na pagkamangha",
    "Hiling ko lang naman na",
    "Tayo na sanang dalawa ang siyang huli at ang umpisa",
    "Papatunayang ang unang pag-ibig ay 'di mawawala",
    "Nakailang tula na, ba't tila 'di napupuna?",
    "Ang tangi kong hiling, hanggang dulo ikaw ang kapiling",
    "Kung puwede lang, hanggang pangmagpakailanman",
    "Hinding-hindi na papakawalan kailanman",
    "Ang dating tamis ng pagsasama, nasa'n na? (Hinahanap-hanap ka, whoa)",
    "Ba't sa 'ting dal'wa, ako na lang ang natira? (Sana'y magkita pa)",
    "Tinig mong kay ganda, maririnig pa ba?",
    "Handang tahaking mag-isa kahit wala ka na",
    "Kung nasa'n ka man, nawa ay masaya ka na (palalayain ka, whoa)",
    "Kahit na 'di na tayo magsasama pa (mahal pa rin kita)",
    "Dinggin mo lang ang hiling na mag-iingat ka",
    "Oh, Leonora kong sinta, ah",
]


def norm(word):
    word = unicodedata.normalize("NFKD", word)
    word = "".join(c for c in word if not unicodedata.combining(c))
    word = word.lower()
    word = re.sub(r"[^a-z0-9\u00f1\u00d1\u2019']", "", word)
    return word


def close(a, b):
    if not a or not b:
        return False
    if a == b or a in b or b in a:
        return True
    if len(a) > 3 and len(b) > 3:
        # cheap edit-distance for small strings
        m, n = len(a), len(b)
        prev = list(range(n + 1))
        for i in range(1, m + 1):
            cur = [i] + [0] * n
            for j in range(1, n + 1):
                cost = 0 if a[i - 1] == b[j - 1] else 1
                cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
            prev = cur
        return prev[n] <= 2
    return False


def main():
    # make bundled ffmpeg discoverable by whisper (it calls "ffmpeg" literally)
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = os.path.dirname(ffmpeg_exe)
    ffmpeg_target = os.path.join(ffmpeg_dir, "ffmpeg.exe")
    if not os.path.exists(ffmpeg_target):
        shutil.copy(ffmpeg_exe, ffmpeg_target)
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
    os.environ["FFMPEG_BINARY"] = ffmpeg_target

    print("Loading Whisper model...")
    model = whisper.load_model("base")

    print("Transcribing", AUDIO)
    result = model.transcribe(AUDIO, word_timestamps=True, language="tl", verbose=False)

    words = []
    for seg in result.get("segments", []):
        for w in seg.get("words", []):
            if w.get("word") is None or w.get("start") is None:
                continue
            words.append((float(w["start"]), norm(w["word"])))

    print("Whisper words:", len(words))
    print("Sample:", [(round(s, 1), t) for s, t in words[:12]])

    # Whisper's text for sung vocals is unreliable, but its word *timestamps*
    # still track when vocals occur. Spread the lyric lines across the detected
    # vocal timeline by quantile so they progress in order with the song.
    word_times = sorted(w[0] for w in words)
    n = len(word_times)
    N = len(LYRIC_LINES)
    times = []
    if n == 0:
        times = [round(i * 5.0, 2) for i in range(N)]
    else:
        for i in range(N):
            q = i / (N - 1) if N > 1 else 0
            idx = min(n - 1, round(q * (n - 1)))
            times.append(round(word_times[idx], 2))

    data = {
        "source": "whisper-base-timestamps",
        "lines": len(times),
        "times": times,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Wrote", OUT)
    print("Times:", times)


if __name__ == "__main__":
    main()
