# MSManalysis

## Description

This python program allows an easy and interactive analysis of Markov State Models (MSMs) generated with deeptime library.
Users can provide a list of MSMs at different lagtimes with the microstates used to generate the MSMs, then test the markovianity and compute kinetical data (mean first passage times and event rates).

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Available command](#available-command)
- [Examples](#examples)
- [License](#license)
- [Contact](#contact)

---

## Installation

To install the directory from GitHub:

```bash
# Clone the repository
git clone https://github.com/SNS-Brancato-Lab/MSManalysis.git

# Navigate to the script directory
cd MSManalysis

# Install all the required modules
pip install -r requirements.txt
```

In order to use the program, the following modules must be installed:

- deeptime
- numpy
- matplotlib
- scipy
- pickle

---

## Usage

MSManalysis works provinding commands in the terminal. Commands can be provided inside an input file (batch mode) or inserted directly in the command line (interactive mode).

a. **Batch mode**

```bash
# Batch mode
python main.py -i input.in
```

'input.in' is a text file containing commands for the analysis of MSMs.

b. **Interactive mode**

```bash
# Batch mode
python main.py
```

Interactive mode is automatically activated if no command file is provided.

---

## Available command



## Examples

**Add references to a Zenodo repository with an example.**

---

## License

---

## Contact

For further information or any other request, please contact the autor at his email adress.

- **Author:** Luca Benedetti
- **Email:** [luca.benedetti@sns.it](mailto\:luca.benedetti@sns.it)
