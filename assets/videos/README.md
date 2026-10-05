# Website video recommendations

Videos showing actual prediction and planning behavior would add the most value. Animated diagrams can complement these demonstrations by explaining the method.

## Recommended videos, in priority order

1. **Hierarchical planning rollout beneath the Summary.** Show an AntMaze episode alongside the coarse plan, intermediate subgoals, and executed actions. Highlight the active subgoal as the ant moves to make the hierarchy immediately understandable.

2. **Completed: execution comparisons in Planning performance.** Eight videos organized in the `fourroom/`, `ant/`, `pusht/`, and `cube/` subdirectories of [executions](executions/) appear beneath Fig. 4 under “Planning in action”: one row each for FourRoom, AntMaze, Push-T, and Cube, with two episodes per environment. Each video shows Start, LeWM, H-JEPA, and Goal. The episodes sit side by side on desktop and stack on mobile. Videos play muted and loop while visible, reset when they leave view, and restart when they return; reduced-motion preferences disable automatic playback. Playback controls remain available. Matched planning budgets should be verified against the experiment settings before claiming them in the website copy.

3. **Completed: animation in Hierarchical planning.** [Open the standalone preview](hierarchical-planning.html) through the local server. The SVG animation follows four steps: encode current state and goal → optimize the coarse plan → refine a subgoal → execute, observe, and replan. Refinement lasts six seconds and the other steps last four seconds; the combined refinement step highlights the subgoal before the fine rollout. Includes autoplay, a 18-second loop, play/pause, replay, step selection, and a timeline. Reduced-motion preferences start playback paused. Based on [the original TikZ](../fig_hierarchical_planning.tex). The animation replaces the static planning image in the Hierarchical planning section.

4. **Completed: abstraction video in Learning abstractions.** [selective_abstraction_lvl4.mp4](selective_abstraction_lvl4.mp4) shows ground-truth observations alongside labeled decoded representations at levels 1–4 for AntMaze and FourRoom. It is embedded in Fig. 2, centered beneath the depth probe plots, with muted autoplay, looping, and playback controls.

## Suggested starting point

Start with one compelling AntMaze rollout and the planning animation. Keep the static figures, use muted video with playback controls, and avoid adding motion everywhere.

## Training animation

[Hierarchical training](hierarchical-training-interleaved.html) appears in the Hierarchical predictive learning section, replacing the static image and the first animation. It follows the [training TikZ](../fig_hjepa_training_w1.tex) with two levels, stride 2, and state window 1. Five observations (o₀–o₄) alternate with four actions (a₀–a₃). Level 2 contains three states derived from times 0, 2, and 4, with two macro-actions aggregating action pairs (0, 1) and (2, 3).

Three stages cover encoding the trajectory (4 seconds), building the next level (4 seconds), and joint prediction/regularization with gradient flow (6 seconds). It includes the same playback, step-selection, timeline, and reduced-motion behavior as the planning animation.

Both embedded animations reset and pause when they leave the viewport, then restart from the beginning when they return. Reduced-motion preferences keep them paused until the viewer presses Play.
