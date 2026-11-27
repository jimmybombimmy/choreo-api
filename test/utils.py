def sort_by_id(entries):
    ordered_entries = []

    for u in sorted(entries, key=lambda item: item.id):
        ordered_entries.append(u)

    return ordered_entries
