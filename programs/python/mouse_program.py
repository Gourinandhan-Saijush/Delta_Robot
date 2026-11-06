import argparse
import math
import queue
import threading
import tkinter as tk
from tkinter import messagebox

from cri_lib import CRIController

ROBOT_IP = "192.168.3.11"
CRI_PORT = 3920
FRAME = "#base"

X_MIN, X_MAX = -100.0, 100.0
Y_MIN, Y_MAX = -100.0, 100.0

DEFAULT_Z = 0.0

VELOCITY = 100.0
ACCELERATION = 50.0
COMMAND_TIMEOUT = 3.0

PHYSICAL_MOTION_ENABLED = True


class MouseRobot:
    def __init__(self, root):
        self.root = root
        self.robot = None
        self.connected = False
        self.held = False
        self.z = DEFAULT_Z
        self.targets = queue.Queue(maxsize=1)
        self.worker = None
        self.last_error = None

        root.title("igus Delta — Mouse XY Control")
        root.geometry("760x650")

        self.canvas = tk.Canvas(
            root, width=600, height=500,
            bg="white", highlightthickness=1
        )
        self.canvas.pack(pady=10)

        self.canvas.create_rectangle(
            50, 50, 550, 450, outline="black"
        )
        self.canvas.create_text(
            300, 25,
            text="Hold left mouse button inside workspace to jog"
        )

        self.dot = self.canvas.create_oval(
            295, 245, 305, 255, fill="red"
        )

        controls = tk.Frame(root)
        controls.pack()

        tk.Label(controls, text="Z height (mm):").grid(row=0, column=0)
        self.z_entry = tk.Entry(controls, width=10)
        self.z_entry.insert(0, str(DEFAULT_Z))
        self.z_entry.grid(row=0, column=1)

        tk.Button(
            controls, text="Set Z", command=self.set_z
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            controls, text="Connect CRI", command=self.connect
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            controls, text="STOP", command=self.stop
        ).grid(row=0, column=4, padx=5)

        self.status = tk.Label(
            root, text="PREVIEW ONLY — physical motion disabled"
        )
        self.status.pack(pady=10)

        self.canvas.bind("<ButtonPress-1>", self.press)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.canvas.bind("<Motion>", self.move_mouse)
        root.bind("<Escape>", lambda event: self.stop())
        root.protocol("WM_DELETE_WINDOW", self.close)

    def set_z(self):
        try:
            value = float(self.z_entry.get())
            if not math.isfinite(value):
                raise ValueError
            self.z = value
            self.status.config(text=f"Z set to {self.z:.1f} mm")
        except ValueError:
            messagebox.showerror(
                "Invalid Z", "Enter a valid finite number."
            )

    def connect(self):
        if not PHYSICAL_MOTION_ENABLED:
            messagebox.showinfo(
                "Preview mode",
                "Physical motion is disabled in this script."
            )
            return

        if self.connected:
            return

        try:
            self.robot = CRIController()

            if not self.robot.connect(ROBOT_IP, CRI_PORT):
                self.robot.close()
                self.robot = None
                raise RuntimeError("CRI connection failed")

            self.connected = True
            self.status.config(
                text="CRI connected; waiting for mouse jog"
            )

            self.worker = threading.Thread(
                target=self.motion_worker, daemon=True
            )
            self.worker.start()

        except Exception as exc:
            self.status.config(text=f"Connection error: {exc}")
            messagebox.showerror("CRI connection error", str(exc))

    def press(self, event):
        if not (50 <= event.x <= 550 and 50 <= event.y <= 450):
            return

        self.held = True
        self.move_mouse(event)

    def release(self, event):
        self.held = False
        self.status.config(
            text="Released — no new targets queued"
        )

        if self.connected:
            threading.Thread(
                target=self.request_stop, daemon=True
            ).start()

    def stop(self):
        self.held = False
        self.status.config(text="STOP requested")

        with self.targets.mutex:
            self.targets.queue.clear()
            self.targets.not_full.notify()

        if self.connected:
            threading.Thread(
                target=self.request_stop, daemon=True
            ).start()

    def request_stop(self):
        try:
            self.robot.stop_move()
        except Exception as exc:
            self.last_error = str(exc)

    def move_mouse(self, event):
        if not (50 <= event.x <= 550 and 50 <= event.y <= 450):
            return

        x = X_MIN + (event.x - 50) / 500 * (X_MAX - X_MIN)
        y = Y_MAX - (event.y - 50) / 400 * (Y_MAX - Y_MIN)

        self.canvas.coords(
            self.dot,
            event.x - 5, event.y - 5,
            event.x + 5, event.y + 5
        )

        self.status.config(
            text=f"Target X={x:.1f}, Y={y:.1f}, Z={self.z:.1f} mm"
        )

        if self.held and self.connected:
            try:
                self.targets.put_nowait((x, y, self.z))
            except queue.Full:
                try:
                    self.targets.get_nowait()
                except queue.Empty:
                    pass

                try:
                    self.targets.put_nowait((x, y, self.z))
                except queue.Full:
                    pass

    def motion_worker(self):
        while self.connected:
            try:
                x, y, z = self.targets.get(timeout=0.1)
            except queue.Empty:
                continue

            if not self.held:
                continue

            try:
                result = self.robot.move_cartesian(
                    X=x, Y=y, Z=z,
                    A=0, B=0, C=180,
                    E1=0, E2=0, E3=0,
                    velocity=VELOCITY,
                    frame=FRAME,
                    wait_move_finished=True,
                    move_finished_timeout=COMMAND_TIMEOUT,
                    acceleration=ACCELERATION,
                )

                if result is False:
                    self.last_error = (
                        "Controller rejected motion command"
                    )
                    self.held = False
                    self.root.after(
                        0,
                        lambda msg=self.last_error:
                        self.status.config(text=msg)
                    )
                    break

            except Exception as exc:
                self.last_error = (
                    f"{type(exc).__name__}: {exc}"
                )
                self.held = False
                self.root.after(
                    0,
                    lambda msg=self.last_error:
                    self.status.config(text=f"Motion error: {msg}")
                )
                break

    def close(self):
        self.held = False
        self.connected = False

        if self.robot is not None:
            try:
                self.robot.stop_move()
            except Exception:
                pass

            try:
                self.robot.close()
            except Exception:
                pass

        self.root.destroy()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--physical", action="store_true")
    args = parser.parse_args()

    if args.physical and not PHYSICAL_MOTION_ENABLED:
        raise SystemExit(
            "Physical mode is locked. Verify workspace, tool frame "
            "and stop behaviour before enabling PHYSICAL_MOTION_ENABLED."
        )

    root = tk.Tk()
    app = MouseRobot(root)
    root.mainloop()