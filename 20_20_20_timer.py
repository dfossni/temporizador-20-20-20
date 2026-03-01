import tkinter as tk
from tkinter import font as tkfont

# ── Constants ──────────────────────────────────────────────────────────────
WORK_SECONDS  = 20 * 60
BREAK_SECONDS = 20

# ── Palette: sólida, sin transparencia ─────────────────────────────────────
BG        = "#dfe8d0"   # verde sage claro — fondo ventana
CARD      = "#eaf0e0"   # superficie de tarjeta
BORDER    = "#7a9e5c"   # borde sage visible
ACCENT    = "#2d5a1b"   # sage oscuro — texto principal y arco
ACCENT2   = "#5c3a0a"   # marrón otoñal — descanso
TEXT_HI   = "#1a2e10"   # casi negro forestal
TEXT_LO   = "#3d5c28"   # sage oscuro legible
TRACK     = "#b8cea0"   # pista del arco

BTN_GREEN       = "#3a7020"
BTN_GREEN_HOV   = "#2a5518"
BTN_BROWN       = "#7a4a10"
BTN_BROWN_HOV   = "#5c3808"
BTN_DISABLED    = "#aaaaaa"
BTN_FG          = "#ffffff"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("20 · 20 · 20")
        self.resizable(False, False)
        self.configure(bg=BG)
        try:
            self.iconbitmap(self._find_icon())
        except Exception:
            pass

        self.state = "idle"
        self.remaining = WORK_SECONDS
        self.break_rem = BREAK_SECONDS

        self._build_ui()
        self._center(320, 440)
        self._tick()

    # ── UI ─────────────────────────────────────────────────────────────────
    def _build_ui(self):
        self.f_title  = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.f_sub    = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.f_time   = tkfont.Font(family="Segoe UI", size=48, weight="bold")
        self.f_btn    = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.f_emoji  = tkfont.Font(family="Segoe UI Emoji", size=26)

        # Tarjeta
        card = tk.Frame(self, bg=CARD, highlightthickness=2,
                        highlightbackground=BORDER)
        card.pack(padx=16, pady=16, fill="both", expand=True)

        tk.Label(card, text="E Y E   C A R E", bg=CARD,
                 fg=TEXT_LO, font=self.f_title).pack(pady=(22, 0))

        tk.Label(card, text="20 · 20 · 20", bg=CARD,
                 fg=ACCENT, font=tkfont.Font(family="Segoe UI", size=13, weight="bold")
                 ).pack(pady=(2, 0))

        # Arco + tiempo
        self.canvas = tk.Canvas(card, width=210, height=210,
                                bg=CARD, highlightthickness=0)
        self.canvas.pack(pady=(14, 6))
        self._draw_ring(1.0)

        # Estado
        self.lbl_status = tk.Label(card, text="Listo para empezar",
                                   bg=CARD, fg=TEXT_LO, font=self.f_sub,
                                   wraplength=260, justify="center")
        self.lbl_status.pack(pady=(2, 14))

        # Botones
        bf = tk.Frame(card, bg=CARD)
        bf.pack(pady=(0, 22))

        self.btn_start = tk.Button(
            bf, text="▶  Empezar", font=self.f_btn,
            bg=BTN_GREEN, fg=BTN_FG,
            activebackground=BTN_GREEN_HOV, activeforeground=BTN_FG,
            relief="flat", bd=0, padx=16, pady=8, cursor="hand2",
            command=self._on_start)
        self.btn_start.grid(row=0, column=0, padx=6)

        self.btn_stop = tk.Button(
            bf, text="■  Reiniciar", font=self.f_btn,
            bg=BTN_DISABLED, fg=BTN_FG,
            activebackground=BTN_BROWN_HOV, activeforeground=BTN_FG,
            relief="flat", bd=0, padx=16, pady=8, cursor="hand2",
            state="disabled", command=self._on_reset)
        self.btn_stop.grid(row=0, column=1, padx=6)

    # ── Arco ───────────────────────────────────────────────────────────────
    def _draw_ring(self, fraction, color=None):
        if color is None:
            color = ACCENT
        c = self.canvas
        c.delete("all")
        cx, cy, r = 105, 105, 78

        c.create_arc(cx-r, cy-r, cx+r, cy+r,
                     start=0, extent=359.9,
                     outline=TRACK, width=10, style="arc")
        if fraction > 0.001:
            c.create_arc(cx-r, cy-r, cx+r, cy+r,
                         start=90, extent=-(fraction * 360),
                         outline=color, width=10, style="arc")

        if self.state in ("idle", "running"):
            mins, secs = divmod(self.remaining, 60)
            txt = f"{mins:02d}:{secs:02d}"
        elif self.state in ("break_prompt", "breaking"):
            txt = f"00:{self.break_rem:02d}"
        else:
            txt = "✓"

        c.create_text(cx, cy, text=txt, fill=TEXT_HI,
                      font=self.f_time, anchor="center")

    # ── Estados ────────────────────────────────────────────────────────────
    def _on_start(self):
        if self.state != "idle":
            return
        self.state = "running"
        self.remaining = WORK_SECONDS
        self.btn_start.config(state="disabled", bg=BTN_DISABLED)
        self.btn_stop.config(state="normal", bg=BTN_BROWN)
        self.lbl_status.config(text="Mirando la pantalla…", fg=ACCENT)

    def _on_reset(self):
        self.state = "idle"
        self.remaining = WORK_SECONDS
        self.break_rem = BREAK_SECONDS
        self.btn_start.config(state="normal", bg=BTN_GREEN)
        self.btn_stop.config(state="disabled", bg=BTN_DISABLED)
        self.lbl_status.config(text="Listo para empezar", fg=TEXT_LO)
        self._draw_ring(1.0)

    def _on_accept_break(self):
        self.state = "breaking"
        self.break_rem = BREAK_SECONDS
        if hasattr(self, "_ov") and self._ov:
            self._ov.destroy()
            self._ov = None
        self.lbl_status.config(text="Mira un objeto a 6 m…", fg=ACCENT2)
        self.btn_stop.config(state="disabled", bg=BTN_DISABLED)

    def _on_done_ack(self):
        if hasattr(self, "_ov") and self._ov:
            self._ov.destroy()
            self._ov = None
        self._on_reset()

    # ── Tick ───────────────────────────────────────────────────────────────
    def _tick(self):
        if self.state == "running":
            if self.remaining > 0:
                self.remaining -= 1
            frac = self.remaining / WORK_SECONDS
            self._draw_ring(frac, ACCENT)
            if self.remaining == 0:
                self.state = "break_prompt"
                self._show_overlay(
                    icon="👁️",
                    title="¡Es hora de descansar!",
                    body="Aparta la vista y enfoca un objeto\na unos 6 metros de distancia.",
                    btn_text="Entendido — iniciar cuenta",
                    btn_bg=BTN_BROWN, btn_hov=BTN_BROWN_HOV,
                    cmd=self._on_accept_break,
                )

        elif self.state == "breaking":
            if self.break_rem > 0:
                self.break_rem -= 1
            frac = self.break_rem / BREAK_SECONDS
            self._draw_ring(frac, ACCENT2)
            if self.break_rem == 0:
                self.state = "done"
                self._draw_ring(0, ACCENT)
                self._show_overlay(
                    icon="🎉",
                    title="¡Excelente trabajo!",
                    body="Tus ojos descansaron correctamente.\n¡Vuelve cuando quieras!",
                    btn_text="Reiniciar temporizador",
                    btn_bg=BTN_GREEN, btn_hov=BTN_GREEN_HOV,
                    cmd=self._on_done_ack,
                )

        self.after(1000, self._tick)

    # ── Popup ──────────────────────────────────────────────────────────────
    def _show_overlay(self, icon, title, body, btn_text, btn_bg, btn_hov, cmd):
        ov = tk.Toplevel(self)
        ov.title("")
        ov.resizable(False, False)
        ov.configure(bg=BG)
        ov.attributes("-topmost", True)

        W, H = 340, 290
        sw, sh = ov.winfo_screenwidth(), ov.winfo_screenheight()
        ov.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")

        card = tk.Frame(ov, bg=CARD, highlightthickness=2,
                        highlightbackground=BORDER)
        card.pack(fill="both", expand=True, padx=8, pady=8)

        tk.Label(card, text=icon, bg=CARD,
                 font=self.f_emoji).pack(pady=(22, 4))

        tk.Label(card, text=title, bg=CARD, fg=TEXT_HI,
                 font=tkfont.Font(family="Segoe UI", size=13, weight="bold")
                 ).pack()

        tk.Label(card, text=body, bg=CARD, fg=TEXT_LO,
                 font=self.f_sub, justify="center", wraplength=280
                 ).pack(pady=(8, 18))

        tk.Button(card, text=btn_text, font=self.f_btn,
                  bg=btn_bg, fg=BTN_FG,
                  activebackground=btn_hov, activeforeground=BTN_FG,
                  relief="flat", bd=0, padx=18, pady=8,
                  cursor="hand2", command=cmd
                  ).pack(pady=(0, 20))

        self._ov = ov

    # ── Centro ─────────────────────────────────────────────────────────────

    def _find_icon(self):
        import os, sys
        base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, "icono.ico")

    def _center(self, w, h):
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")


if __name__ == "__main__":
    App().mainloop()
