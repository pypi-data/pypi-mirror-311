import os
import platform
import shutil
import requests
import tarfile
import zipfile
import py7zr
from tqdm import tqdm

from query2clips.filepaths import ffmpeg_directory

system = platform.system()
arch = platform.machine()


def download_file(url: str, output_file: str) -> str:
    print(f"Downloading {url} to {output_file}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_length = int(r.headers.get("Content-Length", 0))
        with open(output_file, "wb") as f:
            for chunk in tqdm(
                r.iter_content(chunk_size=8192),
                total=total_length / 8192,
                unit="KB",
                unit_scale=True,
            ):
                f.write(chunk)
    return output_file


def ffmpeg_linux():
    ffmpeg_version = "7.0.2"

    if arch == "aarch64":
        arch = "arm64"
    elif arch == "x86_64":
        arch = "amd64"

    ffmpeg_url = f"https://johnvansickle.com/ffmpeg/releases/ffmpeg-{ffmpeg_version}-{arch}-static.tar.xz"
    download_file(ffmpeg_url, "ffmpeg.tar.xz")

    with tarfile.open("ffmpeg.tar.xz") as tar:
        tar.extractall()

    shutil.move(
        f"ffmpeg-{ffmpeg_version}-{arch}-static/ffmpeg",
        os.path.join(ffmpeg_directory, "ffmpeg"),
    )
    shutil.move(
        f"ffmpeg-{ffmpeg_version}-{arch}-static/ffprobe",
        os.path.join(ffmpeg_directory, "ffprobe"),
    )

    os.chmod(os.path.join(ffmpeg_directory, "ffmpeg"), 0o755)
    os.chmod(os.path.join(ffmpeg_directory, "ffprobe"), 0o755)

    os.remove("ffmpeg.tar.xz")
    shutil.rmtree(f"ffmpeg-{ffmpeg_version}-{arch}-static")


def ffmpeg_macos():
    # Official ffmpeg docs provides evermeet.cx as a mirror but it goes down frequently :(.
    # ffmpeg_version = "7.1"

    # ffmpeg_url = f"https://evermeet.cx/ffmpeg/ffmpeg-{ffmpeg_version}.zip"
    # ffprobe_url = f"https://evermeet.cx/ffprobe/ffprobe-{ffmpeg_version}.zip"

    # download_file(ffmpeg_url, "ffmpeg.zip")
    # download_file(ffprobe_url, "ffprobe.zip")

    # with zipfile.ZipFile("ffmpeg.zip", "r") as zip_ref:
    #     zip_ref.extractall(ffmpeg_directory)

    # with zipfile.ZipFile("ffprobe.zip", "r") as zip_ref:
    #     zip_ref.extractall(ffmpeg_directory)

    # Using manually uploaded ffmpeg binaries.
    ffmpeg_url = "https://github.com/hanchchch/query2clips/raw/refs/heads/main/ffmpeg/macos/ffmpeg"
    ffprobe_url = "https://github.com/hanchchch/query2clips/raw/refs/heads/main/ffmpeg/macos/ffprobe"

    download_file(ffmpeg_url, os.path.join(ffmpeg_directory, "ffmpeg"))
    download_file(ffprobe_url, os.path.join(ffmpeg_directory, "ffprobe"))

    os.chmod(os.path.join(ffmpeg_directory, "ffmpeg"), 0o755)
    os.chmod(os.path.join(ffmpeg_directory, "ffprobe"), 0o755)


def ffmpeg_windows():
    ffmpeg_version = "7.0.2"
    ffmpeg_url = f"https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-{ffmpeg_version}-essentials_build.7z"

    download_file(ffmpeg_url, "ffmpeg.7z")

    with py7zr.SevenZipFile("ffmpeg.7z", mode="r") as z:
        z.extractall()

        # Move files
        shutil.move(
            f"ffmpeg-{ffmpeg_version}-essentials_build/bin/ffmpeg.exe",
            "./ffmpeg/ffmpeg.exe",
        )
        shutil.move(
            f"ffmpeg-{ffmpeg_version}-essentials_build/bin/ffprobe.exe",
            "./ffmpeg/ffprobe.exe",
        )

        os.chmod(os.path.join(ffmpeg_directory, "ffmpeg.exe"), 0o755)
        os.chmod(os.path.join(ffmpeg_directory, "ffprobe.exe"), 0o755)

        # Cleanup
        os.remove("ffmpeg.7z")
        shutil.rmtree(f"ffmpeg-{ffmpeg_version}-essentials_build")


def install_ffmpeg():
    os.makedirs(ffmpeg_directory, exist_ok=True)

    if system == "Linux":
        ffmpeg_linux()
    elif system == "Darwin":
        ffmpeg_macos()
    elif system == "Windows":
        ffmpeg_windows()
    else:
        raise ValueError(f"Unsupported operating system: {system}")


def ensure_ffmpeg_installed():
    if os.path.exists(ffmpeg_directory) and len(os.listdir(ffmpeg_directory)) > 0:
        return
    print("Looks like ffmpeg is not installed. Installing ffmpeg...")
    install_ffmpeg()
