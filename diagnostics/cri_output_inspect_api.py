import inspect
from cri_lib import CRIController

controller = CRIController()

try:
    print("Output-related methods:\n")

    for name in dir(controller):
        if any(word in name.lower() for word in (
            "output", "digital", "dout", "io", "signal"
        )):
            member = getattr(controller, name)

            if callable(member):
                try:
                    signature = inspect.signature(member)
                except (TypeError, ValueError):
                    signature = "(signature unavailable)"

                print(f"{name}{signature}")

    print("\nCartesian movement method source:\n")

    print(inspect.getsource(CRIController.move_cartesian))

finally:
    try:
        controller.close()
    except Exception:
        pass

    print("\nInspection finished.")