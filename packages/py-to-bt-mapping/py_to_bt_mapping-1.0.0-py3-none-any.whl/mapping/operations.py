import os, time, math, random, stat, win32security, subprocess, traceback, msvcrt, serial
from datetime import datetime

#software operations
#enter
def enter(data_source, variable_list=None, error_var=None):
    try:
        if data_source.startswith("@"):
            source = assignments.get(data_source)
            if source is None:
                raise ValueError(f"Assigned name {data_source} not found.")
        else:
            if os.path.exists(data_source):
                source = open(data_source, 'r')
            else:
                raise FileNotFoundError(f"File or device '{data_source}' not found.")
        if variable_list is None:
            record = source.readline()
            print(f"Skipped record: {record.strip()}")
            return
        record = source.readline()
        if not record.strip():  
            print("Blank line encountered, variables retain their values.")
            return
        data_items = record.strip().split()  
        data_pointer = 0
        for var in variable_list:
            if data_pointer >= len(data_items):
                break  
            item = data_items[data_pointer]
            if isinstance(var, int):  
                if item == ',':
                    continue  
                try:
                    var_value = float(item) if '.' in item else int(item)
                    globals()[var] = var_value
                except ValueError:
                    raise ValueError(f"Invalid numeric input '{item}'.")
            elif isinstance(var, str):  
                if len(item) > len(globals()[var]):  
                    remaining = len(item) - len(globals()[var])
                    globals()[var] = item[:len(globals()[var])]
                    data_items.insert(data_pointer + 1, item[-remaining:])
                else:
                    globals()[var] = item
            data_pointer += 1
        remaining_data = data_items[data_pointer:]
        if remaining_data:
            print(f"Remaining input discarded: {' '.join(remaining_data)}")
    except (FileNotFoundError, IOError, ValueError) as error:
        if error_var:
            globals()[error_var] = str(error)
        else:
            print(f"Error: {error}")
    finally:
        if not data_source.startswith("@") and 'source' in locals():
            source.close()

#File Operations
# msi$: msi() to return current working directory (cwd).
# msi: msi(dir) to change directory and then return new cwd.

def msi(dir = None, error_var = None):
    try:
        if dir == None:
            return os.getcwd()    
        else:
            if os.path.isdir(dir):
                os.chdir(dir)
                return os.getcwd()
            else:
                return "Not a valid directory" 
    except Exception as e:
        if error_var is not None:
            error_var = str(e)  
        else:
            return e

# pwd() is the same as msi$. Shows cwd.
def pwd():
    return os.getcwd()
        
def cd(dir, error_var = None):
    try:   
        if os.path.isdir(dir):
            os.chdir(dir)
        else: 
            return "Not a valid directory"
    except Exception as e:
        if error_var is not None:
            error_var = str(e)  
        else:
            return e
        
# assign to
assignments = {}
def assign_to(at_name, identifier, is_device=True, mode='text', error_var=None, access='write', es='exclusive', ano='over'):
    try:
        if identifier == "*":
            if at_name in assignments:
                assignments[at_name].close()
                del assignments[at_name]
                print(f"{at_name} has been cancelled and closed.")
            return 
        if at_name in assignments:
            assignments[at_name].close()
            del assignments[at_name]
        if is_device:
            if access == 'read':
                device = serial.Serial(identifier, baudrate=9600, timeout=1)  
            elif access == 'write' or ('read' in access and 'write' in access):
                device = serial.Serial(identifier, baudrate=9600, timeout=1, write_timeout=1)
            else:
                raise ValueError("Invalid access mode specified.")
            assignments[at_name] = device
            print(f"{at_name} assigned to device {identifier} with access '{access}' and mode '{mode}'.")      
        else:
            if access == 'read':
                if not os.path.exists(identifier):
                    raise ValueError(f"File '{identifier}' does not exist; 'read' access specified.")
                file_mode = 'r'
            elif access == 'write':
                if ano == 'new' and os.path.exists(identifier):
                    raise ValueError(f"File '{identifier}' already exists; 'new' access specified.")
                elif ano == 'over':
                    file_mode = 'w'
                elif ano == 'append':
                    file_mode = 'a'
                else:
                    file_mode = 'w'
            elif 'read' in access and 'write' in access:
                file_mode = 'r+' if os.path.exists(identifier) else 'w+'
            else:
                raise ValueError(f"Invalid access mode for file: {access}")
            if mode == 'binary':
                file_mode += 'b'            
            assigned_file = open(identifier, file_mode)
            if es == 'exclusive' and os.name == 'nt':
                msvcrt.locking(assigned_file.fileno(), msvcrt.LK_NBLCK, 1)           
            assignments[at_name] = assigned_file
            print(f"{at_name} assigned to file {identifier} with access '{access}', mode '{mode}', and {es} use.")
    except (FileNotFoundError, IOError, ValueError) as error:
        if error_var:
            globals()[error_var] = str(error)
        else:
            print(f"Error: {error}")

