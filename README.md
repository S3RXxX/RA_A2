# Randomized Algorithms (RA-MIRI): Assignment #2
Done by:
    - Sergi Guimerà Roig
    - Iván Sánchez Gala

# Project Structure
- ***.pdf:** Task statement.
- **bins.py:** Code where class Bins is created and it contains all asked and auxiliar functions.
- **exp$.py:** Experimentation changing values of Bins.
- **exp$plots.py:** Code to generate plots from the experimentation.
- **exp$metricsplots.py:** Code to generate plots of the std of gap from the different executions of each experiment.
- ***.csv:** Saved data from the experimentation.
- **./exp$:** Folder to save the plots.
# Requirements
numpy>=1.26

pandas>=2.2

matplotlib>=3.8

Code executed with python 3.12.4

# Env
python3 -m venv env

Linux/Macos -> source env/bin/activate

Windows -> .\env\Scripts\Activate

pip install -r requirements.txt

# Bins tutorial
To simulate any experiment the first you need to do is create the object Bins:

**Bins(m=m, seed=seed)**

Where m is the number of bins and seed is a number to allow replicability.

Finally, to execute the simulation you need to execute:

**bins.simulate(d=d, n=n, beta=beta, b_size=b_batch) #Without uncertainty**

or

**bins.simulate_uncertainty(d=d, n=n, beta=beta, b_size=b_batch) # With uncertainty**

Where d is the number of bins selected at random with replacements to select the bin where the ball will go, n is the number of balls the program will put into the bins, beta is the probability of using the d-choice rule or the probability of choosing the scenario where k=2 when the experiment is with uncertainty, and b_size is the batch size.

To execute the different experiments you need to execute:

python3 exp$.py #$ is the experiment number

To execute the plots:

python3 exp$plots.py # gap plots

python3 exp$metricsplots.py # for the plots regarding the standard deviaton of the gap
