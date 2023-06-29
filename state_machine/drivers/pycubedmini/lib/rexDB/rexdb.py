import time
from src.dense_packer import DensePacker
from src.file_manager import FileManager

VERSION = "0.0.1"
VERSION_BYTE = 0x00

UNSIGNED_CHAR = 'B'
UNSIGNED_LONG_LONG = 'Q'
FLOAT = 'f'


class RexDB:
    def __init__(self, fstring, field_names: tuple, bytes_per_file=1024,
                 files_per_folder=50, time_method=time.gmtime):
        # add "i" as time will not be input by caller
        self._packer = DensePacker("i" + fstring)
        self._field_names = ("timestamp", *field_names)
        self._cursor = 0
        self._timer_function = time_method
        self._init_time = self._timer_function()
        self._prev_timestamp = time.mktime(self._init_time)
        self._timestamp = 0
        self._file_manager = FileManager(
            "i" + fstring, self._field_names, bytes_per_file, files_per_folder)
        self._file_manager.start_db_entry(self._prev_timestamp)
        self._file_manager.start_folder_entry(self._prev_timestamp)

    def log(self, data) -> bool:
        """
        log: bytes -> bool
        logs the data given into the correct folder and file. Also handles when new
        folders and files need to be created. Returns True if the data was
        successfully logged, False otherwise.
        """
        self._timestamp = (int)(time.mktime(self._timer_function()))

        if (self._timestamp < self._prev_timestamp):
            raise ValueError("logging backwards in time")

        if self._cursor >= self._file_manager.lines_per_file:
            self._file_manager.write_to_folder_map(self._timestamp)
            if self._file_manager.files >= self._file_manager.files_per_folder:
                # if no more files can be written in a folder, make new folder
                self._file_manager.write_to_db_map(self._timestamp)
                self._file_manager.create_new_folder()
                self._file_manager.start_db_entry(self._timestamp)
            # if no more lines can be written in a file, make new file
            self._file_manager.create_new_file()
            self._file_manager.start_folder_entry(self._timestamp)
            self._cursor = 0

        data_bytes = self._packer.pack((self._timestamp, *data))
        success = self._file_manager.write_file(data_bytes)
        self._cursor += 1
        self._prev_timestamp = self._timestamp
        return success

    @staticmethod
    def int_cmp(x, y):
        return (x > y) - (x < y)

    def nth(self, n):
        with open(self._file_manager.current_file, "rb") as fd:
            fd.seek(n*self._packer.line_size)
            line = fd.read(self._packer.line_size)
            return self._packer.unpack(line)[1:]

    def col(self, i):
        data = []
        with open(self._file_manager.current_file, "rb") as fd:
            fd.seek(0)
            for _ in range(self._packer.line_size):
                line = fd.read(self._packer.line_size)
                print(line)
                if len(line) != self._packer.line_size:
                    break
                line = self._packer.unpack(line)
                data.append(line[i])
        return data[self._cursor:] + data[:self._cursor]

    def get_data_at_time(self, t: time.struct_time):
        """
        struct_time -> tuple
        Given a time struct that was used to log in the database, this will return the first entry
        logged at that time.

        The precision of this function goes only to the nearest second because of the restrictions
        of struct_time
        """
        tfloat = time.mktime(t)
        filepath = self._file_manager.location_from_time(tfloat)
        if tfloat < time.mktime(self._init_time):
            raise ValueError("time is before database init time")
        try:
            with open(filepath, "rb") as fd:
                for _ in range(self._file_manager.lines_per_file):
                    raw_data = fd.read(self._packer.line_size)
                    data = self._packer.unpack(raw_data)
                    if (data[0] == tfloat):
                        return data
        except Exception as e:
            print(f"could not find data: {e}")
        return None

    def get_data_at_range(self, start_time: time.struct_time, end_time: time.struct_time):
        """
        (struct_time * struct_time) -> tuple
        Given a range of time, first argument of start time, second argument of end time
        this function will return all database entries falling within that range

        the struct_time datatype only holds precision of the nearest second, so this
        database only has precision to the nearest second as well.
        """
        start = time.mktime(start_time)
        end = time.mktime(end_time)
        filepaths = self._file_manager.locations_from_range(start, end)
        entries = []
        for filepath in filepaths:
            try:
                with open(filepath, "rb") as file:
                    for _ in range(self._file_manager.lines_per_file):
                        raw_data = file.read(self._packer.line_size)
                        data = self._packer.unpack(raw_data)
                        if (start <= data[0] and data[0] <= end):
                            entries.append(data)
            except Exception as e:
                print(f"could not search file: {e}")

        return entries

    def get_data_at_field_threshold(self,
                                    field: str,
                                    threshold,
                                    goal,
                                    cmp_fn=int_cmp,
                                    start_time=None,
                                    end_time=None):
        """
        string * 'a * int set * ('a * 'a -> ORDER) * struct_time * struct_time -> list

        field
        - str
        - is a string and is the name of the field you want to query on.

        Threshold:
        - 'a
        - is the value that you want to compare the data to

        goal:
        - any subset of {-1, 0, 1}
        - The integers used in this set should be -1, 0, 1.
        - -1 corresponds to less than, 0 corresponds to equal to, 1 corresponds to
          greater that. put in your set each operation you would like to include.

        cmp_fn:
        - 'a * 'a -> (some x in the set {-1, 0, 1})
        - is an optional field. It is the comparison function you are using
          to compare your threshold with the data stored in the database. The default
          is an integer comparison function.

        the start_time and end_time fields are optional fields to limit your search
        to a specific time range.

        The complexity of this function if O(n). This function does not benefit from
        the speed increase that the map files provide.
        """

        entries = []
        filepaths = []
        # get files to search
        if start_time and end_time:
            # If start and end times were specified only search files that fall within that range.
            start = time.mktime(start_time)
            end = time.mktime(end_time)
        elif start_time:
            # if only start time specified search from start time to now
            start = time.mktime(start_time)
            end = time.mktime(self._timer_function())
        else:
            # if neither are specified search from the database's start to now
            start = time.mktime(self._init_time)
            end = time.mktime(self._timer_function())

        filepaths = self._file_manager.locations_from_range(start, end)
        # get the correct field index for comparison
        for i, f in enumerate(self._field_names):
            if field.lower() == f.lower():
                field_index = i

        # access every file
        for filepath in filepaths:
            try:
                with open(filepath, "rb") as file:
                    for _ in range(self._file_manager.lines_per_file):
                        raw_data = file.read(self._packer.line_size)
                        data = self._packer.unpack(raw_data)
                        # compare entry and threshold and see if they match the goal
                        if (cmp_fn(data[field_index], threshold) in goal):
                            entries.append(data)
            except Exception as e:
                print(f"could not search file: {e}")

        return entries