def get_permissions(path):
    """
    Converts file permissions to rwx/rwx/rwx format.
    """
    st = os.stat(path)
    perms = [
        stat.filemode(st.st_mode)[1:4],  # Owner permissions
        stat.filemode(st.st_mode)[4:7],  # Group permissions
        stat.filemode(st.st_mode)[7:10], # Others permissions
    ]
    return "/".join(perms)

def format_date(timestamp):
    """
    Formats the file's modification time into a readable date and time.
    """
    return time.strftime('%a %b %d %H:%M', time.localtime(timestamp))

def get_file_type(path):
    _, ext = os.path.splitext(path)
    if os.path.isdir(path):
        return "dir"
    elif ".o" in ext:
        return "obj" 
    else:
        return "src"

def get_owner_and_group(path):
    """
    Retrieves the owner and group names on Windows using pywin32.
    """
    sd = win32security.GetFileSecurity(path, win32security.OWNER_SECURITY_INFORMATION)
    owner_sid = sd.GetSecurityDescriptorOwner()
    owner_name, domain, type = win32security.LookupAccountSid(None, owner_sid)
    return owner_name, domain

def cat(directory_id=None, file_id=None, error_variable=None, option=None):
    if directory_id is None:
        directory_id = os.getcwd()
    if not os.path.isdir(directory_id):
        error_msg = f"Directory {directory_id} does not exist."
        if error_variable:
            print(f"Error: {error_variable} - {error_msg}")
        else:
            print(f"Error: {error_msg}")
        return
    try:
        entries = os.listdir(directory_id)
    except Exception as e:
        error_msg = str(e)
        if error_variable:
            print(f"Error: {error_variable} - {error_msg}")
        else:
            print(f"Error: {error_msg}")
        return
    select_filter = None
    short = False
    protect = False
    if option:
        if 'select' in option:
            parts = option.split('select ')
            if len(parts) > 1:
                select_filter = parts[1].split(',')[0].strip()  # Get the filter term before other options
        short = 'short' in option
        protect = 'protect' in option
    if select_filter:
        entries = [entry for entry in entries if entry.startswith(select_filter)]
    output_data = []
    for entry in entries:
        entry_data = entry
        entry_path = os.path.join(directory_id, entry)
        st = os.stat(entry_path)
        if protect:
            permissions = get_permissions(entry_path)
            owner, group = get_owner_and_group(entry_path)
            file_type = get_file_type(entry_path)
            entry_data = f"{permissions}  {owner:<7} {group:<7} {file_type:<5} {entry}"
        elif short:
            # Short Listing: only names of files and directories
            entry_data = entry
        else:
            # Standard listing: date, size, type, and name
            date = format_date(st.st_mtime)
            size = st.st_size
            file_type = get_file_type(entry_path)
            entry_data = f"{date}  {size:<7} {file_type:<5} {entry}"
        output_data.append(entry_data)
    if file_id:
        if os.path.exists(file_id):
            error_msg = f"File {file_id} already exists."
            if error_variable:
                print(f"Error: {error_variable} - {error_msg}")
            else:
                print(f"Error: {error_msg}")
            return
        try:
            with open(file_id, 'w') as f:
                f.write("\n".join(output_data))
            print(f"Directory listing written to {file_id}.")
        except Exception as e:
            error_msg = str(e)
            if error_variable:
                print(f"Error: {error_variable} - {error_msg}")
            else:
                print(f"Error writing to {file_id}: {error_msg}")
    else:
        for line in output_data:
            print(line)

