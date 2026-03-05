"""
End-to-end workflow - V3 Full Pipeline + Zero Tolerance (Simplified)
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

MVP_ROOT = Path(__file__).resolve().parents[0]
if str(MVP_ROOT) not in sys.path:
    sys.path.insert(0, str(MVP_ROOT))

from pipeline.config import PROMPTS_DIR, RUNS_DIR
from pipeline.llm_client import LLMClient, LLMStage
from pipeline.llm.types import LLMBackend


# User requirement
REQUIREMENT = r"""已知椭圆 C: x²/a² + y²/b² = 1 (a > b > 0) 过点 M(2,3)，点 A 为其左顶点，且 AM 的斜率为 1/2。
1. 求 C 的方程；
2. 点 N 为椭圆上任意一点，求 △AMN 的面积的最大值。"""


# Layout contract v3
LAYOUT_CONTRACT_V3 = r"""# 3x3 Grid Layout (Math Problem Solving)

Layout: Left text, Right graphics

---

【排版铁律 - 版本 v3】

### 0. 题目常驻铁律

**绝对要求：**
- 题目文本必须在画面中始终常驻显示，不能被动画删除或覆盖
- 在 construct 开头立即渲染题目：`self.add(title_text)`
- 在后续所有动画中绝对不再修改或删除题目文本

### 1. 标题区（Title Zone）- 左上角 2x1

- 坐标：`x0: 0.05, y0: 0.15, x1: 0.66, y1: 0.48`
- 占用：宽度 66%，高度 33%
- 定位方法：使用 `.to_corner(UL)` 定位到左上角，然后微调
- **实现要求：**
  - 使用 `Text("题目文本")` 渲染完整题目
  - 在 construct 开头立即 `self.add(title_text)`
  - 在后续所有动画中绝对不再修改或删除题目文本
- 内容：标题文本、完整题目文本（常驻）和实时信息（如面积值等）
- 宽度限制：`max_width_ratio = 0.28`

### 2. 推导讲解区（Explanation Zone）- 左下角 2x2

