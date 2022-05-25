def get_code(url: str):
    lines = url.split('%')
    for line in lines:
        if line.count('-') == 4:
            raw = line[4:] + '\n'
            if len(raw) == 30:
                return raw
            else:
                return raw.split('=')[1]
