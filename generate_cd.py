from tqdm import tqdm
from pydub import AudioSegment
import os


def main():
    data_folder = os.path.join(os.getcwd(), "data")

    paths = os.listdir(data_folder)
    paths = list(map(lambda x: os.path.join(data_folder, x), paths))
    paths = list(filter(lambda x: os.path.isfile(x), paths))

    raws = {}

    def process_path(path):
        file_name = os.path.split(path)[-1]
        page_num = int(file_name[4:7])
        segment = AudioSegment.from_mp3(path)
        raws[page_num] = segment

    print("Processing paths to audio.")
    for path in tqdm(paths[:30 + 1]):
        process_path(path)

    num_divisions = 3
    num_pages = 10

    print("Building and exporting audio files.")
    for division in tqdm(range(num_divisions)):
        div_audio = AudioSegment.empty()
        for page in range(num_pages):
            target = division * num_pages + page
            if not target in raws:
                continue
            div_audio = div_audio.append(raws[target], 0)
        div_audio.export(f"out/division-{division}.mp3", format="mp3")


if __name__ == "__main__":
    main()
