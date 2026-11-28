"""Generate narration, inspectable previews, and the final encoded movie."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import textwrap
import wave

from credits_timing import CREDITS_SECONDS

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
WIDTH, HEIGHT, FPS = 1920, 1080, 30
BEAT = 17
CHAPTERS = (
    ("FanoSteiner", "The Fano plane and Steiner systems", 4),
    ("ProjectiveLine", "The projective-line construction", 4),
    ("CurtisKitten", "Curtis’s kitten", 4),
    ("ConwayMINIMOG", "Conway’s MINIMOG and the tetracode", 4),
    ("JohnsonGraph", "Johnson graphs and equitable partitions", 4),
    ("Blackjack", "Mathematical blackjack", 6),
)


def run(*args):
    subprocess.run([str(x) for x in args], check=True)


def timestamp(seconds):
    ms = round(seconds * 1000)
    return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"


def narration(model):
    from piper import PiperVoice, SynthesisConfig
    voice = PiperVoice.load(model)
    sections = re.findall(r"^### .+\n([^#\n]+)", (ROOT/"narration.md").read_text(), re.M)
    assert len(sections) == sum(c[2] for c in CHAPTERS)
    rate = voice.config.sample_rate
    captions = []
    with wave.open(str(BUILD/"narration.wav"), "wb") as wav:
        wav.setparams((1,2,rate,0,"NONE","not compressed"))
        for i, paragraph in enumerate(sections):
            sentences = re.split(r"(?<=[.!?]) +", paragraph.strip())
            audio = []
            for sentence in sentences:
                spoken = (sentence.replace("hexads", "hex adds")
                          .replace("hexad", "hex add")
                          .replace("tetracode", "tetra code")
                          .replace("MINIMOG", "mini mog")
                          .replace("Curtis’s", "Curtis's"))
                chunks = voice.synthesize(spoken, SynthesisConfig(length_scale=.96, noise_scale=.3))
                audio.append(b"".join(c.audio_int16_bytes for c in chunks))
            lead = round(rate*.48)
            gap = round(rate*.15)
            total = lead + sum(len(a)//2 for a in audio) + gap*(len(audio)-1)
            if total > rate*(BEAT-.25):
                factor = (rate*(BEAT-.32)-lead-gap*(len(audio)-1))/sum(len(a)//2 for a in audio)
                converted = []
                for pcm in audio:
                    result = subprocess.run(["ffmpeg","-v","error","-f","s16le","-ar",str(rate),
                        "-ac","1","-i","pipe:0","-af",f"atempo={1/factor:.6f}","-f","s16le","pipe:1"],
                        input=pcm,capture_output=True,check=True)
                    converted.append(result.stdout)
                audio = converted
            cursor = lead
            wav.writeframes(b"\0\0"*lead)
            for j, (sentence, pcm) in enumerate(zip(sentences, audio)):
                start = i*BEAT + cursor/rate
                wav.writeframes(pcm)
                cursor += len(pcm)//2
                end = i*BEAT + cursor/rate
                lines = textwrap.wrap(sentence, 41)
                groups = [lines[k:k+2] for k in range(0,len(lines),2)]
                characters = sum(sum(map(len, group)) for group in groups)
                elapsed = start
                for group in groups:
                    until = elapsed + (end-start)*sum(map(len, group))/characters
                    captions.append(f"{len(captions)+1}\n{timestamp(elapsed)} --> {timestamp(until)}\n"
                                    + "\n".join(group))
                    elapsed = until
                if j < len(audio)-1:
                    wav.writeframes(b"\0\0"*gap)
                    cursor += gap
            assert cursor <= rate*BEAT, (i,cursor/rate)
            wav.writeframes(b"\0\0"*(rate*BEAT-cursor))
            print(f"Beat {i+1:02}: spoken through {cursor/rate:.2f}s", flush=True)
    (BUILD/"minimogs-blackjack.srt").write_text("\n\n".join(captions)+"\n")


def clip(scene):
    return BUILD/"media"/"videos"/"scenes"/"1080p30"/f"{scene}.mp4"


def probe(path):
    return json.loads(subprocess.check_output([
        "ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))


def inspect():
    preview = BUILD/"inspection"
    preview.mkdir(exist_ok=True)
    for scene, _, beats in CHAPTERS:
        path = clip(scene)
        info = probe(path)["streams"][0]
        assert (info["width"], info["height"], info["r_frame_rate"]) == (WIDTH,HEIGHT,"30/1")
        for i in range(beats):
            run("ffmpeg","-v","error","-y","-ss",str(i*BEAT+15.7),"-i",path,
                "-frames:v","1","-vf","scale=960:540",preview/f"{scene}-{i+1}.png")
        print(f"{scene}: {info['nb_frames']} frames", flush=True)
    run("ffmpeg", "-v", "error", "-y", "-ss", "3", "-i", clip("EndCredits"),
        "-frames:v", "1", "-vf", "scale=960:540", preview/"EndCredits.png")


def normalize_clip(scene, duration):
    raw = clip(scene)
    info = probe(raw)["streams"][0]
    assert (info["width"], info["height"], info["r_frame_rate"]) == (WIDTH, HEIGHT, "30/1")
    assert abs(int(info["nb_frames"]) - duration*FPS) < FPS//2
    normalized = BUILD/f"{scene}.mp4"
    run("ffmpeg","-v","error","-y","-i",raw,"-vf","tpad=stop_mode=clone:stop_duration=0.5",
        "-t",duration,"-an","-c:v","libx264","-threads",3,"-preset","fast","-crf","18",
        "-pix_fmt","yuv420p",normalized)


def assemble():
    for scene, _, beats in CHAPTERS:
        normalize_clip(scene, beats*BEAT)
    normalize_clip("EndCredits", CREDITS_SECONDS)
    mux()


def mux():
    manifest = BUILD/"clips.ffconcat"
    entries = ["ffconcat version 1.0"]
    schedule = [(scene, title, beats*BEAT) for scene, title, beats in CHAPTERS]
    schedule.append(("EndCredits", "Credits", CREDITS_SECONDS))
    for scene, _, _ in schedule:
        entries.append(f"file '{scene}.mp4'")
    manifest.write_text("\n".join(entries)+"\n")
    chapters = BUILD/"chapters.ffmetadata"
    metadata = [";FFMETADATA1", "title=MINIMOGs and Mathematical Blackjack"]
    start = 0
    for _, title, duration in schedule:
        end = start + duration
        metadata += ["[CHAPTER]", "TIMEBASE=1/1", f"START={start}", f"END={end}", f"title={title}"]
        start = end
    chapters.write_text("\n".join(metadata)+"\n")
    run("ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",manifest,
        "-i",BUILD/"narration.wav","-i",BUILD/"minimogs-blackjack.srt","-i",chapters,
        "-map","0:v","-map","1:a","-map","2:s","-map_metadata","3","-map_chapters","3",
        "-c:v","copy","-c:a","aac","-b:a","128k","-af",f"volume=-3dB,apad=pad_dur={CREDITS_SECONDS}","-c:s","mov_text",
        "-metadata:s:s:0","language=eng","-disposition:s:0","0",
        "-movflags","+faststart",ROOT/"minimogs-blackjack.mp4")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("narrate","inspect","assemble"))
    parser.add_argument("--model",type=Path)
    args = parser.parse_args()
    BUILD.mkdir(exist_ok=True)
    if args.action == "narrate":
        if args.model is None:
            parser.error("narrate requires --model")
        narration(args.model)
    elif args.action == "inspect":
        inspect()
    else:
        assemble()


if __name__ == "__main__":
    main()
