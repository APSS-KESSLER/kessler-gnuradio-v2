import pmt
from gnuradio import gr

class pdu_ax25_byte_prepender_filter(gr.basic_block):
    """
    pass PDUs only if second byte == 0xA2
    """

    def __init__(self):
        gr.basic_block.__init__(
            self,
            name="PDU Ax25 Prepender",
            in_sig=None,
            out_sig=None
        )

        # Message ports
        self.message_port_register_in(pmt.intern("in"))
        self.message_port_register_out(pmt.intern("out"))

        self.set_msg_handler(pmt.intern("in"), self.handle_msg)

    def handle_msg(self, msg):
        if not pmt.is_pair(msg):
            return

        meta = pmt.car(msg)
        data = pmt.cdr(msg)

        if not pmt.is_u8vector(data):
            return

        vec = pmt.u8vector_elements(data)

        if len(vec) < 2:
            return

        # DROP if second byte is 0xFE
        if vec[1] != 0xA2:
            return

        # PREPEND 0x00 safely
        new_vec = [0x00] + list(vec)

        new_pmt = pmt.init_u8vector(len(new_vec), new_vec)

        self.message_port_pub(
            pmt.intern("out"),
            pmt.cons(meta, new_pmt)
        )