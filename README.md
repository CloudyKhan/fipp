# fipp.py - Flexible Interactive Password Processor

**fipp.py** is a flexible, interactive password processor that filters and customizes password lists based on length, special characters, numbers, uppercase requirements, and encoding, with both command-line and interactive modes. It can be tailored and customized to fit a wide variety of Password Policies.

### Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Options](#command-line-options)
  - [Interactive Mode](#interactive-mode)
  - [Examples](#examples)
- [File Encoding](#file-encoding)
  - [Converting Encoding](#converting-encoding)



---

## Features
- **Filter passwords by length**: Set exact password length requirements.
- **Allow or disallow special characters**: Customize whether special characters should be included.
- **Control inclusion of numbers**: Choose whether to allow numbers in the passwords.
- **Enforce uppercase letters**: Specify the minimum number of uppercase letters required.
- **Support for multiple encodings**: Handle password files encoded in `ISO-8859-1`, `UTF-8`, and `UTF-16`.
- **Interactive mode**: Provides step-by-step instructions for configuring options.
- **Graceful error handling**: Offers clear feedback on file-related or encoding issues.

---

## Installation

1. **Clone the Repository**:
    ```
    git clone https://github.com/CloudyKhan/fipp.git
    ```

2. **Navigate to the Directory**:
    ```
    cd fipp
    ```

3. **Ensure Python 3.x is Installed**:
    Make sure Python 3 is installed by running:
    ```
    python3 --version
    ```

    If Python is not installed, follow the [official Python installation guide](https://www.python.org/downloads/).

---

## Usage

### Command-Line Options:
Use the following command-line arguments to control the behavior of fipp.py:

```
usage: python3 fipp.py [-h] [-l LENGTH] [-s] [-n] [-c CAPSLOCK] [-i INPUT] [-o OUTPUT] [-e ENCODING] [-I]
```

| Option           | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `-h`, `--help`   | Show the help message and exit                                               |
| `-l LENGTH`      | Set the exact password length (default: 8)                                   |
| `-s`, `--special`| Allow passwords with special characters (default: no special characters)      |
| `-n`, `--number` | Allow passwords with numbers (default: no numbers)                           |
| `-c CAPSLOCK`    | Minimum number of uppercase letters (optional, no uppercase letter check if omitted)|
| `-i INPUT`       | Specify input password file (required)                                       |
| `-o OUTPUT`      | Specify output file for filtered passwords (default: `output.txt`)           |
| `-e ENCODING`    | Specify file encoding (default: ISO-8859-1, other options: UTF-8, UTF-16)    |
| `-I, --interactive` | Activate interactive mode                                                 |

---

### Interactive Mode:
In **interactive mode**, fipp.py will guide you through each filtering option, one by one. To start interactive mode, run:

```
python3 fipp.py -I
```

In this mode, you will:
- Enter the desired password length.
- Specify special characters and numbers.
- Set the minimum number of uppercase letters.
- Provide input/output file paths.
- Choose the file encoding.
- Meet fipp.py (ASCII).

### Examples:

#### Example 1: Filter Passwords by Length (8 characters)
```
python3 fipp.py -l 8 -i input_passwords.txt -o filtered_passwords.txt
```

#### Example 2: Allow Special Characters and Numbers
```
python3 fipp.py -l 10 -s -n -i input_passwords.txt -o filtered_passwords.txt
```

#### Example 3: Require at Least 2 Uppercase Letters
```
python3 fipp.py -l 8 -s -n -c 2 -i input_passwords.txt -o filtered_passwords.txt
```

---

## File Encoding

Check file encoding with:
```
file -i input_file
```

If your password file is encoded in a different format, fipp.py allows you to specify the encoding during execution. If you are unsure, the default encoding is **ISO-8859-1**.

### Converting Encoding
If your file is not in the desired encoding (for example, rockyou.txt is typically encoded in ISO-8859-1), you can convert it to another encoding using the following command on Linux:

```
iconv -f <source_encoding> -t <target_encoding> input_file -o output_file
```

Replace `input_file` with the name of your actual input file and `output_file` with the desired output filename.


---


**Happy password processing!** If you have any issues, feel free to reach out or contribute to the project.

