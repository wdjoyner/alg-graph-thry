"""Generate narration, inspectable previews, and the final encoded movie."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import re
import subprocess
import textwrap
import wave

from timeline import BEAT, CHAPTERS, FPS

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
WIDTH, HEIGHT = 1920, 1080


def run(*args):
    subprocess.run([str(x) for x in args], check=True)


def timestamp(seconds):
    ms = round(seconds * 1000)
    return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"


def narration(model):
    from piper import PiperVoice, SynthesisConfig
    voice = PiperVoice.load(model)
    sections = re.findall(r"^### .+\n([^#\n]+)", (ROOT/"narration.md").read_text(), re.M)
    assert len(sections) == 4 * len(CHAPTERS)
    rate = voice.config.sample_rate
    captions = []
    with wave.open(str(BUILD/"narration.wav"), "wb") as wav:
        wav.setparams((1,2,rate,0,"NONE","not compressed"))
        for i, paragraph in enumerate(sections):
            sentences = re.split(r"(?<=[.!?]) +", paragraph.strip())
            audio = []
            for sentence in sentences:
                spoken = (sentence.replace("Kociemba", "Koh chem bah")
                          .replace("Zassenhaus", "Zassen house")
                          .replace("Mathieu", "Mat you")
                          .replace("Cayley", "Kay lee")
                          .replace("x d", "x D"))
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
    (BUILD/"complement-regularity.srt").write_text("\n\n".join(captions)+"\n")


def clip(scene):
    return BUILD/"media"/"videos"/"scenes"/"1080p30"/f"{scene}.mp4"


def probe(path):
    return json.loads(subprocess.check_output([
        "ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))


def inspect():
    preview = BUILD/"inspection"
    preview.mkdir(exist_ok=True)
    for scene, _ in CHAPTERS:
        beats = 4
        path = clip(scene)
        info = probe(path)["streams"][0]
        assert (info["width"], info["height"], info["r_frame_rate"]) == (WIDTH,HEIGHT,"30/1")
        for i in range(beats):
            run("ffmpeg","-v","error","-y","-threads",2,"-ss",str(i*BEAT+13),"-i",path,
                "-frames:v","1","-vf","scale=960:540","-threads",1,preview/f"{scene}-{i+1}.png")
        print(f"{scene}: {info['nb_frames']} frames", flush=True)


def assemble():
    manifest = BUILD/"clips.ffconcat"
    entries = ["ffconcat version 1.0"]
    for scene, _ in CHAPTERS:
        beats = 4
        raw = clip(scene)
        info = probe(raw)["streams"][0]
        assert (info["width"],info["height"],info["r_frame_rate"]) == (WIDTH,HEIGHT,"30/1")
        duration = beats*BEAT
        frames = int(info["nb_frames"])
        assert abs(frames-duration*FPS) < FPS//2
        normalized = raw
        if frames != duration*FPS:
            normalized = BUILD/f"{scene}.mp4"
            run("ffmpeg","-v","error","-y","-i",raw,
                "-vf","tpad=stop_mode=clone:stop_duration=0.5",
                "-frames:v",duration*FPS,"-an","-c:v","libx264","-threads",2,
                "-preset","fast","-crf","18","-pix_fmt","yuv420p",normalized)
        entries.append(f"file '{normalized.relative_to(BUILD).as_posix()}'")
    manifest.write_text("\n".join(entries)+"\n")
    chapters = BUILD/"chapters.ffmetadata"
    metadata = [";FFMETADATA1", "title=Which symmetric groups have a complement?"]
    start = 0
    for _, title in CHAPTERS:
        beats = 4
        end = start + BEAT*beats
        metadata += ["[CHAPTER]", "TIMEBASE=1/1", f"START={start}", f"END={end}", f"title={title}"]
        start = end
    chapters.write_text("\n".join(metadata)+"\n")
    run("ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",manifest,
        "-i",BUILD/"narration.wav","-i",BUILD/"complement-regularity.srt","-i",chapters,
        "-map","0:v","-map","1:a","-map","2:s","-map_metadata","3","-map_chapters","3",
        "-c:v","copy","-c:a","aac","-b:a","128k","-af","volume=-3dB","-c:s","mov_text",
        "-metadata:s:s:0","language=eng","-disposition:s:0","0",
        "-movflags","+faststart",ROOT/"complement-regularity.mp4")


def verify():
    import srt

    path = ROOT / "complement-regularity.mp4"
    info = json.loads(subprocess.check_output([
        "ffprobe","-v","error","-show_streams","-show_chapters",
        "-show_format","-of","json",str(path)
    ]))
    video, audio, subtitles = [
        next(stream for stream in info["streams"] if stream["codec_type"] == kind)
        for kind in ("video","audio","subtitle")
    ]
    duration = BEAT * 4 * len(CHAPTERS)
    assert (video["width"],video["height"]) == (WIDTH,HEIGHT)
    assert Fraction(video["avg_frame_rate"]) == FPS
    assert int(video["nb_frames"]) == duration * FPS
    assert video["codec_name"] == "h264" and audio["codec_name"] == "aac"
    assert abs(float(audio["duration"])-duration) < .05
    assert abs(float(info["format"]["duration"])-duration) < .05
    assert subtitles["tags"]["language"] == "eng"
    assert [round(float(chapter["start_time"])) for chapter in info["chapters"]] == [
        i*4*BEAT for i in range(len(CHAPTERS))
    ]
    caps = list(srt.parse((ROOT/"complement-regularity.srt").read_text()))
    extracted = subprocess.check_output([
        "ffmpeg","-v","error","-i",str(path),"-map","0:s:0","-f","srt","pipe:1"
    ]).decode("utf-8")
    assert list(srt.parse(extracted)) == caps
    assert caps[0].start.total_seconds() >= 0
    for i, cue in enumerate(caps):
        assert cue.start < cue.end and cue.end.total_seconds() <= duration
        assert not i or caps[i-1].end <= cue.start
    # Measure decoded narration separately in each chapter.
    for i,(scene, _) in enumerate(CHAPTERS):
        levels = subprocess.run([
            "ffmpeg","-hide_banner","-ss",str(i*4*BEAT),"-i",str(path),
            "-t",str(4*BEAT),"-map","0:a:0","-af","volumedetect","-f","null","-"
        ],capture_output=True,text=True,check=True).stderr
        level = float(re.search(r"mean_volume: (-?\d+(?:\.\d+)?) dB",levels)[1])
        assert -35 < level < -8, (scene,level)
    print(f"Verified {duration}s, {WIDTH}×{HEIGHT}, {FPS} fps, six narrated chapters, "
          f"and {len(caps)} matching English subtitle cues.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("narrate","inspect","assemble","verify"))
    parser.add_argument("--model",type=Path)
    args = parser.parse_args()
    BUILD.mkdir(exist_ok=True)
    if args.action == "narrate":
        if args.model is None:
            parser.error("narrate requires --model")
        narration(args.model)
    elif args.action == "inspect":
        inspect()
    elif args.action == "assemble":
        assemble()
    else:
        verify()


if __name__ == "__main__":
    main()
