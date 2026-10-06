# H-JEPA promotional video

This folder reproduces the approved **88-second, 1920 × 1080, 30 fps** cut
(approved opening with L1 ← L2 ← L3 above the maze). It contains the renderer, additional source clips,
and optional subtitles. Other footage and plots are reused from the repository's
`assets/` directory. The instrumental soundtrack is synthesized by the renderer.

The website does not load or execute anything in this folder. No website build
or publishing configuration is required. Rendered files and the local Python
environment are gitignored; the final MP4 is generated locally.

## Setup and render

Use Python 3.9–3.12. The pinned dependencies were validated with Python 3.9 on
macOS. From the repository root:

```sh
python3 -m venv video-production/.venv
video-production/.venv/bin/python -m pip install -r video-production/requirements.txt
video-production/.venv/bin/python video-production/render.py
```

The main output is `video-production/output/hjepa_demo.mp4`, with H.264 video
and AAC stereo audio. `hjepa_demo.srt` is copied into the output directory.
The renderer also writes individual scene MP4s, logs, an intermediate WAV,
and a concatenation list there. It regenerates every scene on each render,
so edits take effect without deleting old output manually.

For a quick storyboard without encoding the full movie:

```sh
video-production/.venv/bin/python video-production/render.py --preview
```

This writes `storyboard.jpg` and one preview image per scene. Defaults resolve
relative to the script's repository, so commands also work from another working
directory when the interpreter and script are addressed by absolute path.
Use `--out /path/to/output` for a different render destination. Only the default
output directory is covered by the repository's ignore rule.

To preview just the current opening, including decoded subgoals and the
AntMaze Pareto plot:

```sh
video-production/.venv/bin/python video-production/render.py --preview-opening-decoding
```

This writes `opening-pareto-decoding-preview.png` using the same composition
as the full movie. `--preview-opening-pareto` keeps the earlier maze-only
alternative available as a static preview.

The opening title is “H-JEPA: Hierarchical World Models for Visual Planning”,
with no subtitle. Three 224-pixel decoded views appear in a row ordered L1,
L2, L3; arrows point leftward from L3 to L2 to L1. A 560 × 400 overhead maze
is centered beneath them. The AntMaze success–compute plot appears on the
right under “Higher success with less compute”. The illustrative-footage
disclosure and 2.5× playback label remain at the bottom.

### Fonts and FFmpeg

The approved typography uses **Avenir Next**, supplied by macOS. The renderer
uses its Regular and Demi Bold faces. The system font is not redistributed.
On another system, supply locally installed regular and semibold TTF/OTF files:

```sh
python3 video-production/render.py \
  --font-regular /path/to/Regular.ttf \
  --font-semibold /path/to/Semibold.ttf
```

Alternate fonts change the appearance. The renderer checks that headline text
fits, but inspect `--preview` for other labels and captions before rendering.
`imageio-ffmpeg` provides FFmpeg on supported platforms; an existing executable
can be selected with `IMAGEIO_FFMPEG_EXE=/path/to/ffmpeg`.

## Timeline and editing

| Time | Duration | Scene |
| --- | ---: | --- |
| 0:00–0:10 | 10 s | Compact planning teaser, decoded subgoals, and AntMaze Pareto plot |
| 0:10–0:22 | 12 s | Learning predictive hierarchies |
| 0:22–0:30 | 8 s | Selective abstraction |
| 0:30–0:46 | 16 s | Hierarchical planning |
| 0:46–0:53 | 7 s | Four-environment execution grid |
| 0:53–1:01 | 8 s | Simulation Pareto results |
| 1:01–1:13 | 12 s | Inverse dynamics at each level (DROID method) |
| 1:13–1:21 | 8 s | DROID videos and results |
| 1:21–1:28 | 7 s | Project link and credits |

In `render.py`, `TITLES` controls the eight headings, `SPECS` controls scene
durations, `clips()` specifies crops and playback rates, and `compose()` lays
out each slide; `compose_opening()` arranges the synchronized maze and decoded
views from one source frame. Clip crops use `(width, height, x, y)` in source pixels.
Clip durations and `SPECS` should agree. Total duration, the progress bar,
and soundtrack length are calculated from `SPECS`.

`captions.srt` is the optional text track. The main visual captions are already
burned into the video. Update subtitle timestamps when changing scene lengths;
subtitle timing is not automatically inferred from `SPECS`.

## Source material

| Source | Use |
| --- | --- |
| `sources/hierarchical_planning_sliding_new.mp4` | Opening: source seconds 2–27 at 2.5×, decoded at 1606 × 1080. Maze crop `(1222, 872, 32, 84)`; each decoded panel is 296 × 296 at x=1282 and y=740/412/84 for L1/L2/L3. The source heading is omitted. |
| `sources/hjepa-training.mp4` | Training illustration: 14 seconds shown in 12 seconds. |
| `sources/hjepa-planning.mp4` | Planning illustration: 18 seconds shown in 16 seconds. |
| `sources/idm-schema.mp4` | Inverse-dynamics illustration (`../assets/videos/idm-schema.html`, diagram only, recorded frame-exact at 2×): 17 seconds shown in 12 seconds, crop `(2340, 1116, 0, 100)` drops the top caption line. |
| `../assets/videos/selective_abstraction_lvl4.mp4` | First eight seconds at normal playback speed. |
| `../assets/videos/executions/fourroom/fourroom_ep28.mp4` | FourRoom execution comparison, about 1.2× playback. |
| `../assets/videos/executions/ant/ant_ep35.mp4` | AntMaze execution comparison, about 1.9× playback. |
| `../assets/videos/executions/pusht/pusht_ep7.mp4` | Push-T execution comparison, about 1.1× playback. |
| `../assets/videos/executions/cube/cube_30_ep2.mp4` | Cube execution comparison at original playback speed. |
| `../assets/videos/scene-diversity.mp4` | First eight seconds at normal speed; `(784, 230, 40, 318)` selects only the three DROID videos. |
| `../assets/figures/overview.png` | Opening AntMaze Pareto plot, cropped to `(left=1450, top=60, right=2375, bottom=1010)` with its axes, legend, and error bars preserved. |
| `../assets/figures/planning-results-pareto.png` | All four simulation success-versus-compute plots, including axes, legend, and error bars. |
| `../assets/figures/droid-ablation.png` | DROID inverse-dynamics/hierarchy bar chart. |
| `../assets/figures/droid-compute.png` | DROID fidelity-versus-compute plot. |

The two method illustration MP4s are archived copies of the original local
training/planning exports. Their editable diagrams remain in
[`hierarchical-training-interleaved.html`](../assets/videos/hierarchical-training-interleaved.html)
and [`hierarchical-planning.html`](../assets/videos/hierarchical-planning.html).
The separate `assets/videos/hierarchical_planning/` experiment is not used.
The older `sources/hierarchical_planning_sliding.mp4` is retained for previous
cuts; the current opening uses the compact `_new` clip.

The opening teaser was supplied separately and shows **illustrative planning
using recorded observations and decoded states**, played at 2.5×. Use `--teaser PATH`
to select another compatible source. No model inference is run during rendering.

Project claims and evaluation context follow `../index.html`. Execution clips
are examples, separate from aggregate results; each LeWM/H-JEPA pair uses the
same playback transformation. They are not labeled as matched-compute trials.
Three levels perform best on navigation and Cube, while two work best on Push-T.
DROID reports offline end-effector path fidelity, not closed-loop task success,
and uses inverse-dynamics supervision. Its compute chart includes frozen-encoder
references at their native 1 fps; the H-JEPA models use 5 fps.