- 坐标：`x0: 0.05, y0: 0.50, x1: 0.66, y1: 0.83`
- 占用：宽度 66%，高度 66%
- 定位方法：使用 `.to_edge(LEFT)` 靠左，垂直排列
- 排列：使用 `VGroup(...).arrange(DOWN, buff=...)`
- 宽度限制：`max_width_ratio = 0.60`
- **MathTex 中文禁令：** 绝对禁止在 MathTex 或 Tex 中写入任何中文字符
  - **会导致 LaTeX 编译崩溃**
  - 中文讲解使用 `Text("中文内容")`
  - 数学公式使用 `MathTex("S = \\frac{1}{2} b h")`
  - 如需混排，使用 VGroup([Text("中文"), MathTex("公式")]).arrange(RIGHT)`

### 3. 几何作图区（Graph Zone）- 右侧 1x3

- 坐标：`x0: 0.67, y0: 0.00, x1: 1.00, y1: 1.00`
- 占用：宽度 33%，高度 100%
- 定位方法：使用 `.to_edge(RIGHT)` 靠右对齐
- 坐标系要求：`Axes` 对象缩放并限制在右半边
- 动态更新：动点、动态线段必须使用 `always_redraw`

---

## 动态动画铁律

1. 必须且只能使用一个 `ValueTracker` 来控制角度 θ（初始值为 0）
2. 所有动态更新的元素（文本、点、线）都必须通过 `always_redraw` 绑定到这个 Tracker 上
3. 严禁写死静态坐标，所有坐标必须通过参数方程实时计算
4. 椭圆方程：x²/16 + y²/12 = 1
5. 参数方程：x = 4cosθ, y = 2√3 sinθ
6. 左顶点 A: (-4, 0)
7. 点 M: (2, 3)
8. 点 N: (4cosθ, 2√3 sinθ)
9. 三角形面积公式：S = 0.5 * |AM| * d(N, AM)
"""


# Fixer rules v3
FIXER_RULES_V3 = """Fixer Rules - Version 3

NEVER remove always_redraw, ValueTracker, or core animation logic.

You must:
1. Fix syntax errors
2. Fix logic errors
3. Keep ALL dynamic animation effects
4. Keep ValueTracker and always_redraw
5. Ensure theta_tracker.set_value(TAU) works

[LaTeX Compilation Error Fix]

If Error Log contains "LaTeX compilation error", it's because MathTex contains non-compilable characters (Chinese or unescaped words).

Your fix action MUST be:
- Replace offending MathTex with Text, OR
- Remove all Chinese characters and replace with pure English/numbers
- DO NOT try to fix LaTeX macros

Example fixes:
- Change MathTex(r"S = \\frac{1}{2} \\times base \\times height") to:
  Text("S = 1/2 x base x height") or MathTex(r"S = \\frac{1}{2} b h")
- Change MathTex(r"|AM| = 3\\sqrt{5}") to: Text("|AM| = 3*sqrt(5)")

Keep dynamic animation features intact!
"""


def build_client() -> LLMClient:
    """Build LLM client (Claude only)."""

    stage_map = {
        "codegen": LLMStage(
            name="codegen",
            backend=LLMBackend(name="anthropic", stage_config="codegen"),
            prompt_bundle="llm4_codegen",
        ),
        "fixer": LLMStage(
            name="fixer",
            backend=LLMBackend(name="anthropic", stage_config="fixer"),
            prompt_bundle="llm5_fixer",
        ),
    }
    return LLMClient(prompts_dir=PROMPTS_DIR, stage_map=stage_map)


def extract_code_from_response(response: str) -> str:
    """Extract Python code from response."""
    import re

    code_pattern = r'```python\s*([\s\S]*?)\s*```'
    match = re.search(code_pattern, response)
    if match:
        return match.group(1).strip()

    code_pattern = r'```\s*([\s\S]*?)\s*```'
    match = re.search(code_pattern, response)
    if match:
        return match.group(1).strip()

    return response.strip()


def run_render(py_file: Path, class_name: str, quality: str = "l", timeout: int = 900) -> tuple[bool, str, str]:
    """Execute manim render."""
    try:
        result = subprocess.run(
            ["manim", str(py_file), f"-q{quality}", "--format=mp4"],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(py_file.parent)
        )
        return (result.returncode == 0), result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Render timeout"
    except FileNotFoundError:
        return False, "", "manim command not found"


def main():
    print("=" * 70)
    print("End-to-End Video Generation - V3 (Full Pipeline + Zero Tolerance)")
    print("=" * 70)
    print()

    # Create run directory
    run_id = time.strftime("%Y%m%d_%H%M%S")
    run_dir = RUNS_DIR / f"e2e_v3_{run_id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"Run directory: {run_dir}")
    print()

    # Save requirements and layout contract
    (run_dir / "requirement.txt").write_text(REQUIREMENT, encoding="utf-8")
    (run_dir / "layout_contract_v3.md").write_text(LAYOUT_CONTRACT_V3, encoding="utf-8")

    # Use existing scene designs from previous successful run
    previous_designs_file = RUNS_DIR / "e2e_v3_20260305_102033" / "stage3_designs.json"
    if previous_designs_file.exists():
        print("Loading scene designs from previous run...")
        designs_data = json.loads(previous_designs_file.read_text(encoding="utf-8"))
        print(f"Loaded scene designs (Scene ID: {designs_data.get('scene_id', 'N/A')}, Class: {designs_data.get('class_name', 'N/A')})")
        print()
    else:
        print("ERROR: Previous scene designs file not found!")
        print("This script requires a previous V3 run with scene designs.")
        return 1

    # Build LLM client
    client = build_client()

    # ================================
    # Stage 4: CodeGen
    # ================================
    print("=" * 70)
    print("Stage 4/5: CodeGen (Claude Opus-4.6)")
    print("=" * 70)

    codegen_system = client.load_stage_system_prompt("codegen")

    # Inject v3 layout contract + ZERO TOLERANCE rule
    codegen_system = codegen_system + r"""

[Layout Contract v3]
""" + LAYOUT_CONTRACT_V3 + r"""

[Font Isolation Rule - NO Chinese in MathTex]

ABSOLUTELY FORBID using ANY Chinese characters in MathTex or Tex.

For Chinese display (e.g., "bottom", "height", "max area"), you MUST use native Text("your Chinese content") class.

If mixing formulas and Chinese text:
- Use VGroup with .arrange() to connect them, OR
- Use pure English letters in MathTex (e.g., use "S = \\frac{1}{2} b h" instead of "S = \\frac{1}{2} x base x height")

Examples:
- CORRECT: MathTex(r"S = \\frac{1}{2} b h") or Text("S = 1/2 x bottom x height")
- WRONG: MathTex(r"S = \\frac{1}{2} \\times base \\times height") (base/height undefined)
- WRONG: MathTex(r"\\text{bottom}") (Chinese causes LaTeX compilation failure)

【ZERO TOLERANCE RULE - HIGHEST PRIORITY】

WARNING: When generating explanation_zone code, you have ZERO TOLERANCE for missing or deleting ANY Chinese characters from on_screen_text!

- DO NOT delete or omit Chinese explanation text to "avoid LaTeX errors"
- on_screen_text contains BOTH Chinese logic words AND math formulas
- You MUST preserve ALL information from on_screen_text
- If you encounter mixed Chinese + formula (e.g., "S = 1/2 * 底 * 高"), you MUST handle it correctly:
  * Option 1: Decompose and use VGroup: VGroup(Text("S = 1/2 * ", font_size=24), Text("底", font_size=24), Text(" × ", font_size=24), Text("高", font_size=24)).arrange(RIGHT)
  * Option 2: Use MathTex for formula part + Text for explanation: VGroup(Text("根据面积公式：", font_size=24), MathTex("S = \\frac{1}{2}bh", font_size=24)).arrange(RIGHT)
- If you omit any Chinese text from original on_screen_text, generation WILL FAIL.

[Dynamic Animation Rules]
1. Use ONE ValueTracker for theta (start=0)
2. All dynamic elements use always_redraw
3. Ellipse: x²/16 + y²/12 = 1
4. Parametric: x = 4cosθ, y = 2√3 sinθ
5. Point A: (-4, 0), Point M: (2, 3), Point N: (4cosθ, 2√3 sinθ)
6. Triangle area: S = 0.5 * |AM| * d(N, AM)

[Title Zone Requirement]
Always display full original problem statement in title_zone.
"""

    codegen_user = """[User Requirement]
""" + REQUIREMENT + """

[Scene Design]
""" + json.dumps(designs_data, ensure_ascii=False, indent=2) + """

Generate complete Manim code following these requirements:
1. Inherit from Scene class
2. Use 3x3 grid layout strictly
3. Use ValueTracker to control point N motion
4. Display dynamic triangle area value
5. Point N moves along ellipse using always_redraw
6. theta_tracker animates from 0 to TAU (2π)
7. Output ONLY Python code, no explanation.
"""

    code, code_raw, code_chunks = client.generate_code(
        stage_key="codegen",
        system_prompt=codegen_system,
        user_prompt=codegen_user,
        max_continue_rounds=3
    )

    extracted_code = extract_code_from_response(code)

    (run_dir / "scene.py").write_text(extracted_code, encoding="utf-8")
    (run_dir / "stage4_code_raw.txt").write_text(code_raw, encoding="utf-8")
    for idx, chunk in enumerate(code_chunks, 1):
        (run_dir / f"stage4_code_continue_{idx}.txt").write_text(chunk, encoding="utf-8")

    print("Code generation complete")
    print(f"  - Code length: {len(extracted_code)} chars")
    print()

    # Progress report
    print("Progress Report:")
    print("  ✓ CodeGen: Claude Opus-4.6")
    print("  ✓ Using scene designs from previous V3 run")
    print()
    print("Ready for Stage 5: Fixer - Code rendering and fixing")
    print()

    # ================================
    # Stage 5: Fixer
    # ================================
    print("=" * 70)
    print("Stage 5/5: Fixer (Claude Opus-4.6)")
    print("=" * 70)

    fixer_system = client.load_stage_system_prompt("fixer")

    # Inject v3 fixer rules
    fixer_system = fixer_system + "\n\n" + FIXER_RULES_V3

    current_code = extracted_code
    py_file = run_dir / "scene.py"

    max_fix_rounds = 3
    fix_round = 0

    while fix_round <= max_fix_rounds:
        print(f"  Render attempt {fix_round + 1}/{max_fix_rounds + 1}...")

        py_file.write_text(current_code, encoding="utf-8")

        # Render with 900s timeout
        success, stdout, stderr = run_render(py_file, "MainScene", quality="l", timeout=900)

        (run_dir / f"render_stdout_{fix_round}.txt").write_text(stdout, encoding="utf-8")
        (run_dir / f"render_stderr_{fix_round}.txt").write_text(stderr, encoding="utf-8")

        if success:
            print()
            print("=" * 70)
            print("RENDER SUCCESSFUL!")
            print("=" * 70)
            print()

            media_dir = run_dir / "media" / "videos" / "scene" / "480p15"
            if media_dir.exists():
                mp4_files = list(media_dir.glob("*.mp4"))
                if mp4_files:
                    mp4_path = mp4_files[0]
                    print(f"Video file: {mp4_path}")
                    print()

                    final_mp4 = run_dir / "final.mp4"
                    shutil.copy2(mp4_path, final_mp4)
                    print(f"Copied to: {final_mp4}")
                    print()

                    try:
                        subprocess.run(["open", str(final_mp4)], check=False)
                        print("Video opened automatically")
                        print()
                    except:
                        pass

            print("=" * 70)
            print("END-TO-END WORKFLOW COMPLETE!")
            print("=" * 70)
            print()
            print("Summary:")
            print("  ✓ V3 Optimizations applied:")
            print("    - Zero tolerance rule enforced for Chinese text")
            print("    - VGroup + Text mixing for explanation zone")
            print("    - Timeout: 900s (15 minutes)")
            print("    - Fixer rule: Keep always_redraw/ValueTracker")
            print("    - LaTeX fix: No Chinese in MathTex")
            print()
            return 0
        else:
            print(f"  ✗ Render failed")
            if stderr:
                error_preview = stderr[-500:] if len(stderr) > 500 else stderr
                print(f"  Error preview: {error_preview}")
            print()

            if fix_round >= max_fix_rounds:
                print()
                print("=" * 70)
                print("RENDER FAILED: Max fix rounds reached")
                print("=" * 70)
                print()
                print("Final error log:")
                print(stderr)
                print()
                return 1

            print(f"  Sending fix request to Claude...")

            fixer_user = f"""[Target Class Name] MainScene

[Round {fix_round + 1} Error Log]
```
{stderr[-3000:] if len(stderr) > 3000 else stderr}
```

[Original Code]
```python
{current_code}
```

{FIXER_RULES_V3}

Fix the errors and output ONLY the complete fixed Python code, no explanation.
"""

            (run_dir / f"fixer_system_{fix_round}.txt").write_text(fixer_system, encoding="utf-8")

            fixed_code, fixed_raw, fixed_chunks = client.generate_code(
                stage_key="fixer",
                system_prompt=fixer_system,
                user_prompt=fixer_user,
                max_continue_rounds=3
            )

            current_code = extract_code_from_response(fixed_code)

            (run_dir / f"fix_raw_{fix_round}.txt").write_text(fixed_raw, encoding="utf-8")
            for idx, chunk in enumerate(fixed_chunks, 1):
                (run_dir / f"fix_continue_{fix_round}_{idx}.txt").write_text(chunk, encoding="utf-8")

            print(f"  ✓ Fix code received")
            print()

            fix_round += 1

    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nUser interrupted", file=sys.stderr)
        sys.exit(130)
