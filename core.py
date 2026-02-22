"""
core.py
-------
Pure business logic for Shutdown Timer.
Handles OS-level shutdown commands — NO GUI / tkinter dependencies.
Every function returns a result that the GUI layer interprets.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from enum import Enum, auto


# ── Result types ─────────────────────────────────────────────────────────

class ShutdownResult(Enum):
    SUCCESS = auto()
    ALREADY_SCHEDULED = auto()
    NO_PENDING = auto()
    ERROR = auto()


@dataclass(frozen=True, slots=True)
class TimerResult:
    """Outcome of a set / cancel operation."""
    status: ShutdownResult
    code: int = 0
    message: str = ""


# ── Windows return codes ─────────────────────────────────────────────────

_RC_SUCCESS           = 0
_RC_ALREADY_SCHEDULED = 1190
_RC_NO_PENDING        = 1116


# ── Low-level helpers ────────────────────────────────────────────────────

def _run_shutdown_cmd(args: str) -> int:
    """Execute a shutdown command and return the process exit code (-1 on exception)."""
    try:
        proc = subprocess.run(
            f"shutdown {args}",
            shell=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return proc.returncode
    except Exception:
        return -1


def schedule_shutdown(seconds: int) -> TimerResult:
    """Schedule a system shutdown after *seconds* seconds."""
    if seconds < 0:
        return TimerResult(ShutdownResult.ERROR, -1, "เวลาต้องไม่ติดลบ")

    rc = _run_shutdown_cmd(f"-s -t {seconds}")

    if rc == _RC_SUCCESS:
        return TimerResult(ShutdownResult.SUCCESS, rc)
    if rc == _RC_ALREADY_SCHEDULED:
        return TimerResult(ShutdownResult.ALREADY_SCHEDULED, rc,
                           "มีการตั้งเวลาปิดเครื่องอยู่แล้ว")
    return TimerResult(ShutdownResult.ERROR, rc,
                       f"ไม่สามารถตั้งเวลาปิดเครื่องได้ (code: {rc})")


def cancel_shutdown() -> TimerResult:
    """Cancel a pending shutdown."""
    rc = _run_shutdown_cmd("-a")

    if rc == _RC_SUCCESS:
        return TimerResult(ShutdownResult.SUCCESS, rc, "ยกเลิกการปิดเครื่องเสร็จสิ้น")
    if rc == _RC_NO_PENDING:
        return TimerResult(ShutdownResult.NO_PENDING, rc,
                           "ไม่มีการตั้งเวลาปิดเครื่องอยู่ก่อนหน้า")
    return TimerResult(ShutdownResult.ERROR, rc,
                       f"เกิดข้อผิดพลาด (code: {rc})")


def force_reschedule(seconds: int) -> TimerResult:
    """Cancel any existing timer, then schedule a new one."""
    cancel_shutdown()
    return schedule_shutdown(seconds)


# ── Formatting helpers ───────────────────────────────────────────────────

def seconds_to_hms(total_seconds: int) -> tuple[int, int, int]:
    """Convert total seconds → (hours, minutes, seconds)."""
    h, remainder = divmod(max(0, total_seconds), 3600)
    m, s = divmod(remainder, 60)
    return h, m, s


def hms_to_seconds(hours: int = 0, minutes: int = 0, seconds: int = 0) -> int:
    """Convert hours/minutes/seconds → total seconds."""
    return hours * 3600 + minutes * 60 + seconds


def format_duration(total_seconds: int) -> str:
    """Return a human-readable Thai string like '1 ชม. 30 น.'."""
    h, m, s = seconds_to_hms(total_seconds)
    parts: list[str] = []
    if h > 0:
        parts.append(f"{h} ชม.")
    if m > 0:
        parts.append(f"{m} น.")
    if s > 0 and h == 0:
        parts.append(f"{s} วินาที")
    return " ".join(parts) if parts else "0 วินาที"
