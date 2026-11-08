"""Encode and Decode Strings: from the worst idea to the best one.

Three ways to pack a list of strings into one string and get the exact list back, in the order the episode covers them.
Run this file to check all three: python3 solution.py
"""


def comma_encode(strs):
    """Join with commas. Breaks as soon as a string contains a comma."""
    return ",".join(strs)


def comma_decode(s):
    return s.split(",")


def escape_encode(strs):
    """Escape backslashes and commas inside each string, then join with commas. Works, but the decoder checks every character."""
    return ",".join(x.replace("\\", "\\\\").replace(",", "\\,") for x in strs)


def escape_decode(s):
    out, word, i = [], [], 0
    while i < len(s):
        if s[i] == "\\":                 # an escaped character: keep the next one as it is
            word.append(s[i + 1])
            i += 2
        elif s[i] == ",":                # a real separator
            out.append("".join(word))
            word = []
            i += 1
        else:
            word.append(s[i])
            i += 1
    out.append("".join(word))
    return out


def length_encode(strs):
    """Write each string's length and a '#' before it. O(n) time."""
    return "".join(f"{len(x)}#{x}" for x in strs)


def length_decode(s):
    """Read the number up to '#', then cut exactly that many characters. Never searches inside a string. O(n) time."""
    out, i = [], 0
    while i < len(s):
        j = s.index("#", i)              # the '#' only marks where the length stops
        n = int(s[i:j])
        out.append(s[j + 1:j + 1 + n])
        i = j + 1 + n                    # jump straight over the string
    return out


if __name__ == "__main__":
    example = ["hi", "a,b", "ok"]                         # the example from the video
    assert comma_decode(comma_encode(example)) == ["hi", "a", "b", "ok"]   # three strings come back as four
    assert length_encode(example) == "2#hi3#a,b2#ok"

    cases = [
        example,
        ["neet", "code", "love", "you"],
        [""],
        ["", ""],
        ["#", "12#", "a#b#c"],                            # a '#' inside a string can't break it
        ["back\\slash", "comma,", "\\,"],
        ["x" * 123, "long length"],                       # a length with more than one digit
    ]
    for enc, dec in ((escape_encode, escape_decode), (length_encode, length_decode)):
        for strs in cases:
            assert dec(enc(strs)) == strs, (enc.__name__, strs)
    print(f"Escaping and length prefixing pass all {len(cases)} cases. Commas alone fail on the example.")
