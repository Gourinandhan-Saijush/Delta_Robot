
import inspect
from cri_lib import CRIController

controller = CRIController()

try:
    print("Connecting to igus controller...")
    connected = controller.connect("192.168.3.11", 3920)

    if not connected:
        print("Connection failed.")
    else:
        print("\nRelevant CRI methods:\n")

        for name in dir(controller):
            if any(word in name.lower() for word in (
                "move", "linear", "cart", "output",
                "digital", "program", "active", "enable"
            )):
                member = getattr(controller, name)

                if callable(member):
                    try:
                        signature = inspect.signature(member)
                    except (TypeError, ValueError):
                        signature = "(signature unavailable)"

                    print(f"{name}{signature}")

finally:
    controller.close()
    print("\nConnection closed.")
