import os
import json
import auditok

from zipfile import ZipFile

ENERGY_THRESHOLD = 55
OUTPUT_DIRECTORY = "data"
AUDIO_CLIPS_JSON = "clips.json"
TEST_FILE = "audiomass-output.wav"


def zip_files(directry: str) -> None:
    with ZipFile(f"{directry}.zip", "w") as zf:
        for dirname, subdirs, files in os.walk(directry):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename), arcname=filename)


def create_out_directory(file: str) -> str:
    filename = os.path.split(file)[-1].split(".")[0]

    directory = os.path.join(OUTPUT_DIRECTORY, filename)

    try:
        os.mkdir(directory)
    except FileExistsError:
        pass

    return directory


def main():
    d = {"input_file": TEST_FILE, "audio_clips": []}
    directory = create_out_directory(TEST_FILE)

    audio_regions = auditok.split(TEST_FILE, energy_threshold=ENERGY_THRESHOLD)

    for i, r in enumerate(audio_regions):
        filename = r.save(f"{os.path.join(directory, TEST_FILE)}_{i}.wav")

        d["audio_clips"].append(
            {
                "clip_file": filename,
                "start_time": r.meta.start,
                "end_time": r.meta.end,
                "duration": r.meta.end - r.meta.start,
            }
        )

    with open(os.path.join(directory, AUDIO_CLIPS_JSON), "w") as file:
        file.write(json.dumps(d))

    zip_files(directory)


if __name__ == "__main__":
    main()