def copy(sources, destination, error_var=None, first_line=None, last_line=None):
    #enter sources in a list eg. ["file1", "file2"]
    #if only 1 source file enter as just "file"
    if len(sources) == 1:
        sources = [sources] 
    # Validate all source files
    for source in sources:
        if not os.path.exists(source):
            if error_var is not None:
                error_var[0] = 1
            return f"Error: Source file '{source}' does not exist."
    lines_to_copy = []
    for source in sources:
        with open(source, 'r') as src_file:
            lines = src_file.readlines()
            if first_line is not None and last_line is not None:
                if first_line < 1 or last_line < 1 or first_line > len(lines) or last_line > len(lines):
                    if error_var is not None:
                        error_var[0] = 2
                    return "Error: Line numbers are out of bounds."
                lines_to_copy.extend(lines[first_line-1:last_line])
            elif first_line is not None:
                if first_line < 1 or first_line > len(lines):
                    if error_var is not None:
                        error_var[0] = 2
                    return "Error: First line number is out of bounds."
                lines_to_copy.extend(lines[first_line-1:])
            elif last_line is not None:
                if last_line < 1 or last_line > len(lines):
                    if error_var is not None:
                        error_var[0] = 2
                    return "Error: Last line number is out of bounds."
                lines_to_copy.extend(lines[:last_line])
            else:
                lines_to_copy.extend(lines)  
    with open(destination, 'w') as dest_file:
        dest_file.writelines(lines_to_copy)
    return f"{sources} copied over to {destination}"

def create_dir(dir_name, error_var = None):
    try:
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
            return "Directory created"
        else:
            raise FileExistsError("This directory exists.")
    except Exception as e:
        if error_var is not None:
            error_var = str(e)  
        else:
            return e

#create ascii
def create_ascii(file_id, error_var = None):
    try:
        if os.path.exists(file_id):
            raise FileExistsError("This file exists.")
        else:
            with open(file_id, 'w') as file:
                pass
            return f"File created: {file_id}"  
    except Exception as e:
        if error_var is not None:
            error_var = str(e)  
        else:
            return e

#link
def link(new_file_id, existing_file_id, error_var = None):
    try:
        if not os.path.exists(existing_file_id) or os.path.exists(new_file_id):
            return "error"
        # Create a hard link to the existing file with the new identifier
        if os.path.exists(existing_file_id) and not os.path.exists(new_file_id):
            os.link(existing_file_id, new_file_id)
            return f"Link created successfully: '{new_file_id}' -> '{existing_file_id}'"
    except Exception as e:
        if error_var is not None:
            error_var = str(e)  
        else:
            return e

#rename        
def rename(old_name, new_name, error_var = None):
    try:
        if not os.path.exists(old_name) or os.path.exists(new_name):
            return "error"
        if os.path.exists(old_name) and not os.path.exists(new_name):
            os.rename(old_name, new_name)
            return f"Renamed '{old_name}' to '{new_name}'."
    except Exception as e:
        if error_var is not None:
            error_var = str(e)  
        else:
            return e
        
#unlink
def unlink(identifier, error_var = None):
    try:
        if not os.path.exists(identifier):
            raise FileNotFoundError(f"Error: '{identifier}' does not exist.")
        if os.path.isfile(identifier):
            os.unlink(identifier)
            return f"Removed file link: '{identifier}'."
        elif os.path.isdir(identifier):
            os.rmdir(identifier)
            return f"Removed empty directory: '{identifier}'."
    except Exception as e:
        if error_var is not None:
            error_var = str(e)
        else:
            print(e)

#merge
def merge(primary_file_id, secondary_files):   
    """
    Merges lines from multiple secondary files into a primary file.
    Parameters:
    primary_file_id (str): The name of the primary file to be merged into.
    secondary_files (list of lists): A list where each list contains:
                                       [file_id, first_line (optional), last_line (optional)].
    """
    try:
        with open(primary_file_id, 'r') as pfile:
            workspace = pfile.readlines()
    except FileNotFoundError:
        raise ValueError(f"Primary file {primary_file_id} not found.")
    for file_info in secondary_files:
        secondary_file_id = file_info[0]
        first_line = file_info[1] if len(file_info) > 1 else None
        last_line = file_info[2] if len(file_info) > 2 else None
        try:
            with open(secondary_file_id, 'r') as sfile:
                secondary_content = sfile.readlines()
        except FileNotFoundError:
            raise ValueError(f"File {secondary_file_id} not found.")
        if first_line is not None and first_line < 0:
            raise ValueError(f"First line number must be a positive number.")
        if last_line is not None and last_line < 0:
            raise ValueError(f"Last line number must be a positive number.")
        first_line = first_line if first_line is not None else 0
        last_line = last_line + 1 if last_line is not None else len(secondary_content)
        if first_line >= len(secondary_content):
            raise ValueError(f"First line {first_line} is out of range for file {secondary_file_id}")
        last_line = min(last_line, len(secondary_content))
        lines_to_merge = secondary_content[first_line:last_line]
        if not workspace[-1].endswith('\n'):
            workspace.append("\n")
        workspace.extend(lines_to_merge)
    with open(primary_file_id, 'w') as pfile:
        pfile.writelines(workspace)
    return f"Merge completed and saved to {primary_file_id}"

