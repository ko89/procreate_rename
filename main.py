from zipfile import ZipFile
import datetime
from pathlib import Path
import shutil
import argparse


# Try to determine the date the file was created
# TODO: find a better way than checking video segments
def get_create_date(proc_file: Path):
    archive = ZipFile(proc_file, "r")
    # Check the creation date of the first video segment
    # Newer files use mp4
    segment_filename = "video/segments/segment-1.mp4"

    # Check if its an older file with m4v video
    if "video/segments/segment-1.m4v" in archive.namelist():
        segment_filename = "video/segments/segment-1.m4v"

    try:
        date_tuple = archive.getinfo(segment_filename).date_time
        return datetime.date(date_tuple[0], date_tuple[1], date_tuple[2])
    except KeyError:
        print("Could not determine creation date!")
        return None


# create a file name in the format "./output_directory/{date}_{oldname}_{counter}.procreate"
def create_filename(out_path, old_name, create_date, counter):
    if counter is None:
        return Path(out_path, f"{str(create_date)}_{old_name}.procreate")

    return Path(out_path, f"{str(create_date)}_{old_name}_{counter:02}.procreate")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        nargs=1,
        type=Path,
        help="input directory containing procreate files",
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs=1,
        type=Path,
        help="output directory where renamed files will be copied",
    )

    args = parser.parse_args()
    in_path = args.input[0]
    out_path = args.output[0]

    for proc_file in in_path.glob("*.procreate"):
        print(f"Checking file: {proc_file}")
        create_date = get_create_date(proc_file)

        if create_date is None:
            print("Skipping file..")
            continue

        # If there are multiple files with the same name, created on the same date,
        # add/increase the counter at the end of the filename

        proc_file_renamed = create_filename(out_path, proc_file.stem, create_date, None)
        counter = 1
        while proc_file_renamed.absolute().exists():
            counter = counter + 1
            proc_file_renamed = create_filename(
                out_path, proc_file.stem, create_date, counter
            )

        print(f"Copying file to: {proc_file_renamed.absolute()}")
        if not proc_file_renamed.absolute().exists():
            shutil.copy(src=proc_file.absolute(), dst=proc_file_renamed.absolute())


if __name__ == "__main__":
    main()
