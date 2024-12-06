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

Outputs are saved in `outputs/<query>` directory.

```
outputs/a cat playing piano
├── urls.csv
├── clips
│   ├── J---aiyznGQ
│   │   ├── 0001.json
│   │   ├── 0001.mp4
│   │   ├── 0002.json
│   │   └── 0002.mp4
│   ├── Yc-5P8-xLWU
│   │   ├── 0001.json
│   │   ├── 0001.mp4
│   │   ├── 0002.json
│   │   └── 0002.mp4
│   ├── _YSF5iHpGnU
│   │   ├── 0001.json
│   │   ├── 0001.mp4
│   │   ├── 0002.json
│   │   ├── 0002.mp4
│   │   ├── 0003.json
│   │   ├── 0003.mp4
│   │   ├── 0004.json
│   │   ├── 0004.mp4
│   │   ├── 0005.json
│   │   ├── 0005.mp4
│   │   ├── 0006.json
│   │   ├── 0006.mp4
│   │   ├── 0007.json
│   │   └── 0007.mp4
│   └── q-mDYH4lBhE
│       ├── 0001.json
│       ├── 0001.mp4
│       ├── 0002.json
│       ├── 0002.mp4
│       ├── 0003.json
│       ├── 0003.mp4
│       ├── 0004.json
│       └── 0004.mp4
└── videos
    ├── J---aiyznGQ.mp4
    ├── Yc-5P8-xLWU.mp4
    ├── _YSF5iHpGnU.mp4
    └── q-mDYH4lBhE.mp4
```

The `urls.csv` file contains the fetched urls of the videos.
The `videos` directory contains the downloaded original videos.
The `clips` directory contains the generated clips and their captions.
