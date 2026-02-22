"""
theme.py
--------
Centralized theme configuration for Shutdown Timer.
Catppuccin Mocha-inspired dark palette with all style definitions.
"""

from __future__ import annotations

from tkinter import ttk
import tkinter as tk

# ── Color Palette (Catppuccin Mocha) ─────────────────────────────────────
COLORS = {
    "crust":    "#11111b",
    "base":     "#1e1e2e",
    "mantle":   "#181825",
    "surface0": "#313244",
    "surface1": "#45475a",
    "surface2": "#585b70",
    "overlay0": "#6c7086",
    "overlay1": "#7f849c",
    "text":     "#cdd6f4",
    "subtext0": "#a6adc8",
    "subtext1": "#bac2de",
    "blue":     "#89b4fa",
    "sapphire": "#74c7ec",
    "green":    "#a6e3a1",
    "red":      "#f38ba8",
    "peach":    "#fab387",
    "yellow":   "#f9e2af",
    "mauve":    "#cba6f7",
    "lavender": "#b4befe",
}

# ── Fonts ────────────────────────────────────────────────────────────────
FONT_TITLE    = ("Segoe UI", 16, "bold")
FONT_SUBTITLE = ("Segoe UI", 10)
FONT_LABEL    = ("Segoe UI", 10)
FONT_INPUT    = ("Segoe UI", 13)
FONT_BUTTON   = ("Segoe UI", 10, "bold")
FONT_COUNTDOWN = ("Consolas", 36, "bold")
FONT_COUNTDOWN_LABEL = ("Segoe UI", 9)
FONT_PRESET   = ("Segoe UI", 9, "bold")
FONT_STATUS   = ("Segoe UI", 9, "bold")
FONT_EMOJI    = ("Segoe UI Emoji", 18)


def apply_theme(root: tk.Tk) -> None:
    """Apply the dark theme to the root window and all ttk styles."""
    root.configure(bg=COLORS["base"])

    style = ttk.Style(root)
    style.theme_use("clam")

    # ── Base ─────────────────────────────────────────────────────────
    style.configure(
        ".",
        background=COLORS["base"],
        foreground=COLORS["text"],
        font=FONT_LABEL,
    )

    # ── Frames ───────────────────────────────────────────────────────
    style.configure("Card.TFrame", background=COLORS["surface0"], relief="flat")
    style.configure("Base.TFrame", background=COLORS["base"])
    style.configure("Surface.TFrame", background=COLORS["surface0"])

    # ── Labels ───────────────────────────────────────────────────────
    style.configure("Card.TLabel", background=COLORS["surface0"],
                    foreground=COLORS["subtext0"], font=FONT_LABEL)
    style.configure("Title.TLabel", background=COLORS["surface0"],
                    foreground=COLORS["text"], font=FONT_TITLE)
    style.configure("Subtitle.TLabel", background=COLORS["surface0"],
                    foreground=COLORS["subtext0"], font=FONT_SUBTITLE)
    style.configure("Countdown.TLabel", background=COLORS["surface0"],
                    foreground=COLORS["blue"], font=FONT_COUNTDOWN)
    style.configure("CountdownUnit.TLabel", background=COLORS["surface0"],
                    foreground=COLORS["overlay1"], font=FONT_COUNTDOWN_LABEL)
    style.configure("StatusActive.TLabel", background=COLORS["surface0"],
                    foreground=COLORS["green"], font=FONT_STATUS)
    style.configure("StatusInactive.TLabel", background=COLORS["surface0"],
                    foreground=COLORS["overlay0"], font=FONT_STATUS)
    style.configure("InputLabel.TLabel", background=COLORS["surface0"],
                    foreground=COLORS["subtext1"], font=FONT_LABEL)

    # ── Separator ────────────────────────────────────────────────────
    style.configure("Card.TSeparator", background=COLORS["surface1"])

    # ── Spinbox ──────────────────────────────────────────────────────
    style.configure(
        "TSpinbox",
        fieldbackground=COLORS["surface1"],
        background=COLORS["surface1"],
        foreground=COLORS["text"],
        arrowcolor=COLORS["text"],
        bordercolor=COLORS["surface1"],
        lightcolor=COLORS["surface1"],
        darkcolor=COLORS["surface1"],
        insertcolor=COLORS["text"],
        font=FONT_INPUT,
    )
    style.map(
        "TSpinbox",
        fieldbackground=[("focus", COLORS["surface2"])],
        bordercolor=[("focus", COLORS["blue"])],
    )

    # ── Buttons ──────────────────────────────────────────────────────
    _button_styles = [
        ("Green.TButton",  COLORS["green"],    COLORS["crust"]),
        ("Red.TButton",    COLORS["red"],      COLORS["crust"]),
        ("Preset.TButton", COLORS["surface1"], COLORS["text"]),
    ]
    for name, bg, fg in _button_styles:
        font = FONT_PRESET if "Preset" in name else FONT_BUTTON
        style.configure(
            name,
            background=bg,
            foreground=fg,
            font=font,
            borderwidth=0,
            focusthickness=0,
            padding=(10, 7),
            relief="flat",
        )
        hover_bg = COLORS["blue"] if "Preset" not in name else COLORS["surface2"]
        style.map(
            name,
            background=[("active", hover_bg), ("pressed", COLORS["surface1"])],
            foreground=[("active", COLORS["crust"] if "Preset" not in name else COLORS["text"]),
                        ("pressed", COLORS["text"])],
        )
