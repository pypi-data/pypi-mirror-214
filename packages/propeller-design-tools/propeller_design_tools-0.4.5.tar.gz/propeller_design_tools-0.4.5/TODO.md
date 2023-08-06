PDT To-Do List
==============
High-Priority (soon)
--------------------
1. Make PDT create the user-set directories on setting if they don't exist yet
2. Make the main Propeller() plot number into Newtons/kW
3. Figure out why my example PNG files are not showing on Github or PyPi
4. Offer the built GUI for Windows for free (how? do I need a website to host the download? how to push updates?)
5. Consider a 1x iterative scheme to "go back" and re-calculate stations parameters
   after a successful Propeller() creation returned from XROTOR, and we actually know what
   the chords of each station are, so we can update the "1/10th of the local radius" estimate

Backlog (med-priority)
----------------------
* Is atmo_props['altitude'] input in km or m (just rename it altitude_km)?
* Implement units for all input parameters (rename them all with units on end)
* Add a "Cm_const" callout to the RadialStation plot
* Work on better / non-buggy implementation of > 1 RadialStations in propeller creation
* Work on propeller "analysis sweeps" to gain access to more of the XROTOR functionality
(example5_prop_analysis.py)
* Work on propeller optimization routines (example6_grid_optimizer.py)
* Scale the size of the velocity vectors in the propeller 3d plot

Wishlist (low-priority)
-----------------------
* Consider ways to generate hub and blade/hub interface geometries (or give user option to modify, maybe via a file?)
* Consider ways to "cut in" in the blade chords near the hub when using design_vorform='pot' or 'grad' (via file?)
* Finish the optimization code
* Fully vet-out / check and troubleshoot every single aspect of the GUI to ensure no errors or crashes
* Integrate Ads into the GUI for revenue
* Should I add pure-python implementations of XFOIL and XROTOR? What are the advantages, if any?
* Eliminate the user's need to even input a value for the desired blade cl distribution altogether (as an option).

Completed (tracking)
--------------------
* Create this $hit
* Git Gud at coding - obtain & integrate XFOIL and XROTOR source code such that
  the user no longer needs to get the executables themselves, the entire package is
  finally self-contained - or other ways to make PDT a "complete package"
* Consider ways to automate the downloading of coordinate files
* Consider ways to automate the generation of airfoil polar data
* Determine best way to indicate all input parameter units & implement
* Make it all work as long as XFOIL and XROTOR are in the correct directory
*
