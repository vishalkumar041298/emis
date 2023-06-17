def remove_urn(id: str) -> str:
    if 'urn:uuid:' in id:
        return id.split(":")[-1]