#Flow Control
# Sleep
def wait(seconds):
    if seconds < 0:
        raise ValueError("The wait time must be non-negative.")
    elif seconds < 0.025:
        return
    else:
        time.sleep(seconds)

#Math Operations
#option bit
optionbit = 16
def option_bit(val, old_bits = 32):
    global optionbit
    val = round(val)
    if val == 32:
        optionbit = 32
        old_bits = 16
    elif val == 16:
        optionbit = 16
        old_bits = 32
    else:
        return "error - rounds to {}".format(val)

#rotate
def rotate(value, rotatebits):
    try:
        rotate_val = abs(rotatebits) % optionbit
        if rotatebits > 0:
            return (value >> rotate_val) | (value << (optionbit - rotate_val))
        elif rotatebits < 0:
            return (value << rotate_val) | (value >> (optionbit - rotate_val))
        return value
    except Exception as e:
        print(e)
    
#bincmp
def bincmp(n):
    try:
        return ~n
    except Exception as e:
        print(e)

#binand
def binand(val1, val2):
    return val1 & val2

#bineor
def bineor(val1, val2):
    return val1 ^ val2

#binior
def binior(val1, val2):
    return val1 | val2

#exor
def exor(val1, val2):
    if val1 != 0:
        val1 = 1
    if val2 != 0:
        val2 = 1
    return val1 ^ val2    

#bit
def bit(value, bit_no):
    bit_str = ""
    for i in range(optionbit, -1, -1):
        k = value >> i
        if (k & 1):
            bit_str += "1"
        else:
            bit_str += "0"
    bit_str = bit_str[::-1]
    return int(bit_str[bit_no])

#dround
def dround(value, sig_fig):
    sig_fig = round(sig_fig)
    if sig_fig < 1:   
        return 0
    elif sig_fig > 17:  
        return value
    if value == 0:
        return 0  
    # Calculate the order of magnitude (number of digits before decimal point)
    order = math.floor(math.log10(abs(value))) + 1
    # Calculate the rounding position in terms of significant digits
    rounding_position = sig_fig - order
    rounded_value = round(value, rounding_position)
    return rounded_value

#acs
def acs(value):
    return math.acos(value)

#asn
def asn(value):
    return math.asin(value)

#atn
def atn(value):
    return math.atan(value)

def bin_remove_space(string):
    string = string.strip()
    bin_str = ''
    for digit in string:
        if digit == " ":
            return bin_str
        bin_str += digit
    return bin_str

#bti
def bti(val_str, error_var = None):
    try:
        val_str = bin_remove_space(val_str)
        if len(val_str) > optionbit and val_str[0] == "0":
            val_str = val_str.lstrip("0")
        elif len(val_str) > optionbit and val_str[0] == '1':
            return "Integer overflow error"
        if len(val_str) < optionbit:
            _0s_added = "0" * (optionbit - len(val_str))
            val_str = _0s_added + val_str
        if val_str[0] == "0":
            return int(val_str, 2)
        elif val_str[0] == "1":
            return int(val_str[1:], 2) - int(math.pow(2, len(val_str) - 1))
    except Exception as e:
        if error_var is not None:
            error_var = str(e)  
        else:
            return e

#exp
def exp(value):
    return math.pow(math.e, value)

