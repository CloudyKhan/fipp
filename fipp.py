import re
import os
import sys

# Displays the ASCII art for fipp.py 
def show_intro():
    print(r"""
         __                 # Flexible 
       _/__\_               # Interactive 
       (⌐■_■)  <- fipp.py   # Password 
                            # Processor
                           
                            [ CloudyKhan | https://github.com/CloudyKhan ]
    """)

# Displays the help page (for lost souls)
def show_help():
    print("""
  ___  ___  ___  ___ 
 | __||_ _|| _ \| _ \\
 | _|  | | |  _/|  _/
 |_|  |___||_|  |_|  

Flexible Interactive Password Processor

usage: fipp.py [-h] [-l LENGTH] [-s] [-n] [-c CAPSLOCK] [-i INPUT] [-o OUTPUT] [-e ENCODING] [-I]

options:
  -h, --help               Show this help message and exit
  -l LENGTH, --length      Exact password length (default: 8)
  -s, --special            Allow passwords with special characters (default: no special characters, spaces are considered special characters)
  -n, --number             Allow passwords with numbers (default: no numbers)
  -c CAPSLOCK, --capslock  Minimum number of uppercase letters (optional, no uppercase letter check if omitted)
  -i INPUT, --input        Input password file (required)
  -o OUTPUT, --output      Output file for filtered passwords (can be a full file path or current directory)
  -e ENCODING, --encoding  Specify file encoding (default: ISO-8859-1, common options: UTF-8, UTF-16)
  -I, --interactive        Activate interactive mode

Example Usage:
  python3 fipp.py -l 8 -s -n -c 2 -i /path/to/input.txt -o /path/to/output.txt -e UTF-8
  python3 fipp.py -I

Notes:
  - If `-s` (special characters) or `-n` (numbers) are not specified, passwords with special characters, spaces, or numbers will be excluded by default.
  - If you're not sure about encoding, proceed with default (ISO-8859-1).
  """ )

# Ensure the output directory exists before writing the filtered passwords
def ensure_dir(file_path):
    output_dir = os.path.dirname(file_path)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created missing directory: {output_dir}")
        except OSError as err:
            print(f"Error creating directory: {err}")
            sys.exit(1)

# Check if a password contains any special characters 
def has_specials(pwd):
    return bool(re.search(r'[^a-zA-Z0-9]', pwd))  # Match anything that's not a letter or digit

# Check if a password contains any digits
def has_numbers(pwd):
    return bool(re.search(r'[0-9]', pwd))

# Check if a password contains the required number of uppercase letters
def has_uppercase(pwd, min_upper):
    return sum(1 for c in pwd if c.isupper()) >= min_upper

# Process the input password file and filter based on user-specified rules
def process_pw_file(length, allow_special, allow_num, min_upper, in_file, out_file, encoding):
    ensure_dir(out_file)  # Make sure the output directory is ready

    try:
        with open(in_file, 'r', encoding=encoding) as file_in, open(out_file, 'w', encoding=encoding) as file_out:
            total_pwds = sum(1 for line in file_in)  # Count total lines (passwords)
            file_in.seek(0)  # Reset file pointer to the start

            filtered_pwds = 0  # Track how many valid passwords we find
            
            # Start processing the password file line by line
            for pwd in file_in:
                pwd = pwd.strip()  # Clean whitespace

                # Check if password has the exact required length
                if len(pwd) != length:
                    continue
                
                # Check for special characters if allowed
                if not allow_special and has_specials(pwd):
                    continue

                # Check for digits if allowed
                if not allow_num and has_numbers(pwd):
                    continue

                # Check for uppercase letter requirement
                if min_upper and not has_uppercase(pwd, min_upper):
                    continue

                # Save the valid password to the output file
                file_out.write(pwd + '\n')
                filtered_pwds += 1  # Count how many passed the filters
            
            # Show user how many passwords made it through the filter
            print(f"\n[+] Original file had {total_pwds} lines (passwords).")
            print(f"[+] Filtered file has {filtered_pwds} lines (passwords).")
            print("[+] Processing completed successfully.")

    except FileNotFoundError as err:
        print(f"Error: {err}. Please ensure the file exists and the path is correct.")
    except UnicodeDecodeError as err:
        print(f"Error: There was an issue reading the file with the encoding '{encoding}'.")
        print("If you're unsure about the file encoding, try using UTF-8 or consult the file's source.")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

