def parse_walk_schedule(schedule_spec):
    if not isinstance(schedule_spec, str):
        return "Invalid schedule input"

    try:
        parts = schedule_spec.strip().split("-")

        if len(parts) != 3:
            return "Invalid schedule format"

        pets_str, mins_str, weekend_str = parts

        pets = int(pets_str)
        mins = int(mins_str)

        if pets <= 0 or mins <= 0:
            return "Pets and minutes must be positive"

        weekend_map = {"YES": 15.0, "NO": 0.0}
        weekend = weekend_str.strip().upper()

        if weekend not in weekend_map:
            return "Invalid weekend option"

        weekend_fee = weekend_map[weekend]
        base_fee = 20.0 if mins <= 30 else 35.0
        total = base_fee + (pets * 5.0) + weekend_fee

        return f"Walk: {pets} pets, {mins} mins - Total ${total:.2f}"

    except (ValueError, OverflowError):
        return "Invalid schedule input"


def compute_pace_per_pet(walk_metrics_str):
    if not isinstance(walk_metrics_str, str):
        return "Invalid pace input"

    try:
        parts = walk_metrics_str.strip().split("/")

        if len(parts) != 2:
            return "Invalid pace format"

        mins = float(parts[0])
        pets = float(parts[1])

        if not (0 < mins < float("inf")):
            return "Invalid minutes"

        if not (0 < pets < float("inf")):
            return "Invalid number of pets"

        pace = mins / pets

        if not (0 <= pace < float("inf")):
            return "Invalid pace result"

        return round(pace, 2)

    except (ValueError, ZeroDivisionError, OverflowError):
        return "Invalid pace input"


def lookup_temperament_surcharge(temperament_code):
    if not isinstance(temperament_code, str):
        return "Invalid temperament input"

    prefix = temperament_code.strip().upper()[:3]

    surcharges = {
        "CAL": 0.0,
        "PLY": 5.0,
        "REA": 12.0,
        "AGG": 20.0
    }

    return surcharges.get(prefix, "Invalid temperament code")


def main():
    print("==== Running parse_walk_schedule ====")
    s_input = input("Enter schedule (e.g. 2-30-YES): ")
    print(parse_walk_schedule(s_input))

    print("\n==== Running compute_pace_per_pet ====")
    p_input = input("Enter minutes/pets (e.g. 45/3): ")
    print("Pace (min/pet):", compute_pace_per_pet(p_input))

    print("\n==== Running lookup_temperament_surcharge ====")
    t_input = input(
        "Enter temperament code (e.g. CALM, PLAYFUL, AGGRESSIVE): "
    )
    print("Surcharge: $", lookup_temperament_surcharge(t_input))


if __name__ == "__main__":
    main()