def hex_to_binary(string):
    hex_dict = {
    '0': '0000', '1': '0001', '2': '0010', '3': '0011',
    '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', 
    'a': '1010', 'A': '1010', 
    'b': '1011', 'B': '1011', 
    'c': '1100', 'C': '1100', 
    'd': '1101', 'D': '1101', 
    'e': '1110', 'E': '1110', 
    'f': '1111', 'F': '1111' }
    string = string.strip()
    bin_str = ''
    for digit in string:
        if digit == " ":
            return bin_str
        bin_str += hex_dict[digit]
    return bin_str

#hti
def hti(val_str, error_var = None):
    try:
        bin_str = hex_to_binary(val_str)
        if len(bin_str) > optionbit and bin_str[0] == "0":
            bin_str = bin_str.lstrip("0")
        elif len(bin_str) > optionbit and bin_str[0] == '1':
            return "Integer overflow error"
        if len(bin_str) < optionbit:
            _0s_added = "0" * (optionbit - len(bin_str))
            bin_str = _0s_added + bin_str
        if bin_str[0] == "0":
            return int(bin_str, 2)
        elif bin_str[0] == "1":
            return int(bin_str[1:], 2) - int(math.pow(2, len(bin_str) - 1))
    except Exception as e:
        if error_var is not None:
            error_var = str(e)  
        else:
            return e

#lgt
def lgt(val):
    if val > 0:
        return math.log10(val)
    else:
        return "error"

#mod
def mod(value, divisor):
    divisor = abs(divisor)
    return value - (int(value/divisor) * divisor)

#num
def num(string):
    return ord(string[0])

def oct_to_binary(string):
    oct_dict = {
    '0': '000', '1': '001', '2': '010', '3': '011',
    '4': '100', '5': '101', '6': '110', '7': '111'}
    string = string.strip()
    bin_str = ''
    for digit in string:
        if digit == " ":
            return bin_str
        bin_str += oct_dict[digit]
    return bin_str

#oti
def oti(val_str, error_var = None):
    try:
        bin_str = oct_to_binary(val_str)
        if len(bin_str) > optionbit and bin_str[0] == "0":
            bin_str = bin_str.lstrip("0")
        elif len(bin_str) > optionbit and bin_str[0] == '1':
            return "Integer overflow error"
        if len(bin_str) < optionbit:
            _0s_added = "0" * (optionbit - len(bin_str))
            bin_str = _0s_added + bin_str
        if bin_str[0] == "0":
            return int(bin_str, 2)
        elif bin_str[0] == "1":
            return int(bin_str[1:], 2) - int(math.pow(2, len(bin_str) - 1))
    except Exception as e:
        if error_var is not None:
            error_var = str(e)  
        else:
            return e

#pi
def pi():
    return math.pi

#pos
def pos(str1, str2):
    return str1.find(str2) + 1

#randomize
def randomize(seed):
    random.seed(seed)

#rnd
def rnd():      #check with backend impl
    return random.random()

#sgn
def sgn(val):
    if val > 0:
        return 1
    elif val < 0:
        return -1
    else:
        return 0

#sin
def sin(val):
    return math.sin(val)

#sqr
def sqr(val):
    if val >= 0:
        return math.sqrt(val)
    else:
        return "error"

#tan
def tan(val):
    return math.tan(val)

#cos
def cos(val):
    return math.cos(val)

def val(num_str, error_var = None):
    try:
        if "." in num_str:
            return float(num_str)
        else:
            return 0
    except Exception as e:
        if error_var is not None:
            error_var = str(e)  
        else:
            return e

#floor
def bt_int(val):            #Python has a built in int() function that converts strings or floats to whole numbers
    return math.floor(val)

#shift
def shift(val, shift_val):
    if shift_val > 0:
        return val >> shift_val
    elif shift_val < 0:
        return val << -shift_val
    else:
        return val

#div
def div(val1, val2):
    return int(val1/val2)

#and
def bt_and(val1, val2):            #Python and operator return True or False (not 1 or 0)
    if val1 != 0 and val2 != 0:
        return 1
    if val1 == 0 or val2 == 0:
        return 0
    
#not
def bt_not(val):         #Python not operator return True or False (not 1 or 0)
    if val == 0:
        return 1
    if val!= 0:
        return 0

#or
def bt_or(val1, val2):            #Python or operator return True or False (not 1 or 0)
    if val1 != 0 or val2 != 0:
        return 1
    if val1 == 0 and val2 == 0:
        return 0
    
