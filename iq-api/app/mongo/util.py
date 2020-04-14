def modify_id_response(row):
    row["id"] = str(row.pop("_id"))
    return row
