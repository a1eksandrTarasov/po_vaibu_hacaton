import json

EMV_TAGS = {
    "9F02": "Transaction Amount",
    "5F2A": "Transaction Currency Code",
    "9F15": "Merchant Category Code (MCC)",
    "9F4E": "Merchant Name",
    "9F1C": "Terminal ID"
}

def parse_emv(data):
    parsed_data = {}
    index = 0


    hex_data = data.strip().split()

    while index < len(hex_data):
        tag = hex_data[index]
        index += 1


        if int(tag, 16) & 0x1F == 0x1F:
            tag += hex_data[index]
            index += 1


        length = int(hex_data[index], 16)
        index += 1

        value = ''.join(hex_data[index:index + length])
        index += length

        parsed_data[EMV_TAGS.get(tag, tag)] = decode_value(tag, value)

    return parsed_data

def decode_value(tag, value):
    if tag == "9F02":
        return int(value) / 100
    elif tag == "5F2A":  # Валюта
        return "RUB" if value == "0643" else value
    elif tag == "9F15":  # MCC-код
        return f"MCC-{value}"
    elif tag == "9F4E":  # ASCII
        return bytes.fromhex(value).decode('ascii')
    elif tag == "9F1C":  # Terminal ID
        return value
    return value

emv_data = "80 A8 00 00 1F 9F02 06 000000010000 5F2A 02 0643 9F15 02 5814 9F4E 0F 504259204D41524B4554 9F1C 08 00112233"


parsed_data = parse_emv(emv_data)
json_output = json.dumps(parsed_data, indent=4, ensure_ascii=False)


with open("parsed_transaction.json", "w", encoding='utf-8') as file:
    file.write(json_output)

print(json_output)