#Reserved Variables
#btgetenv$
def btgetenv_dollar(command=None, rest_of_pathname=None):
    env_val = os.getenv("I3070_ICT_ROOT")
    if env_val is None:
        return "Environment variable I3070_ICT_ROOT is not set."
    if command is None and rest_of_pathname is None:
        return env_val
    if command and rest_of_pathname:
        full_path = f"{env_val}{rest_of_pathname}"
        if command in globals() and callable(globals()[command]) and os.path.exists(full_path):
            globals()[command](full_path)
            return f"{command} command executed with path {full_path}"
        else:
            return f"Error: Command '{command}' is not recognized or not callable."
        
#buffer$
input_buffer = ""
def input_to_buffer():
    global input_buffer
    input_buffer = input() 

def buffer_dollar():
    return input_buffer

#chr$
def chr_dollar(val):
    val = round(val)
    if val > 256:
        val = mod(val, 256)
    if val < 0:
        val += 256
    return chr(val)

#datetime$
def datetime_dollar():
    return time.strftime("%y%m%d%H%M%S")

#itb$
def itb_dollar(val):
    val = round(val)
    val_pos = abs(val)
    bin_str = format(val_pos, 'b')
    if len(bin_str) > optionbit:
        return "Conversion error"
    elif val > 0:
        return bin_str
    elif val < 0:
        bin_str = bin_str.zfill(optionbit)
        inverted_bits = ''.join('1' if bit == '0' else '0' for bit in bin_str)
        inverted_int = int(inverted_bits, 2)
        twos_complement_int = inverted_int + 1
        twos_complement_bin = bin(twos_complement_int)[2:].zfill(optionbit)
        return twos_complement_bin
    return "0"

#ith$
def ith_dollar(val):
    val = round(val)
    val_pos = abs(val)
    hex_str = '{0:X}'.format(val_pos)
    if len(hex_str) * 4 > optionbit:
        return "Value contains the null string"
    elif val > 0:
        return hex_str
    elif val < 0:
        int_val = int(hex_str, 16)
        bin_str = bin(int_val)[2:].zfill(optionbit)
        inverted_bits = ''.join('1' if bit == '0' else '0' for bit in bin_str)
        inverted_int = int(inverted_bits, 2)
        twos_complement_int = inverted_int + 1
        twos_complement_hex = hex(twos_complement_int)[2:].upper().zfill(optionbit // 4)
        return twos_complement_hex
    return "0"
    
#ito$
def ito_dollar(val):
    val = round(val)
    val_pos = abs(val)
    oct_str = '{0:o}'.format(val_pos)
    if len(oct_str) > ((optionbit + 2) // 3):
        return "Value contains the null string"
    elif val > 0:
        return oct_str
    elif val < 0:
        int_val = int(oct_str, 8)
        bin_str = bin(int_val)[2:].zfill(optionbit)
        inverted_bits = ''.join('1' if bit == '0' else '0' for bit in bin_str)
        inverted_int = int(inverted_bits, 2)
        twos_complement_int = inverted_int + 1
        twos_complement_octal = oct(twos_complement_int)[2:].zfill((optionbit + 2) // 3)
        return twos_complement_octal
    return "0"

#lwc$
def lwc_dollar(string):
    return string.lower()

def revision_dollar():
    try:
        version_info = subprocess.check_output(['ksh', '-c', 'version'], text=True)
        return version_info.strip()
    except FileNotFoundError:
        return "KornShell (ksh) is not installed."
    except subprocess.CalledProcessError:
        return "Unable to retrieve version information from KornShell."

#time$
def time_dollar():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%a %b %d, %Y %I:%M %p")
    formatted_time = formatted_time.ljust(26)[:26]
    return formatted_time

#trim$
def trim_dollar(string):
    string = string.strip()
    return string

#triml$
def triml_dollar(string):
    string = string.lstrip()
    return string

#trimr$
def trimr_dollar(string):
    string = string.rstrip()
    return string

#upc$
def upc_dollar(string):
    return string.upper()

#val$
def val_dollar(num):
    result = str(num)
    if num >= 0:
        result = result.lstrip()
    return result

#msec
def msec():
    return int(time.time() * 1000)

#errl
most_recent_error_line = 0
def set_error_line():
    global most_recent_error_line
    tb = traceback.extract_tb(traceback.sys.exc_info()[2])
    most_recent_error_line = tb[-1].lineno

def errl():
    return most_recent_error_line