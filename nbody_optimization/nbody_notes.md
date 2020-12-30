# Assignment 3 Notes

The assignment here was to reduce the runtime of the program from about 90 seconds to about 30 seconds. However, on my machine the runtime of the original program is much longer than 90 seconds; it usually takes about 150-200 seconds. The runtime of the optimized version is also inconsistent, ranging from about 50-75 seconds. It's reduced to about one third of the original time - good enough.

The files are as follows:
   - nbody_00_original: the script found in the initial assignment. I have added timing functionality but have left the program itself untouched.
   - nbody_01_functions: this version contains changes designed to reduce function overhead.
   - nbody_02_variables: this version contains changes designed to reduce the useage of global variables.
   - nbody_03_looping: this version contains changes designed to reduce the amount of work done in loops.
   - nbody_04_built_in: this version contains changes designed to utilize built in functionalities. There is one change that didn't perform right, so I left it as a comment until I can debug.
   - nbody_opt_03: compiles all the changes into a single optimized program.

# Assignment 5 Notes

The files are as follows:
   - nbody_05_itertools: the script has been modified to use itertools.
   - nbody_opt_05: compiles all the changes into a single opptimized program.
