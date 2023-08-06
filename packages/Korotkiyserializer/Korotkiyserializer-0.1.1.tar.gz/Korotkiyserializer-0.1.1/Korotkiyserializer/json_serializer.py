from Korotkiyserializer.Korotkiyserializer.serialiser import serialize, deserialize
import regex


class json_serializer:
    INT_P = r"[+-]?\d+"
    FLOAT_P = fr"({INT_P}(?:\.\d+)?(?:e{INT_P})?)"
    BOOL_P = r"((true)|(false))\b"
    STR_P = r"\"((\\\")|[^\"])*\""
    NONE_P = r"\b(Null)\b"
    COMPLEX_P = fr"{FLOAT_P}{FLOAT_P}j"

    LIST_RECURSION = r"\[(?R)?(,(?R))*\]"
    DICT_RECURSION = r"\{((?R):(?R))?(?:,(?R):(?R))*\}"

    VALUE_P = fr"\s*({LIST_RECURSION}|{DICT_RECURSION}|{STR_P}|{FLOAT_P}|{BOOL_P}|{INT_P}|{NONE_P}|{COMPLEX_P}\s*)"

    def dumps(self, obj):
        obj = serialize(obj)
        return self.custom_to_string(obj)

    def dump(self, obj, file):
        file.write(self.dumps(obj))

    def custom_to_string(self, value):
        if isinstance(value, str):
            return '"' + \
                value.replace("\\", "\\\\"). \
                replace('"', "\""). \
                replace("'", "\'") + '"'

        elif isinstance(value, (int, float, complex)):
            return str(value)

        elif isinstance(value, bool):
            return "true" if value else "false"

        elif isinstance(value, list):
            return "[" + ", ".join([self.custom_to_string(val) for val in value]) + "]"

        if isinstance(value, dict):
            return "{" + ", ".join([f"{self.custom_to_string(k)}: \
                                    {self.custom_to_string(v)}" for k, v in value.items()]) + "}"

    def loads(self, string):
        obj = self.find_elem(string)
        return deserialize(obj)

    def load(self, file):
        return self.loads(file.read())

    def find_elem(self, string):
        string = string.strip()

        match = regex.fullmatch(self.INT_P, string)
        if match:
            return int(match.group(0))

        match = regex.fullmatch(self.STR_P, string)
        if match:
            res = match.group(0)
            res = res.replace("\\\\", "\\"). \
                replace(r"\"", '"'). \
                replace(r"\'", "'")
            return res[1:-1]

        match = regex.fullmatch(self.FLOAT_P, string)
        if match:
            return float(match.group(0))

        match = regex.fullmatch(self.BOOL_P, string)
        if match:
            return match.group(0) == "true"

        match = regex.fullmatch(self.NONE_P, string)
        if match:
            return None

        if string.startswith("[") and string.endswith("]"):
            string = string[1:-1]
            matches = regex.findall(self.VALUE_P, string)
            return [self.find_elem(match[0]) for match in matches]

        if string.startswith("{") and string.endswith("}"):
            string = string[1:-1]
            matches = regex.findall(self.VALUE_P, string)
            return {self.find_elem(matches[i][0]):
                    self.find_elem(matches[i + 1][0])
                    for i in range(0, len(matches), 2)}
