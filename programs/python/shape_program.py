
import math
from cri_lib import CRIController

ROBOT_IP = "192.168.3.11"
CRI_PORT = 3920

DRY_RUN = False

FRAME = "#base"
VELOCITY = 50       # mm/s
ACCELERATION = 40

def check_robot_ready(controller):
    """Check status before allowing the program to proceed."""

    state = controller.robot_state

    referencing = state.referencing_state
    operation = state.operation_mode

    print("Referencing status:", referencing.global_state)
    print("Operation mode:", operation)
    print("Active control:", state.active_control)

    if referencing.mandatory and str(referencing.global_state).endswith(
        "NOT_REFERENCED"
    ):
        raise RuntimeError(
            "Robot is not referenced. Complete referencing in iRC first."
        )

    if not state.active_control:
        raise RuntimeError(
            "Active control is not enabled. Check the controller in iRC."
        )

    if str(operation).endswith("NOT_ENABLED"):
        raise RuntimeError(
            "Robot is not enabled. Check the controller in iRC."
        )

    print("Basic readiness checks passed.")


def main():
    controller = CRIController()

    try:
        print(f"Connecting to {ROBOT_IP}:{CRI_PORT}...")

        if not controller.connect(ROBOT_IP, CRI_PORT):
            raise RuntimeError("Could not connect to robot.")

        time.sleep(2)
        check_robot_ready(controller)
    except Exception as error:
        print(f"Program stopped: {type(error).__name__}: {error}")

    finally:
        try:
            controller.close()
        except Exception:
            pass

        print("Connection closed.")



def make_shape(shape, center_x, center_y, z, size, points=40):
    """Generate Cartesian points for a shape in millimetres."""

    path = []

    if shape == "square":
        half = size / 2
        path = [
            (center_x - half, center_y - half, z),
            (center_x + half, center_y - half, z),
            (center_x + half, center_y + half, z),
            (center_x - half, center_y + half, z),
            (center_x - half, center_y - half, z),
        ]

    elif shape == "triangle":
        radius = size / 2
        for i in range(4):
            angle = math.radians(90 + i * 120)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            path.append((x, y, z))

    elif shape == "circle":
        radius = size / 2
        for i in range(points + 1):
            angle = 2 * math.pi * i / points
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            path.append((x, y, z))

    else:
        raise ValueError("Choose square, triangle, or circle.")

    return path


def preview_path(path):
    print("\nGenerated robot path (millimetres):")
    for i, (x, y, z) in enumerate(path, start=1):
        print(
            f"Point {i:02d}: "
            f"X={x:.2f}, Y={y:.2f}, Z={z:.2f}"
        )
    print(f"\nTotal points: {len(path)}")


def run_robot(path):
    controller = CRIController()

    try:
        print(f"\nConnecting to {ROBOT_IP}:{CRI_PORT}...")
        if not controller.connect(ROBOT_IP, CRI_PORT):
            print("Connection failed. No motion commanded.")
            return

        print("Connected.")

        confirmation = input(
            "\nCheck the robot, tool, coordinate frame, and complete "
            "path in your lab's approved procedure. "
            "Type MOVE to send the path: "
        )

        if confirmation != "MOVE":
            print("Cancelled. No motion commanded.")
            return

        for i, (x, y, z) in enumerate(path, start=1):
            print(
                f"Sending point {i}/{len(path)}: "
                f"X={x:.2f}, Y={y:.2f}, Z={z:.2f}"
            )

            success = controller.move_cartesian(
                X=x,
                Y=y,
                Z=z,
                A=0,
                B=0,
                C=180,
                E1=0,
                E2=0,
                E3=0,
                velocity=VELOCITY,
                frame=FRAME,
                wait_move_finished=True,
                move_finished_timeout=30,
                acceleration=ACCELERATION,
            )

            if success is False:
                print("Motion command failed. Stopping the sequence.")
                return

        print("Path sequence finished.")

    except Exception as error:
        print(f"\nRobot command error: {type(error).__name__}: {error}")
        print("Do not assume the robot stopped safely; check its state.")

    finally:
        try:
            controller.close()
            print("CRI connection closed.")
        except Exception as error:
            print(f"Connection close warning: {error}")


def main():
    print("IGUS DELTA — SHAPE TO MOTION")
    print("Shapes: square, triangle, circle")

    shape = input("Choose shape: ").strip().lower()

    center_x = float(input("Shape centre X (mm): "))
    center_y = float(input("Shape centre Y (mm): "))
    z = float(input("Drawing height Z (mm): "))
    size = float(input("Shape size / diameter (mm): "))

    if size <= 0:
        print("Size must be greater than zero.")
        return

    path = make_shape(
        shape=shape,
        center_x=center_x,
        center_y=center_y,
        z=z,
        size=size,
    )

    preview_path(path)

    if DRY_RUN:
        print("\nPREVIEW ONLY: no robot connection or movement.")
        print("Review the coordinates before considering execution.")
        return

    run_robot(path)


if __name__ == "__main__":
    main()
