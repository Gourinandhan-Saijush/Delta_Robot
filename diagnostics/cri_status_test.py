import time
from pprint import pprint
from cri_lib import CRIController

# Physical igus controller settings
ROBOT_IP = "192.168.3.11"
CRI_PORT = 3920


def main():
    controller = CRIController()

    try:
        print("Connecting to igus controller...")
        print(f"Target: {ROBOT_IP}:{CRI_PORT}")

        connected = controller.connect(ROBOT_IP, CRI_PORT)

        if not connected:
            print("Connection failed. Check IP address and CRI port.")
            return

        print("CRI connection established.")
        time.sleep(2)

        print("\nLatest robot state:")
        pprint(controller.robot_state)

        print("\nRead-only diagnostic finished.")
        print("No motion or digital outputs were commanded.")

    except Exception as error:
        print(f"Error: {type(error).__name__}: {error}")

    finally:
        try:
            controller.close()
            print("Connection closed.")
        except Exception as error:
            print(f"Close warning: {error}")


if __name__ == "__main__":
    main()