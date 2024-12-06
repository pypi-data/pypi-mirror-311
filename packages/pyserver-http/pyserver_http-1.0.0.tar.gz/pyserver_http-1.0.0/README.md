# pyserver: simple http server
## 🛠 Installation
1. Ensure Python 3.9 or newer is installed.
2. Install via pip:
```bash
pip install pyserver-http # pyserver was taken lmao
```
## 🚀 Usage
### Start the Server
Host the server from `~/.pyserver`:
```bash
python -m pyserver serve --host 0.0.0.0 --port 80
```
#### Options:
- `--host`: Host to bind the server (default: `0.0.0.0`).
- `--port`: Port to bind the server (default: `80`).
## 📂 File Structure
```plaintext
pyserver/
├── __main__.py       # Entry point for the application
├── server.py         # Server-side implementation
├── utils.py          # Utility functions (e.g., get local IP)
```
## 🌟 Example Workflow
Run the server on a machine with port 8080:
```bash
python -m pyserver serve --port 8080
```
Place the files to serve in the `~/.pyserver` directory.
## 🔧 Requirements

- Python 3.9 or newer.
- Both devices must be connected to the same local network.

## 🛡 Security Note
This tool is intended for local network use. Do not expose the server to the public internet without proper security measures.