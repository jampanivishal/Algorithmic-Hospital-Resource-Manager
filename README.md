# 🏥 Hospital Bed Allocation & Patient Record System
> **Track 2: Core Software Engineering, OOP & Real-World Data Structures and Algorithms**  
> **CSM (Computer Science & Medical Engineering) Capstone Project**

---

## 🌟 Executive Summary

In emergency medicine, every millisecond counts. Inefficient patient scheduling and linear searches can lead to catastrophic delays. The **Hospital Bed Allocation & Patient Record System** replaces naive linear storage with rigorous **Data Structures and Algorithms (DSA)** to model the real-world operational logic of a hospital emergency room:

1. **Emergency Triage Queue (`Max-Heap Priority Queue`)**: Patients are assigned an Emergency Severity Index (ESI) score from $1$ (*Mild*) to $5$ (*Critical*). A Max-Heap ensures that a Level 5 patient (e.g., cardiac arrest) automatically bypasses Level 1 patients and jumps directly to the front of the line for bed allocation.
2. **Instant Patient Record Lookup (`Hash Map / Hash Table`)**: Records are indexed by a unique `patient_id`. Instead of linear $O(N)$ scanning across thousands of historical records, the system achieves **$O(1)$ average time complexity** for instant patient history retrieval.
3. **Clinical Bed Inventory & Ward Matching**: A structured inventory of physical beds categorized across specialized wards (**ICU**, **Emergency**, **General Ward**, and **Pediatric Ward**) that dynamically maps triage urgency and patient demographics (e.g., pediatric care for ages $< 18$) to the optimal bed.
4. **Relational Storage Layer (`SQLite`)**: Complete state persistence, transactional integrity (ACID), and historical audit logging across application restarts.

---

## 🏗️ Architecture Blueprint & Data Structures

```
                      +---------------------------------------+
                      |       Patient Arrives at ER           |
                      |  (Name, Age, Ailment, Severity 1-5)   |
                      +-------------------+-------------------+
                                          |
                        +-----------------+-----------------+
                        |                                   |
                        v                                   v
             [ Hash Map Indexing ]                [ Priority Queue Heap ]
             dict[patient_id, Patient]            heapq: (-severity, arrival, pt)
             Complexity: O(1)                     Complexity: O(log N)
                        |                                   |
                        |                        Highest Urgency Dequeued
                        |                        (Level 5 jumps to front)
                        |                                   |
                        |                                   v
                        |                         [ Clinical Ward Matcher ]
                        |                         ICU / ER / General / Ped
                        |                                   |
                        +-----------------+-----------------+
                                          |
                                          v
                              [ Bed Allocation & SQLite ]
                              - Bed marked OCCUPIED
                              - Patient marked ADMITTED
                              - Audit Log Recorded
```

### Time & Space Complexity Analysis

| Operation | Data Structure Used | Time Complexity | Space Complexity | Real-World Medical Justification |
| :--- | :--- | :--- | :--- | :--- |
| **Triage Enqueue** | Binary Max-Heap (`heapq`) | $\mathcal{O}(\log N)$ | $\mathcal{O}(1)$ | Rapidly inserts incoming patients into the correct priority bracket. |
| **Triage Dequeue (Next Patient)** | Binary Max-Heap (`heapq`) | $\mathcal{O}(\log N)$ | $\mathcal{O}(1)$ | Sifts the root out and reheapifies, always serving the most critical patient next. |
| **Inspect Top Patient (Peek)** | Binary Max-Heap Root | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Instant triage assessment of who needs the next bed without removing them. |
| **Patient Record Lookup** | Hash Table (`dict`) | $\mathcal{O}(1)$ (avg) | $\mathcal{O}(1)$ | Immediate retrieval of medical history during emergency intake. |
| **Bed Status Lookup / Vacate** | Array / Hash Map | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Real-time bed availability check and instant discharge turnaround. |
| **FIFO Tie-Breaking** | Monotonic Counter Tuple | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Guarantees ethical medical fairness if two patients share the same severity. |

---

## 📂 Project Structure

