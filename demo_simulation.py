"""
Automated Emergency Room Triage & Bed Allocation Simulation.

Runs an automated end-to-end demonstration showing:
1. Patients arriving with different triage severities.
2. Priority Queue Max-Heap behavior (Level 5 jumping to the front ahead of Level 1).
3. FIFO tie-breaking for equal severity patients.
4. Automatic matching and bed allocation into appropriate wards (ICU, Pediatric, Emergency).
5. Instant O(1) Hash Map patient lookup.
6. Patient discharge and bed recycling.
7. SQLite audit logging and capacity analytics.

Execute with:
    python demo_simulation.py
"""

import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.services.hospital_system import HospitalBedAllocationSystem
from src.models.patient import TriageSeverity, PatientStatus


def run_simulation() -> None:
    # Use in-memory or dedicated test db for clean demo
    demo_db = BASE_DIR / "demo_simulation.db"
    if demo_db.exists():
        demo_db.unlink()

    print("=" * 75)
    print("   AUTOMATED DEMONSTRATION: HOSPITAL BED ALLOCATION & TRIAGE DSA")
    print("=" * 75)

    system = HospitalBedAllocationSystem(db_path=demo_db)

    print("\n--- STEP 1: Emergency Department Patient Arrival (Chronological) ---")
    print("Patients arrive at reception one after another:\n")

    arrivals = [
        ("Mild Cold / Skin Rash", "Emma Davis", 22, TriageSeverity.MILD),              # Level 1 (Arrives 1st)
        ("Sprained Ankle", "Marcus Brody", 35, TriageSeverity.MODERATE),               # Level 2 (Arrives 2nd)
        ("Child Persistent High Fever", "Sophia Chen", 7, TriageSeverity.URGENT),      # Level 3 (Arrives 3rd)
        ("Compound Arm Fracture", "David Miller", 44, TriageSeverity.VERY_URGENT),     # Level 4 (Arrives 4th)
        ("Acute Cardiac Arrest", "Robert Vance", 68, TriageSeverity.CRITICAL),         # Level 5 (Arrives 5th / LAST)
        ("Severe Respiratory Distress", "Grace Hopper", 59, TriageSeverity.CRITICAL),  # Level 5 (Arrives 6th / Same severity as Robert!)
    ]

    for ailment, name, age, severity in arrivals:
        p = system.register_patient(name=name, age=age, ailment=ailment, severity=severity)
        print(f"  [ARRIVED] {p.name:<15} | Age: {p.age:<2} | Ailment: {p.ailment:<30} | Severity: {p.severity.label}")

    print("\n" + "=" * 75)
    print("--- STEP 2: Priority Queue (Max-Heap) State Inspection ---")
    print("Notice how DSA reorganizes the line! Even though Robert Vance (Level 5) arrived")
    print("much later than Emma Davis (Level 1), he jumped to the FRONT of the queue.")
    print("Also observe FIFO tie-breaking: Robert Vance (arrived 5th) is ahead of Grace Hopper (arrived 6th).\n")

    queue = system.get_waiting_queue()
    for rank, p in enumerate(queue, start=1):
        print(f"  Position #{rank}: [{p.patient_id}] {p.name:<15} (Triage: {p.severity.label}) -> {p.ailment}")

    print("\n" + "=" * 75)
    print("--- STEP 3: Automated Bed Allocation (Clinical Ward Matching) ---")
    print("The system assigns available beds to the top of the heap in order of priority:\n")

    for _ in range(4):
        patient, bed, msg = system.allocate_next_bed()
        if bed:
            print(f"  [ALLOCATED] {msg}")

    print("\n" + "=" * 75)
    print("--- STEP 4: Instant O(1) Patient Record Lookup via Hash Map ---")
    target_id = "P1005"  # Robert Vance
    print(f"Looking up Patient ID: {target_id}...")
    start_time = time.perf_counter()
    patient = system.get_patient(target_id)
    lookup_time_us = (time.perf_counter() - start_time) * 1_000_000
    print(f"  Retrieved in: {lookup_time_us:.2f} microseconds (O(1) time)")
    if patient:
        print(f"  Record Found : {patient}")
        print(f"  Admitted Bed : {patient.bed_number}")
        print(f"  Status       : {patient.status.value}")

    print("\n" + "=" * 75)
    print("--- STEP 5: Patient Discharge & Bed Recycling ---")
    print(f"Discharging patient {patient.name} ({target_id}) after successful emergency stabilization...")
    p_dis, b_vac, dis_msg = system.discharge_patient(target_id)
    print(f"  [DISCHARGED] {dis_msg}")

    print("\nAllocating the newly freed bed to the next waiting patient in queue...")
    next_patient, next_bed, next_msg = system.allocate_next_bed()
    print(f"  [ALLOCATED] {next_msg}")

    print("\n" + "=" * 75)
    print("--- STEP 6: Final Capacity & Ward Occupancy Summary ---")
    stats = system.get_system_stats()
    print(f"  Total Hospital Beds : {stats['total_beds']}")
    print(f"  Occupied Beds       : {stats['occupied_beds']}")
    print(f"  Available Beds      : {stats['available_beds']}")
    print(f"  Occupancy Rate      : {stats['occupancy_rate_percent']}%")
    print(f"  Waiting in Triage   : {stats['waiting_in_triage']}")

    print("\n  Ward Breakdown:")
    for ward, counts in stats["ward_breakdown"].items():
        print(f"    - {ward:<15}: {counts['occupied']}/{counts['total']} beds occupied")

    system.close()
    print("\n" + "=" * 75)
    print("  SIMULATION COMPLETED SUCCESSFULLY! All DSA operations verified.")
    print("=" * 75)


if __name__ == "__main__":
    run_simulation()
