# looperoni

`looperoni` is a lightweight, zero-dependency CLI tool designed to process a text file line-by-line and execute a shell command using each line. It supports custom placeholder replacement and fixed or randomized execution delays (throttling).

---

## Features
- **Zero Dependencies:** Uses only Python standard libraries.
- **Memory Efficient:** Streams files line-by-line (can handle gigabyte-sized files without high memory usage).
- **Variable Placeholder Substitution:** Custom placeholder tags (`{var}`, `{url}`, etc.).
- **Dynamic Throttling:** Supports fixed delays (`1.5s`) or dynamic floating-point random ranges (`0.5s` to `3.0s`).
- **Real-Time Streaming:** Streams stdout and stderr directly to your console output in real time.

---

## Installation & Setup

To run `looperoni` directly as a standalone system command instead of `python3 looperoni.py`, follow the steps below for your operating system.

### Linux / macOS

1. **Make the file executable:**
   ```bash
   chmod +x looperoni.py

```

2. **Move it to a directory in your system `$PATH**` (renaming it to `looperoni`):
```bash
sudo mv looperoni.py /usr/local/bin/looperoni

```


3. **Verify installation:**
```bash
looperoni --help

```



---

### Windows

#### Option A: Using `pip install -e .` (Recommended with `pyproject.toml`)

If you add a standard `pyproject.toml` file in the same directory:

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "looperoni"
version = "1.0.0"
scripts = { looperoni = "looperoni:main" }

```

Then run:

```powershell
pip install -e .

```

#### Option B: Quick Manual Executable Path

1. Create a folder for your CLI tools (e.g., `C:\tools`).
2. Move `looperoni.py` to `C:\tools\looperoni.py`.
3. Create a file named `looperoni.bat` inside `C:\tools` with the following content:
```cmd
@echo off
python "C:\tools\looperoni.py" %*

```


4. Add `C:\tools` to your System Environment Variable **Path**.

---

## Command Usage

```bash
looperoni -f <file_path> -e <command_string> [options]

```

### Arguments & Options

| Flag | Long Flag | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `-f` | `--file` | **Yes** | — | Path to the input text file. |
| `-e` | `--exec` | **Yes** | — | Shell command string to execute per line. |
| `-d` | `--delay` | No | None | Delay in seconds between iterations: single float (e.g., `1.5`) or random range (e.g., `0.5,3.0`). |
| `-v` | `--var` | No | `var` | Variable placeholder string inside the command (`{var}`). |
| `-h` | `--help` | No | — | Display help menu and exit. |

---

## Examples

### 1. Basic Example (Ping list of hosts)

Given `hosts.txt`:

```
google.com
github.com
cloudflare.com

```

Run:

```bash
looperoni -f hosts.txt -e "ping -c 1 {var}"

```

---

### 2. Custom Variable Placeholder Tag

You can change the variable placeholder from `{var}` to anything else (e.g., `{ip}`) using `-v`:

```bash
looperoni -f ips.txt -v ip -e "nmap -p 80 {ip}"

```

---

### 3. Fixed Delay Throttling

Wait **2 seconds** after each command finishes before starting the next one:

```bash
looperoni -f urls.txt -e "curl -I {var}" -d 2

```

---

### 4. Randomized Interval Delay

Delay execution by a random floating-point duration between **0.5 seconds and 3.5 seconds** between iterations:

```bash
looperoni -f endpoints.txt -e "curl -s [https://api.example.com/](https://api.example.com/){var}" -d 0.5,3.5

```

---

## License
```
MIT License

```
