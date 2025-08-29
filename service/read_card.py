from pirc522 import RFID

class RC522CardReader:
    def __init__(self, pin_rst=22):
        self.rdr = RFID(pin_rst=pin_rst)
        self.previous_read = None
        self.current_read = None
        
    def read(self) -> int:
        (error, tag_type) = self.rdr.request()
        if not error:
            (error, uid) = self.rdr.anticoll()
            if not error:
                return uid
        return None
    
    def read_with_debounce(self) -> int:
        self.current_read = self.read()
        if self.current_read is not None:
            if self.previous_read is None:
                self.previous_read = self.current_read
                return self.current_read
            else:
                self.previous_read = self.current_read
                return None
    def translate_uid(self, uid) -> str:
        str_uid = ""
        for i in uid:
            digit = str(hex(i))[2:]
            str_uid += digit
        return str_uid

    def cleanup(self):
        self.rdr.cleanup()