# Jerrin Shirks

# native imports
import struct


def isNotDict(value) -> bool:
    """Returns True if the input value is not a dictionary, False otherwise."""
    return not isinstance(value, dict)


def isDict(value) -> bool:
    """Returns True if the input value is a dictionary, False otherwise."""
    return isinstance(value, dict)


def isNotList(value) -> bool:
    """Returns True if the input value is not a list, False otherwise."""
    return not isinstance(value, list)


def isList(value) -> bool:
    """Returns True if the input value is a list, False otherwise."""
    return isinstance(value, list)


def readInt(f):
    """Returns an integer read from the file 'f'."""
    return struct.unpack('>i', f.read(4))[0]


def readShort(f):
    """Returns a short read from the file 'f'."""
    return struct.unpack('>h', f.read(2))[0]


def readByte(f):
    """Returns a byte read from the file 'f'."""
    return struct.unpack('>b', f.read(1))[0]


def readString(f):
    """Returns a string read from the file 'f'."""
    len_key = readShort(f)
    return f.read(len_key).decode()


def writeInt(f, value):
    """Writes an integer 'value' to the file 'f'."""
    f.write(struct.pack('>i', value))


def writeShort(f, value):
    """Writes a short 'value' to the file 'f'."""
    f.write(struct.pack('>h', value))


def writeByte(f, value):
    """Writes a byte 'value' to the file 'f'."""
    f.write(struct.pack('>b', value))


def writeString(f, string):
    """Writes a string 'string' to the file 'f'."""
    writeShort(f, len(string))
    f.write(string.encode())