# Interactive mode to guide users through the filtering process
def run_interactive():
    # Show the cool ASCII intro art
    show_intro()

    try:
        # Add a nice separator line for clarity
        print("~" * 74)

        # Ask for minimum password length, default to 8 if left empty
        while True:
            length_input = input("> Enter the exact password length (default: 8): ")
            if length_input == '':
                length = 8  # Default length
                break
            if length_input.isdigit() and int(length_input) > 0:
                length = int(length_input)
                break
            else:
                print("Please enter a valid number.")

        # Ask if the user wants to allow special characters in the passwords
        while True:
            special_input = input("> Should the password allow special characters? (y/n, default: n): ").lower()
            if special_input == '':
                allow_special = False  # No special characters by default
                break
            if special_input in ['y', 'n']:
                allow_special = (special_input == 'y')
                break
            else:
                print("Please enter 'y' or 'n'.")

        # Ask if the user wants to allow numbers in the passwords
        while True:
            num_input = input("> Should the password allow numbers? (y/n, default: n): ").lower()
            if num_input == '':
                allow_num = False  # No numbers by default
                break
            if num_input in ['y', 'n']:
                allow_num = (num_input == 'y')
                break
            else:
                print("Please enter 'y' or 'n'.")

        # Ask if the password policy requires uppercase letters and, if so, how many
        while True:
            upper_input = input("> Does the password policy require uppercase letters? (y/n, default: n): ").lower()
            if upper_input == '':
                min_upper = None  # No uppercase letters required
                break
            if upper_input == 'y':
                while True:
                    upper_count = input("> How many uppercase letters should the password contain (at least)?: ")
                    if upper_count.isdigit() and int(upper_count) > 0:
                        min_upper = int(upper_count)
                        break
                    else:
                        print("Please enter a valid number.")
                break
            elif upper_input == 'n':
                min_upper = None  # No uppercase letter check
                break
            else:
                print("Please enter 'y' or 'n'.")

        # Get the input file path from the user
        while True:
            in_file_path = input("> Enter the path to the input password file: ")
            if in_file_path == '':
                print("Error: You must provide an input password file.")
            elif os.path.isfile(in_file_path):
                break
            else:
                print("File not found. Please provide a valid file path.")

        # Ask for the encoding type, offer common options
        print("\nAvailable encodings: ISO-8859-1 (default), UTF-8, UTF-16")
        encoding_input = input("> Enter file encoding (press Enter for default ISO-8859-1): ").upper()
        if encoding_input == '':
            encoding = 'ISO-8859-1'  # Default encoding
        elif encoding_input in ['ISO-8859-1', 'UTF-8', 'UTF-16']:
            encoding = encoding_input
        else:
            print("Unsupported encoding, defaulting to ISO-8859-1.")
            encoding = 'ISO-8859-1'

        # Get the output file path from the user
        while True:
            out_file_path = input("> Enter the path for the filtered output file (default: ./output.txt): ")
            if out_file_path == '':
                out_file_path = "./output.txt"  # Default to output.txt in current directory
            ensure_dir(out_file_path)
            break

        # Process the passwords with the given options
        print("\n[+] Processing Password File...")
        process_pw_file(length, allow_special, allow_num, min_upper, in_file_path, out_file_path, encoding)

    except KeyboardInterrupt:
        print("\n[+] Process interrupted by user. Exiting gracefully...")
        sys.exit(0)

# Main function to handle command-line arguments and trigger the appropriate mode
def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        show_help()  # Display help message
        sys.exit(0)

    # Check if interactive mode is triggered
    if '-I' in sys.argv:
        run_interactive()
        sys.exit(0)

    # If no parameters are provided, show an error and help
    if len(sys.argv) == 1:
        show_help()
        sys.exit(1)

    # Handle other command-line options for length, special chars, numbers, input/output files, etc.
    args = sys.argv[1:]

    length = 8  # Default length
    allow_special = False  # No special characters by default
    allow_num = False  # No numbers by default
    min_upper = None  # No uppercase letter requirement by default
    in_file_path = None
    out_file_path = "./output.txt"
    encoding = 'ISO-8859-1'  # Default encoding

    # Parse arguments manually
    i = 0
    while i < len(args):
        try:
            if args[i] in ['-l', '--length']:
                if i + 1 < len(args):
                    length = int(args[i + 1])
                    i += 1
                else:
                    raise ValueError("Missing value for argument '-l' (length).")
            elif args[i] in ['-s', '--special']:
                allow_special = True
            elif args[i] in ['-n', '--number']:
                allow_num = True
            elif args[i] in ['-c', '--capslock']:
                if i + 1 < len(args) and args[i + 1].isdigit():
                    min_upper = int(args[i + 1])
                    i += 1
                else:
                    raise ValueError("Missing or invalid value for argument '-c' (capslock).")
            elif args[i] in ['-i', '--input']:
                if i + 1 < len(args):
                    in_file_path = args[i + 1]
                    i += 1
                else:
                    raise ValueError("Missing value for argument '-i' (input file).")
            elif args[i] in ['-o', '--output']:
                if i + 1 < len(args):
                    out_file_path = args[i + 1]
                    i += 1
                else:
                    raise ValueError("Missing value for argument '-o' (output file).")
            elif args[i] in ['-e', '--encoding']:
                if i + 1 < len(args):
                    encoding = args[i + 1].upper()
                    i += 1
                else:
                    raise ValueError("Missing value for argument '-e' (encoding).")
        except ValueError as e:
            print(f"Error: {e}")
            show_help()
            sys.exit(1)
        i += 1

    if not in_file_path:
        print("Error: Input file is required.")
        show_help()
        sys.exit(1)

    process_pw_file(length, allow_special, allow_num, min_upper, in_file_path, out_file_path, encoding)

if __name__ == "__main__":
    main()
