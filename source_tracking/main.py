import sys
from Controls import Rot2Prog
from Tracking import SourceTracking  # Adjust the import if needed.
from astropy.coordinates import SkyCoord
from astropy import units as u

def print_help():
    """
    Print usage instructions for the interactive commands.
    """
    print(
        """
    Available Commands:
    ------------------
    help or h
        Show this help message.

    t <L> <B>
        Track a target at galactic coordinates L, B continuously.
        Example: t 10 10

    s <L> <B>
        Slew immediately to the specified galactic coordinates (L, B).
        Example: s 10 15

    s <Az> <El> azel
        Slew immediately to specified horizontal coords (Az, El) in degrees.
        Example: s 180 45 azel

    r
        Restart the rotator.

    status
        Query and display the current Az, El from the hardware.

    off or exit or q
        Terminate the program and exit.
    """
    )

def main():
    print("Welcome to the Interactive Telescope Terminal")

    # Instantiate the hardware control
    try:
        control = Rot2Prog()  # by default reads 'config.yml'
        print("Rot2Prog control initialized.")
    except Exception as e:
        print(f"Error initializing Rot2Prog: {e}")
        control = None

    # Instantiate the source tracking system
    rotor = SourceTracking(control=control)

    while True:
        try:
            cmd = input("\nEnter command (type 'help' for options): ").strip().lower()
        except KeyboardInterrupt:
            print("\n[Ctrl+C detected] Command input interrupted. Continuing...")
            continue

        if not cmd:
            continue

        if cmd in ["help", "h"]:
            print_help()
            continue

        if cmd in ["off", "exit", "quit", "q", "shutdown"]:
            print("\n...Shutting down...\n")
            if control is not None:
                try:
                    rotor.stow()
                except Exception as e:
                    print(f"Error with rotator: {e}")
            break

        if cmd == "r":
            if control is not None:
                try:
                    control.Restart()
                except Exception as e:
                    print(f"Error restarting rotator: {e}")
            else:
                print("No rotator control available to restart.")
            continue

        # Continuous tracking: t <L> <B>
        if cmd.startswith("t "):
            parts = cmd.split()
            if len(parts) != 3:
                print("Error: Usage: t <L> <B> (e.g., t 10 10)")
                continue
            try:
                l_val = float(parts[1])
                b_val = float(parts[2])
            except ValueError:
                print("Invalid numeric values for L, B.")
                continue

            rotor.track_target(l_val, b_val, update_time=5)
            continue

        # Slewing: s <L> <B>  OR  s <Az> <El> azel
        if cmd.startswith("s "):
            parts = cmd.split()
            if len(parts) == 3:
                try:
                    L_val = float(parts[1])
                    B_val = float(parts[2])
                except ValueError:
                    print("Invalid numeric values for L, B.")
                    continue

                # Convert Galactic coordinates to horizontal (Az, El)
                _, az, el = rotor.tracking_galactic_coordinates(L_val, B_val)
                try:
                    rotor.slew(az, el, override=False)
                    rotor.current_lb = SkyCoord(l=L_val*u.deg, b=B_val*u.deg, frame='galactic')
                except Exception as e:
                    print(f"Error in galactic slew: {e}")

            elif len(parts) == 4 and parts[-1] == "azel":
                try:
                    az = float(parts[1])
                    el = float(parts[2])
                except ValueError:
                    print("Invalid numeric values for Az, El.")
                    continue

                try:
                    rotor.slew(az, el, override=True)
                    rotor.current_lb = None  # Unknown Galactic coordinates in this case.
                except Exception as e:
                    print(f"Error in az/el slew: {e}")
            else:
                print("Invalid usage. Try:\n  s <L> <B>\n  s <Az> <El> azel")
            continue

        if cmd.startswith("status"):
            if control is None:
                print("No rotator available to query status.")
            else:
                try:
                    az, el = control.status()
                    print(f"Az={round(az)}°, El={round(el)}°")
                except Exception as e:
                    print(f"Error reading status: {e}")
            continue

        print("Unknown command. Type 'help' to see available commands.")

    print("\nGoodbye!\n")

if __name__ == "__main__":
    main()