```
hospital_bed_system/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── patient.py          # Patient entity, TriageSeverity (1-5), PatientStatus
│   │   └── bed.py              # Bed entity, WardType (ICU, ER, General, Pediatric)
│   ├── dsa/
│   │   ├── __init__.py
│   │   ├── priority_queue.py   # Max-Heap Triage Priority Queue with FIFO tie-breaker
│   │   └── patient_registry.py # Hash Map O(1) patient index & name query engine
│   ├── database/
│   │   ├── __init__.py
│   │   └── db_manager.py       # SQLite connection, migrations, WAL mode, audit logs
│   ├── services/
│   │   ├── __init__.py
│   │   └── hospital_system.py  # Central controller orchestrating DSA, beds & DB
│   └── cli/
│       ├── __init__.py
│       └── menu.py             # Interactive colored console interface & dashboards
├── tests/
│   ├── __init__.py
│   ├── test_models.py          # Domain model validation & encapsulation tests
│   ├── test_dsa.py             # Rigorous heap priority & hash map tests
│   ├── test_bed_allocation.py  # Ward matching, bed assignment & discharge tests
│   └── test_database.py        # Persistence across system restarts & audit trail
├── demo_simulation.py          # Automated non-interactive ER rush demonstration
├── main.py                     # Interactive CLI entry point
└── README.md                   # Full documentation & interview prep guide
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+ (Built entirely with standard library: **zero third-party dependencies required**).

### 1. Run the Automated Live Simulation
To see the system run an automated emergency rush scenario demonstrating heap reordering, ward matching, microsecond lookups, and bed recycling:
```bash
python demo_simulation.py
```

### 2. Run the Interactive Terminal Application
To interact with the system via a fully featured console menu:
```bash
python main.py
```

### 3. Run the Unit Test Suite
Run the 18 comprehensive unit tests:
```bash
python -m unittest discover -s tests -v
```

---

## 🎯 Technical Interview Preparation (For 3rd Year Placements)

When interviewers at top software and healthcare technology firms ask about this project, be prepared to discuss these core technical decisions:

### Q1: Why use a Priority Queue (Heap) instead of a simple sorted Array or Linked List for triage?
> **Answer**:
> - With an **unsorted array/list**: Insertion is $O(1)$, but finding the highest priority patient takes **$O(N)$**, which is unacceptably slow during emergencies.
> - With a **sorted array**: Finding the highest priority patient is $O(1)$, but inserting an incoming patient requires **$O(N)$** due to element shifting.
> - With a **Binary Heap (Priority Queue)**: Both insertion and extraction run in logarithmic time: **$\mathcal{O}(\log N)$**, with peek in **$\mathcal{O}(1)$**. In an emergency room with hundreds of patients, $\log_2(1000) \approx 10$ operations compared to $1000$ operations in linear time.

### Q2: Python's `heapq` is a Min-Heap by default. How did you implement a Max-Heap with FIFO tie-breaking?
> **Answer**:
> - We negated the severity value: `priority_key = -patient.severity.value`. In a min-heap, $-5$ evaluates before $-1$, effectively turning it into a Max-Heap.
> - To solve **FIFO tie-breaking** (if two patients have severity 5, the one who arrived first must be treated first), we pushed an internal 3-tuple:
>   $$\text{tuple} = (-\text{severity}, \text{arrival\_counter}, \text{patient})$$
> - If severities are identical, Python compares the second element `arrival_counter` (strictly ascending integer), ensuring deterministic first-come, first-served treatment without ever needing custom comparator errors on Patient objects.

### Q3: Why maintain an in-memory Hash Map if SQLite already has an index on `patient_id`?
> **Answer**:
> - In high-throughput clinical monitoring, disk I/O (even with SSDs and SQLite B-Trees) introduces millisecond-level system calls and disk lock overhead.
> - An in-memory Hash Map delivers **sub-microsecond memory lookups ($\mathcal{O}(1)$)**.
> - We adopt the **Cache-Aside / Dual-Layer Pattern**: The Hash Map serves real-time reads and writes in memory, while SQLite provides durable write-through persistence and disaster recovery.

---

## 💼 What to Highlight on Your Resume

When adding this project to your resume, use these high-impact bullet points:

- **"Architected a Hospital Bed Allocation & Triage System utilizing an optimized Binary Max-Heap Priority Queue, reducing emergency bed assignment latency to $\mathcal{O}(\log N)$ complexity."**
- **"Engineered an $\mathcal{O}(1)$ patient record lookup engine via an in-memory Hash Map synchronized with an ACID-compliant SQLite relational persistence layer."**
- **"Formulated a clinical ward-matching algorithm (ICU, Emergency, General, Pediatric) automating bed recycling and bed occupancy tracking across multi-ward hospital facilities."**
- **"Developed 18 comprehensive automated unit tests covering domain encapsulation, heap reordering, and restart state recovery."**
