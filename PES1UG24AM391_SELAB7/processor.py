def validate_blood_type(blood_code):
    if not isinstance(blood_code, str):
        return "Invalid blood code"
    cleaned = blood_code.strip().upper()
    if len(cleaned) < 2:
        return "Invalid blood code"
    antigen = cleaned[:-1]
    rh_char = cleaned[-1]
    valid_antigens = {"A", "B", "AB", "O"}
    rh_map = {"+": "Positive", "-": "Negative"}
    if antigen not in valid_antigens or rh_char not in rh_map:
        return "Invalid blood code"
    return f"{antigen} {rh_map[rh_char]}"

def calculate_pulse_pressure(bp_string):
    if not isinstance(bp_string, str):
        return "Invalid BP format"
    parts = bp_string.strip().split('/')
    if len(parts) != 2:
        return "Invalid BP format"
    try:
        systolic = int(parts[0].strip())
        diastolic = int(parts[1].strip())
    except (ValueError, TypeError):
        return "Invalid BP format"
    if diastolic <= 0 or systolic <= 0:
        return "Invalid BP values"
    pulse_diff = systolic - diastolic
    ratio = round(systolic / diastolic, 2)
    return f"Diff: {pulse_diff}, Ratio: {ratio}"

def parse_donor_registry(donor_entry):
    if not isinstance(donor_entry, str):
        return "Invalid donor record"
    fields = donor_entry.strip().split('|')
    if len(fields) < 3:
        return "Invalid donor record"
    donor_id = fields[0].strip()
    if not donor_id:
        return "Invalid donor record"
    try:
        weight = float(fields[1].strip())
        hemoglobin = float(fields[2].strip())
    except (ValueError, TypeError):
        return "Invalid donor record"
    if weight <= 0 or hemoglobin <= 0:
        return "Invalid donor measurements"
    eligible = weight >= 50.0 and hemoglobin >= 12.5
    return f"Donor {donor_id}: {'Eligible' if eligible else 'Deferred'}"

def main():
    print("==== Running validate_blood_type ====")
    b_input = input("Enter blood type (e.g. A+, O-, AB+): ")
    print("Validated:", validate_blood_type(b_input))
    print("\n==== Running calculate_pulse_pressure ====")
    bp_input = input("Enter BP (e.g. 120/80): ")
    print("BP Metrics:", calculate_pulse_pressure(bp_input))
    print("\n==== Running parse_donor_registry ====")
    d_input = input("Enter record (ID|Weight|Hemoglobin): ")
    print("Status:", parse_donor_registry(d_input))

if __name__ == "__main__":
    main()
