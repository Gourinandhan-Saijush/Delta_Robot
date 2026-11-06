
import time
from cri_lib import CRIController

ROBOT_IP = "192.168.3.11"
CRI_PORT = 3920

BLOWOFF_OUTPUT = 23
SUCTION_OUTPUT = 22


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

def move_linear(
    controller,
    x,
    y,
    z,
    velocity,
    acceleration=40,
):
    """Move to a Cartesian target in the #base frame."""

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
        velocity=velocity,
        frame="#base",
        wait_move_finished=True,
        move_finished_timeout=300.0,
        acceleration=acceleration,
    )

    if not success:
        raise RuntimeError(
            f"Movement failed for target X={x}, Y={y}, Z={z}"
        )


def set_output(controller, output_id, state):
    """Set a digital output and stop if the command fails."""

    success = controller.set_dout(output_id, state)

    if success is False:
        raise RuntimeError(
            f"Failed to set DOut{output_id} to {state}"
        )


def main():
    controller = CRIController()

    try:
        print(f"Connecting to {ROBOT_IP}:{CRI_PORT}...")

        if not controller.connect(ROBOT_IP, CRI_PORT):
            raise RuntimeError("Could not connect to the robot.")

        print("Connected.")

        input(
            "\nAfter completing the required safety checks in iRC, "
            "press Enter to continue, or Ctrl+C to cancel: "
        )

        print("Step 1: Move to X=0, Y=0, Z=110")
        move_linear(controller, 0, 0, 110, velocity=100)

        print("Step 2: Move to X=0, Y=90, Z=-110")
        move_linear(controller, 0, 90, -110, velocity=400)

        print("Step 3: Set DOut22 OFF")
        set_output(controller, BLOWOFF_OUTPUT, False)

        print("Step 4: Set DOut23 ON")
        set_output(controller, SUCTION_OUTPUT, True)

        print("Step 5: Move to X=0, Y=90, Z=110")
        move_linear(controller, 0, 90, 110, velocity=400)

        print("Step 6: Move to X=0, Y=-90, Z=110")
        move_linear(controller, 0, -90, 110, velocity=400)

        print("Step 7: Move to X=0, Y=-90, Z=-90")
        move_linear(controller, 0, -90, -90, velocity=400)

        print("Step 8: Set DOut23 OFF")
        set_output(controller, SUCTION_OUTPUT, False)

        print("Step 9: Set DOut22 ON")
        set_output(controller, BLOWOFF_OUTPUT, True)

        print("\nSequence completed.")

    except KeyboardInterrupt:
        print("\nCancelled by user.")

    except Exception as error:
        print(f"\nError: {type(error).__name__}: {error}")

    finally:
        try:
            controller.close()
            print("Connection closed.")
        except Exception as error:
            print(f"Connection-close warning: {error}")


if __name__ == "__main__":
    main()
