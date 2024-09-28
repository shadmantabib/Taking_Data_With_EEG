# Taking Data with EEG

Welcome to the **Taking_Data_With_EEG** project! This project helps you capture and analyze EEG data using the `mindwave.py` script.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Data Output](#data-output)

## Overview

The `mindwave.py` script allows you to:
- Capture EEG data for a specified duration (currently set to 60 seconds).
- Store the collected data in a CSV file for further analysis.

## Installation

To run `mindwave.py`, you'll need to have a Python environment set up with all the required dependencies. Here's how you can do it:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/shadmantabib/Taking_Data_With_EEG.git
   cd Taking_Data_With_EEG
   ```

2. **Create a Virtual Environment**

   Ensure you have virtualenv installed. If not, install it using:

   ```bash
   pip install virtualenv
   ```

   Then create and activate the virtual environment:

   ```bash
   virtualenv eeg_env

   # Windows
   .\eeg_env\Scripts\activate

   # Mac/Linux
   source eeg_env/bin/activate
   ```

3. **Install Dependencies**

   Install the required packages using requirements.txt:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start recording EEG data, simply run the script:

```bash
python mindwave.py
```

## Data Output

The data collected is stored as a CSV file in the current working directory.
