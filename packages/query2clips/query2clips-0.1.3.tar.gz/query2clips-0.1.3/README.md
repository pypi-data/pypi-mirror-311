# Query2Clips

Query2Clips is a tool to generate clips and captions based on a query.

## Installation

```bash
pip install query2clips
```

## Usage

```bash
python3 -m query2clips --query "a cat playing piano"
```

To caption the clips, set `GEMINI_API_KEY` in `.env` file (or directly in environment variables) and use `--captioner gemini` option.
You might need to install `google-generativeai` package first.

```bash
pip install google-generativeai
python3 -m query2clips --query "a cat playing piano" --captioner gemini
```

Outputs are saved in `outputs` directory.

```
outputs
├── a cat playing piano.csv
├── clips
│   ├── 6hgEJ23Hv_Y
│   │   ├── 0001.json
│   │   └── 0001.mp4
│   ├── G1mWfvbcjcI
│   │   ├── 0001.json
│   │   ├── 0001.mp4
│   │   ├── 0002.json
│   │   ├── 0002.mp4
│   │   ├── 0003.json
│   │   ├── 0003.mp4
│   │   ├── 0004.json
│   │   └── 0004.mp4
│   ├── J---aiyznGQ
│   │   ├── 0001.json
│   │   ├── 0001.mp4
│   │   ├── 0002.json
│   │   └── 0002.mp4
│   └── Yc-5P8-xLWU
│       ├── 0001.json
│       ├── 0001.mp4
│       ├── 0002.json
│       └── 0002.mp4
└── videos
    ├── 6hgEJ23Hv_Y.mp4
    ├── G1mWfvbcjcI.mp4
    ├── J---aiyznGQ.mp4
    └── Yc-5P8-xLWU.mp4
```

The `<query>.csv` file contains the fetched urls of the videos.
The `videos` directory contains the downloaded original videos.
The `clips` directory contains the generated clips and their captions.
