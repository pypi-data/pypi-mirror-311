#!/usr/bin/env python3

# Execute with
# $ python3 -m query2clips

import os
import sys

if __package__ is None and not getattr(sys, "frozen", False):
    # direct call of __main__.py
    import os.path

    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

from dotenv import load_dotenv
import argparse

from query2clips import Query2Clips
from query2clips.install_ffmpeg import ensure_ffmpeg_installed

load_dotenv()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str)
    parser.add_argument("--output-dir", type=str, default="outputs")
    parser.add_argument("--video-size", type=int, default=360)
    parser.add_argument("--search-offset", type=int, default=0)
    parser.add_argument("--search-limit", type=int, default=10)
    parser.add_argument("--adjust-to-keyframes", default=False, action="store_true")
    parser.add_argument("--searcher", type=str, default="youtube", choices=["youtube"])
    parser.add_argument("--downloader", type=str, default="yt_dlp", choices=["yt_dlp"])
    parser.add_argument("--clipper", type=str, default="ffmpeg", choices=["ffmpeg"])
    parser.add_argument(
        "--captioner", type=str, default="none", choices=["none", "gemini"]
    )
    args = parser.parse_args()

    ensure_ffmpeg_installed()
    output_dir = os.path.join(os.path.abspath(args.output_dir), args.query)

    outputs = []
    pipeline = Query2Clips(
        output_dir=output_dir,
        searcher=args.searcher,
        downloader=args.downloader,
        clipper=args.clipper,
        captioner=None if args.captioner == "none" else args.captioner,
        adjust_to_keyframes=args.adjust_to_keyframes,
    )
    for output in pipeline(
        args.query,
        args.search_limit,
        args.search_offset,
        args.video_size,
    ):
        outputs.append(output)

    sum_filesize = sum(output["info"]["size"] for output in outputs)
    sum_duration = sum(output["info"]["duration"] for output in outputs)
    print(f"generated {len(outputs)} clips")
    print(f"sum filesize: {sum_filesize/(1024**2):.2f} MB")
    print(f"sum duration: {sum_duration:.2f} seconds")
