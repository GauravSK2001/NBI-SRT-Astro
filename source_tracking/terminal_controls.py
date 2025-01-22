from Tracking import *
from Controls import *

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

    off or exit or q
        Terminate the program and exit.
    """
    )


def main():
    print("Welcome to the Interactive Telescope Terminal")

    # Instantiate the hardware control
    try:
        control = Rot2Prog()
        print("Rot2Prog control initialized.")
    except Exception as e:
        print(f"Error initializing Rot2Prog: {e}")
        control = None

    # Instantiate the high-level source tracking, passing in the control
    rotor = source_tracking(control=control)

    # Main command loop
    while True:
        cmd = input("\nEnter command (type 'help' for options): ").strip().lower()

        if not cmd:
            continue

        if cmd in ["help", "h"]:
            print_help()
            continue

        if cmd in ["off", "exit", "quit", "q", 'shutdown','off']:
            print("\n ...Shutting down... \n")
            # The rotator will be moved to stow mode.Need to add this 
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

        # ----------------------------------------------------------
        # T <L> <B> => continuous tracking
        # This starts or continues the 5-second update cycle
        # ----------------------------------------------------------
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

            # Set the rotor's current galactic coords
            rotor.current_lb = SkyCoord(l=l_val*u.deg, b=b_val*u.deg, frame='galactic')
            print(f"\nTarget galactic coordinates set to: L={l_val:.2f}°, B={b_val:.2f}°.\n")
            # Start or continue the monitoring loop
            rotor._monitor_pointing(update_time=5)
            # If user hits Ctrl+C, we'll return here
            continue

        # ----------------------------------------------------------
        # Slew => s ...
        #   s <L> <B>  or  s <Az> <El> azel
        # ----------------------------------------------------------
        if cmd.startswith("s "):
            parts = cmd.split()

            # 3 parts => presumably s <L> <B> (galactic)
            if len(parts) == 3:
                try:
                    L = float(parts[1])
                    B = float(parts[2])
                except ValueError:
                    print("Invalid numeric values for L, B.")
                    continue

                current_time, az, el = rotor.tracking_galactic_coordinates(L, B)
                # Attempt immediate slew
                try:
                    rotor.set_pointing(az, el)
                    rotor.current_azel = SkyCoord(alt=el*u.deg, az=az*u.deg, frame='altaz')
                    rotor.current_lb = SkyCoord(l=L*u.deg, b=B*u.deg, frame='galactic')
                    rotor.telescope_pointing = rotor.current_azel
                    print(f"Slewed to galactic L={L:.2f}°, B={B:.2f}° => "
                        f"Az={round(az)}°, El={round(el)}°")
                except Exception as e:
                    print(f"Error in galactic slew: {e}")

            # 4 parts => s <Az> <El> azel
            elif len(parts) == 4 and parts[-1] == "azel":
                try:
                    az = float(parts[1])
                    el = float(parts[2])
                except ValueError:
                    print("Invalid numeric values for Az, El.")
                    continue

                # Attempt to slew to these horizontal coordinates
                try:
                    rotor.set_pointing(az, el)
                    rotor.current_azel = SkyCoord(alt=el*u.deg, az=az*u.deg, frame='altaz')
                    rotor.telescope_pointing = rotor.current_azel
                    rotor.current_lb = None  # We don't know the galactic coords here
                    print(f"Slewed to horizontal Az={round(az)}°, El={round(el)}°")
                except Exception as e:
                    print(f"Error in az/el slew: {e}")
            else:
                print("Invalid usage. Try:\n  s <L> <B>\n  s <Az> <El> azel")
            continue

        # ----------------------------------------------------------
        # Unknown command
        # ----------------------------------------------------------
        print("Unknown command. Type 'help' to see available commands.")

    print("\nGoodbye!\n")


if __name__ == "__main__":
    main()

