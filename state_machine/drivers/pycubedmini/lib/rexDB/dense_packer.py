import struct


class DensePacker():
    def __init__(self, fstring: str) -> None:
        self.fstring_length = len(fstring)
        if self.fstring_length <= 0:
            raise ValueError("fstring must contain at least one data type")
        self.user_fstring = fstring
        self.dense_fstring = self.make_format(fstring)
        self.user_dense_map = self.create_pack_maps(self.user_fstring, self.dense_fstring)
        self.line_size = struct.calcsize(self.dense_fstring)

    def create_pack_maps(self, user_fstring, dense_fstring) -> str:
        '''
        create_pack_map : str * str -> str * str
        Creates a map from the user_fstring to the dense_fstring.
        This maps the last occurence of the data type in user_fstring
        to the first occurence in dense_fstring.
        For Example icfc = [0, 1, 2, 3] -> ficc = [2, 0, 3, 1]
            Notice how the "c" at index 3 comes before the "c" at
            index 1
        '''
        pack_map = {"c": [], "?": [], "h": [], "i": [], "f": [], "Q": [], "d": []}
        length = len(user_fstring)
        # map from the user string to the dense string
        user_dense_map = [0] * length
        for i in range(length):
            pack_map[user_fstring[i]].append(i)
        for i in range(length):
            user_dense_map[i] = pack_map[dense_fstring[i]].pop()

        return user_dense_map

    def pack(self, data: tuple) -> bytes:
        '''
        pack: tuple -> bytes
        takes input in the user_format, converts it to data in dense_format
        and packs that data into bytes.
        '''
        result = [0] * self.fstring_length
        for i in range(self.fstring_length):
            index = self.user_dense_map[i]
            result[i] = data[index]
        return struct.pack(self.dense_fstring, *result)

    def unpack(self, data: bytes) -> tuple:
        '''
        unpack: bytes -> tuple
        takes input in the form of bytes and will unpack the data into a tuple
        that is in the user_format
        '''
        result = [0] * self.fstring_length
        unpacked_data = struct.unpack(self.dense_fstring, data)
        for i in range(self.fstring_length):
            index = self.user_dense_map[i]
            result[index] = unpacked_data[i]
        return tuple(result)

    @staticmethod
    def make_format(fstring: str) -> str:
        '''
        make_format: str -> str
        orders the incoming format string based on the byte size of
        the data type.
        icfc -> ficc
        '''
        char_list = {"c": 1, "?": 0.1, "h": 2, "i": 4, "f": 4.1, "d": 8, "Q": 8.1}
        denseFormat = list(fstring)
        try:
            denseFormat.sort(key=(lambda c: char_list[c]), reverse=True)
        except KeyError as e:
            raise ValueError(f"Invalid fstring contains unsupported data type: {e}")
        return ''.join(denseFormat)

    @staticmethod
    def calc_fstring_size(fstring) -> int:
        '''
        calc_fstring_size: None -> int
        calculates and returns the size in bytes for self.fstring
        '''
        char_list = {"c": 1, "?": 1, "h": 2, "i": 4, "f": 4, "Q": 8, "d": 8}
        sum = 0
        for char in fstring:
            sum += char_list[char]
        return sum
