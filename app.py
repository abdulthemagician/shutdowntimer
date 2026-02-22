"""
app.py
------
Modern GUI for Shutdown Timer.
Features:
  • Live countdown display (HH : MM : SS)
  • Quick-preset buttons (30 min, 1 hr, 2 hr, 4 hr)
  • Custom time input (hours / minutes / seconds spinboxes)
  • Active / Inactive status badge
  • Catppuccin Mocha dark theme
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

from core import (
    ShutdownResult,
    cancel_shutdown,
    force_reschedule,
    format_duration,
    hms_to_seconds,
    schedule_shutdown,
    seconds_to_hms,
)
from theme import COLORS, FONT_COUNTDOWN, FONT_EMOJI, FONT_INPUT, FONT_LABEL, apply_theme

# ── Preset durations (label, seconds) ───────────────────────────────────
PRESETS: list[tuple[str, int]] = [
    ("15 น.",  15 * 60),
    ("30 น.",  30 * 60),
    ("1 ชม.",  60 * 60),
    ("2 ชม.",  2 * 60 * 60),
    ("4 ชม.",  4 * 60 * 60),
]

_TICK_INTERVAL_MS = 500  # countdown refresh rate


# ═════════════════════════════════════════════════════════════════════════
# Application
# ═════════════════════════════════════════════════════════════════════════

class ShutdownTimerApp:
    """Main application window."""

    WIN_W = 420
    WIN_H = 480

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Shutdown Timer")
        self.root.resizable(False, False)

        # State
        self._remaining: int = 0        # seconds left (local tracker)
        self._timer_active: bool = False
        self._tick_id: str | None = None

        # Input variables
        self._hour_var = tk.StringVar(value="0")
        self._min_var  = tk.StringVar(value="0")
        self._sec_var  = tk.StringVar(value="0")

        apply_theme(self.root)
        self._center_window()
        self._build_ui()

    # ── Window position ──────────────────────────────────────────────

    def _center_window(self) -> None:
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - self.WIN_W) // 2
        y = (sh - self.WIN_H) // 2
        self.root.geometry(f"{self.WIN_W}x{self.WIN_H}+{x}+{y}")

    # ── UI construction ──────────────────────────────────────────────

    def _build_ui(self) -> None:
        root = self.root

        outer = tk.Frame(root, bg=COLORS["base"])
        outer.pack(fill="both", expand=True, padx=16, pady=16)

        card = ttk.Frame(outer, style="Card.TFrame", padding=(24, 18, 24, 22))
        card.pack(fill="both", expand=True)
        card.columnconfigure(0, weight=1)

        row = 0

        # ── Title row ────────────────────────────────────────────────
        title_frame = ttk.Frame(card, style="Card.TFrame")
        title_frame.grid(row=row, column=0, sticky="ew", pady=(0, 4))
        ttk.Label(title_frame, text="⏰", style="Title.TLabel",
                  font=FONT_EMOJI).pack(side="left", padx=(0, 8))
        ttk.Label(title_frame, text="Shutdown Timer",
                  style="Title.TLabel").pack(side="left")
        row += 1

        # ── Status badge ─────────────────────────────────────────────
        self._status_label = ttk.Label(card, text="● ไม่มีตัวจับเวลา",
                                       style="StatusInactive.TLabel")
        self._status_label.grid(row=row, column=0, sticky="w", pady=(0, 12))
        row += 1

        # ── Countdown display ────────────────────────────────────────
        cd_frame = ttk.Frame(card, style="Card.TFrame")
        cd_frame.grid(row=row, column=0, sticky="ew", pady=(0, 6))
        cd_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        self._lbl_h = ttk.Label(cd_frame, text="00", style="Countdown.TLabel",
                                anchor="center")
        self._lbl_sep1 = ttk.Label(cd_frame, text=":", style="Countdown.TLabel",
                                   anchor="center")
        self._lbl_m = ttk.Label(cd_frame, text="00", style="Countdown.TLabel",
                                anchor="center")
        self._lbl_sep2 = ttk.Label(cd_frame, text=":", style="Countdown.TLabel",
                                   anchor="center")
        self._lbl_s = ttk.Label(cd_frame, text="00", style="Countdown.TLabel",
                                anchor="center")

        self._lbl_h.grid(row=0, column=0, sticky="ew")
        self._lbl_sep1.grid(row=0, column=1)
        self._lbl_m.grid(row=0, column=2, sticky="ew")
        self._lbl_sep2.grid(row=0, column=3)
        self._lbl_s.grid(row=0, column=4, sticky="ew")

        # Unit labels under countdown
        unit_frame = ttk.Frame(card, style="Card.TFrame")
        unit_frame.grid(row=row + 1, column=0, sticky="ew", pady=(0, 14))
        unit_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        for col, txt in [(0, "ชั่วโมง"), (2, "นาที"), (4, "วินาที")]:
            ttk.Label(unit_frame, text=txt, style="CountdownUnit.TLabel",
                      anchor="center").grid(row=0, column=col, sticky="ew")
        row += 2

        # ── Divider ──────────────────────────────────────────────────
        self._make_divider(card, row); row += 1

        # ── Quick presets ────────────────────────────────────────────
        ttk.Label(card, text="ตั้งเวลาด่วน", style="Card.TLabel").grid(
            row=row, column=0, sticky="w", pady=(0, 6))
        row += 1

        preset_frame = ttk.Frame(card, style="Card.TFrame")
        preset_frame.grid(row=row, column=0, sticky="ew", pady=(0, 14))
        for i, (label, secs) in enumerate(PRESETS):
            btn = ttk.Button(preset_frame, text=label, style="Preset.TButton",
                             command=lambda s=secs: self._on_preset(s))
            btn.pack(side="left", expand=True, fill="x",
                     padx=(0 if i == 0 else 3, 0))
        row += 1

        # ── Divider ──────────────────────────────────────────────────
        self._make_divider(card, row); row += 1

        # ── Custom time input ────────────────────────────────────────
        ttk.Label(card, text="กำหนดเวลาเอง", style="Card.TLabel").grid(
            row=row, column=0, sticky="w", pady=(0, 6))
        row += 1

        input_frame = ttk.Frame(card, style="Card.TFrame")
        input_frame.grid(row=row, column=0, sticky="ew", pady=(0, 16))
        input_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        vcmd_h = (root.register(lambda v: self._validate_int(v, 0, 999)), "%P")
        vcmd_m = (root.register(lambda v: self._validate_int(v, 0, 59)),  "%P")
        vcmd_s = (root.register(lambda v: self._validate_int(v, 0, 59)),  "%P")

        self._spin_h = ttk.Spinbox(input_frame, from_=0, to=999, width=5,
                                   textvariable=self._hour_var, font=FONT_INPUT,
                                   validate="key", validatecommand=vcmd_h,
                                   justify="center")
        self._spin_h.grid(row=0, column=0, sticky="ew", padx=(0, 2))
        ttk.Label(input_frame, text="ชม.", style="InputLabel.TLabel").grid(
            row=0, column=1, sticky="w", padx=(0, 8))

        self._spin_m = ttk.Spinbox(input_frame, from_=0, to=59, width=5,
                                   textvariable=self._min_var, font=FONT_INPUT,
                                   validate="key", validatecommand=vcmd_m,
                                   justify="center", wrap=True)
        self._spin_m.grid(row=0, column=2, sticky="ew", padx=(0, 2))
        ttk.Label(input_frame, text="น.", style="InputLabel.TLabel").grid(
            row=0, column=3, sticky="w", padx=(0, 8))

        self._spin_s = ttk.Spinbox(input_frame, from_=0, to=59, width=5,
                                   textvariable=self._sec_var, font=FONT_INPUT,
                                   validate="key", validatecommand=vcmd_s,
                                   justify="center", wrap=True)
        self._spin_s.grid(row=0, column=4, sticky="ew", padx=(0, 2))
        ttk.Label(input_frame, text="วิ.", style="InputLabel.TLabel").grid(
            row=0, column=5, sticky="w")
        row += 1

        # ── Action buttons ───────────────────────────────────────────
        self._btn_set = ttk.Button(card, text="✅  ตั้งเวลาปิดเครื่อง",
                                   style="Green.TButton", command=self._on_set)
        self._btn_set.grid(row=row, column=0, sticky="ew", pady=(0, 8))
        row += 1

        self._btn_cancel = ttk.Button(card, text="❌  ยกเลิกการปิดเครื่อง",
                                      style="Red.TButton", command=self._on_cancel)
        self._btn_cancel.grid(row=row, column=0, sticky="ew")

        # ── Keyboard shortcuts ───────────────────────────────────────
        root.bind("<Return>", lambda _: self._on_set())
        root.bind("<Escape>", lambda _: self._on_cancel())

    # ── Helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _make_divider(parent: ttk.Frame, row: int) -> None:
        sep = tk.Frame(parent, bg=COLORS["surface1"], height=1)
        sep.grid(row=row, column=0, sticky="ew", pady=6)

    @staticmethod
    def _validate_int(value: str, min_v: int, max_v: int) -> bool:
        if value == "":
            return True
        if value.lstrip("0") == "":
            return True
        if not value.isdigit():
            return False
        return min_v <= int(value) <= max_v

    # ── Countdown logic ──────────────────────────────────────────────

    def _start_countdown(self, total_seconds: int) -> None:
        self._remaining = total_seconds
        self._timer_active = True
        self._update_countdown_display()
        self._update_status()
        self._tick()

    def _stop_countdown(self) -> None:
        self._timer_active = False
        self._remaining = 0
        if self._tick_id is not None:
            self.root.after_cancel(self._tick_id)
            self._tick_id = None
        self._update_countdown_display()
        self._update_status()

    def _tick(self) -> None:
        if not self._timer_active:
            return
        if self._remaining > 0:
            self._remaining -= 1
            self._update_countdown_display()
            self._tick_id = self.root.after(_TICK_INTERVAL_MS * 2, self._tick)
        else:
            self._timer_active = False
            self._update_status()

    def _update_countdown_display(self) -> None:
        h, m, s = seconds_to_hms(self._remaining)
        self._lbl_h.configure(text=f"{h:02d}")
        self._lbl_m.configure(text=f"{m:02d}")
        self._lbl_s.configure(text=f"{s:02d}")

        color = COLORS["blue"] if self._timer_active else COLORS["overlay0"]
        for lbl in (self._lbl_h, self._lbl_sep1, self._lbl_m,
                    self._lbl_sep2, self._lbl_s):
            lbl.configure(foreground=color)

    def _update_status(self) -> None:
        if self._timer_active:
            dur = format_duration(self._remaining)
            self._status_label.configure(
                text=f"● กำลังนับถอยหลัง — {dur}",
                style="StatusActive.TLabel",
            )
        else:
            self._status_label.configure(
                text="● ไม่มีตัวจับเวลา",
                style="StatusInactive.TLabel",
            )

    # ── Event handlers ───────────────────────────────────────────────

    def _on_preset(self, seconds: int) -> None:
        self._schedule_and_display(seconds)

    def _on_set(self) -> None:
        try:
            h = int(self._hour_var.get() or 0)
            m = int(self._min_var.get() or 0)
            s = int(self._sec_var.get() or 0)
        except ValueError:
            messagebox.showerror("ค่าไม่ถูกต้อง",
                                 "กรุณากรอกตัวเลขให้ถูกต้อง")
            return

        total = hms_to_seconds(h, m, s)

        if total <= 0:
            ok = messagebox.askyesno(
                "ปิดเครื่องทันที?",
                "คุณต้องการปิดเครื่องทันทีหรือไม่?\n"
                "ระบบจะนับถอยหลัง 10 วินาทีก่อนปิดเครื่อง",
            )
            if not ok:
                return
            total = 10

        self._schedule_and_display(total)

    def _on_cancel(self) -> None:
        result = cancel_shutdown()

        if result.status == ShutdownResult.SUCCESS:
            self._stop_countdown()
            messagebox.showinfo("ยกเลิก", result.message)
        elif result.status == ShutdownResult.NO_PENDING:
            self._stop_countdown()
            messagebox.showwarning("ไม่มีตัวจับเวลา", result.message)
        else:
            messagebox.showerror("ข้อผิดพลาด", result.message)

    def _schedule_and_display(self, seconds: int) -> None:
        """Central scheduling logic with override handling."""
        result = schedule_shutdown(seconds)

        if result.status == ShutdownResult.SUCCESS:
            self._start_countdown(seconds)
            dur = format_duration(seconds)
            messagebox.showinfo("ตั้งเวลาปิดเครื่อง",
                                f"ตั้งเวลาปิดเครื่องใน {dur} แล้ว")
            return

        if result.status == ShutdownResult.ALREADY_SCHEDULED:
            override = messagebox.askyesno(
                "ตั้งเวลาทับซ้อน",
                "มีการตั้งเวลาปิดเครื่องอยู่แล้ว\n"
                "ต้องการยกเลิกของเก่าและตั้งค่าใหม่หรือไม่?",
            )
            if not override:
                return
            result = force_reschedule(seconds)
            if result.status == ShutdownResult.SUCCESS:
                self._start_countdown(seconds)
                dur = format_duration(seconds)
                messagebox.showinfo("ตั้งเวลาปิดเครื่อง",
                                    f"ตั้งเวลาปิดเครื่องใน {dur} แล้ว")
            else:
                messagebox.showerror("ข้อผิดพลาด", result.message)
            return

        messagebox.showerror("ข้อผิดพลาด", result.message)

    # ── Public ───────────────────────────────────────────────────────

    def run(self) -> None:
        """Start the tkinter event loop."""
        self.root.mainloop()
