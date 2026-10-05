# Website video recommendations

Videos showing actual prediction and planning behavior would add the most value. Animated diagrams can complement these demonstrations by explaining the method.

## Recommended videos, in priority order

1. **Hierarchical planning rollout beneath the Summary.** Show an AntMaze episode alongside the coarse plan, intermediate subgoals, and executed actions. Highlight the active subgoal as the ant moves to make the hierarchy immediately understandable.

2. **Synchronized comparison in Planning performance.** Show flat JEPA and H-JEPA attempting the same task from the same initial state under a matched planning budget. Label the methods and outcomes, and include several representative tasks to give the comparison context.

3. **Completed: animated Fig. 3 in Hierarchical planning.** [Open the standalone preview](hierarchical-planning.html) through the local server. The SVG animation follows four steps: encode current state and goal → optimize the coarse plan → refine a subgoal → execute, observe, and replan. Refinement lasts six seconds and the other steps last four seconds; the combined refinement step highlights the subgoal before the fine rollout. Includes autoplay, a 18-second loop, play/pause, replay, step selection, and a timeline. Reduced-motion preferences start playback paused. Based on [the original TikZ](../fig_hierarchical_planning.tex). The animation replaces the static planning image as Fig. 3 on the website.

4. **Completed: abstraction video in Learning abstractions.** [selective_abstraction_lvl4.mp4](selective_abstraction_lvl4.mp4) shows ground-truth observations alongside labeled decoded representations at levels 1–4 for AntMaze and FourRoom. It is embedded in Fig. 4, centered beneath the depth probe plots, with muted autoplay, looping, and playback controls.

## Suggested starting point

Start with one compelling AntMaze rollout and the Fig. 3 animation. Keep the static figures, use muted video with playback controls, and avoid adding motion everywhere.
