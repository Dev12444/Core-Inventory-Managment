def generate_reference(warehouse_code, op_type, seq):

    return f"{warehouse_code}/{op_type}/{str(seq).zfill(3)}"