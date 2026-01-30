# High-Performance Python Log Parser 🚀

This repository demonstrates the evolution of a log parsing system from a basic memory-safe script to a fully distributed Producer-Consumer architecture.

**The Problem:** Parsing massive server logs (100GB+) efficiently.
**The Constraints:** 1. **Memory:** Cannot load the full file into RAM (avoid OOM errors).
2. **Speed:** Must utilize all CPU cores (bypass Python GIL).
3. **Stability:** Must prevent race conditions during file writes.

---

## 📂 Repository Contents

### 1. `logparser_forone_logfile.py` (Memory Optimized)
**Concept:** The Baseline.  
Uses Python **Generators (`yield`)** to stream the file line-by-line.
* **Pros:** Constant O(1) memory usage regardless of file size.
* **Cons:** Single-threaded. CPU bound. Slow for massive datasets.
* **Key Tech:** `yield`, `with open(..., buffering=...)`

### 2. `logparser_formutiplefiles_multiprocessing.py` (Speed Optimized)
**Concept:** The Scaler.  
Introduces `multiprocessing.Pool` to parallelize the Regex parsing across all available CPU cores.
* **Pros:** 10x-50x faster processing (depending on core count).
* **Cons:** High I/O contention. Multiple workers trying to write to the same file or standard output can cause blocking or jumbled text.
* **Key Tech:** `multiprocessing.Pool`, `starmap`, `cpu_count()`

### 3. `logparser_forhugemutiplefiles_multiprocessing.py` (Architecture Optimized - *Best Practice*)
**Concept:** The Enterprise Solution.  
Implements the **Producer-Consumer Pattern** using a shared `Manager().Queue()`.
* **Architecture:**
    * **Producers (Workers):** Parse logs in parallel and push results to a Queue. They never touch the disk.
    * **Consumer (Listener):** A dedicated process that pulls from the Queue and writes to the disk.
* **Pros:** Thread-safe, non-blocking I/O, graceful shutdown. Decouples "Compute" (Workers) from "I/O" (Listener).
* **Key Tech:** `multiprocessing.Manager`, `Queue`, `Process`, `pool.starmap`

---

## 📊 Performance Comparison (Hypothetical)

| Script | 10GB File Time | Memory Usage | CPU Usage |
| :--- | :--- | :--- | :--- |
| `log_parser_basic.py` | 45 mins | 50 MB | 1 Core (100%) |
| `log_parser_multiprocessing.py` | 4 mins | 800 MB | All Cores (100%) |
| **`log_parser_queue.py`** | **4.2 mins** | **200 MB** | **All Cores + 1 I/O Proc** |

*Note: The Queue approach is slightly slower than raw multiprocessing due to IPC overhead, but significantly more stable and safe for production.*

---

## 🛠️ Setup & Usage

### Prerequisites
* Python 3.8+
* A large log file (e.g., `server.log`)

### Running the Solutions

**1. Basic Generator**
```bash
python logparser_forone_logfile.py
python logparser_formutiplefiles_multiprocessing.py
python logparser_forhugemutiplefiles_multiprocessing.py
