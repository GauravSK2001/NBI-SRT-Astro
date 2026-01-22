import sys
from Controls import Rot2Prog
import Controls_simulator as sim_ctrl
from Tracking import SourceTracking  # Adjust the import if needed.
from astropy.coordinates import SkyCoord,Longitude
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
        Restart the rotor.

    status
        Query and display the current Az, El from the hardware.

    off or exit or q
        Terminate the program and exit.
    """
    )

def main():
    print("Welcome to the Interactive Telescope Terminal")

    # Instantiate the hardware control
    port_master = "COM3"  # Update this to your actual port
    
    interferometryMode = True  # Set to True if using both dishes in interferometry mode
    port_slave = "COM4"   # Update this to your actual port, or set to None if not used
    
    try:
        control_master = Rot2Prog(port_master)  # by default reads 'config.yml'
        print("Rot2Prog control initialized.")
    except Exception as e:
            print(f"Error initializing Rot2Prog: {e} \nFalling back to simulator.")
            control_master = sim_ctrl.Simulator_Rot2Prog(4)

    if interferometryMode:
        try:
            control_slave = Rot2Prog(port_slave)  # by default reads 'config.yml'
            print("Slave Rot2Prog control initialized.")
        except Exception as e:
            print(f"Error initializing Slave Rot2Prog: {e} \nFalling back to simulator.")
            control_slave = sim_ctrl.Simulator_Rot2Prog(3)
    else:
        control_slave = None


    # Instantiate the source tracking system
    rotor = SourceTracking(control_master = control_master, control_slave = control_slave)

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

        if cmd.split()[0] in ["off", "exit", "quit", "q", "shutdown"]:
            print("\n...Shutting down...\n")
            parts = cmd.split()

            if len(parts) > 1 and parts[1] in ["stow", "s"]:
                if control_master is not None:
                    try:
                        rotor.stow()
                    except Exception as e:
                        print(f"Error with rotor: {e}")
            break

        if cmd == "r":
            if control_master is not None:
                try:
                    rotor.restart_rotor()
                    print("Rotator restarted successfully.")
                except Exception as e:
                    print(f"Error restarting rotor: {e}")
            else:
                print("No rotor control available to restart.")
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
            try:
                
                rotor.track_target(l_val, b_val, update_time=5)
            except ValueError as e:
                print(f"Error tracking target: {e}")
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
            if control_master is None:
                print("No rotor available to query status.")
            else:
                try:
                    az, el = rotor.get_current_telescope_az_el()
                    #az, el = Longitude(az,unit=u.deg,wrap_angle=360*u.deg).deg, el
                    print(f"Master status: Az={round(az)}°, El={round(el)}°")
                except Exception as e:
                    print(f"Error reading status: {e}")
                

                if control_slave is not None:
                    try:
                        az, el = rotor.get_current_slave_az_el()
                        #az, el = Longitude(az,unit=u.deg,wrap_angle=360*u.deg).deg, el
                        print(f"Slave status: Az={round(az)}°, El={round(el)}°")
                    except Exception as e:
                        print(f"Error reading status of slave: {e}")
            
            continue


        print("Unknown command. Type 'help' to see available commands.")

    print("\nGoodbye!\n")

if __name__ == "__main__":
    main()
