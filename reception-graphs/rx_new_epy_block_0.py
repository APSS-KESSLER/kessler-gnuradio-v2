import pmt
from gnuradio import gr

class pdu_second_byte_filter(gr.basic_block):
    """
    pass PDUs only if second byte == 0xFE
    """

    def __init__(self):
        gr.basic_block.__init__(
            self,
            name="pdu_second_byte_filter",
            in_sig=None,
            out_sig=None
        )

        # Message ports
        self.message_port_register_in(pmt.intern("in"))
        self.message_port_register_out(pmt.intern("out"))

        self.set_msg_handler(pmt.intern("in"), self.handle_msg)

    def handle_msg(self, msg):
        # Expect (metadata . u8vector)
        if not pmt.is_pair(msg):
            return

        meta = pmt.car(msg)
        data = pmt.cdr(msg)

        if not pmt.is_u8vector(data):
            return

        vec = pmt.u8vector_elements(data)

        # Need at least 2 bytes
        if len(vec) < 2:
            return

        # Check second byte
        if vec[1] == 0xFE:
            # Pass through unchanged
            return 
        else: 

            self.message_port_pub(
                pmt.intern("out"),
                pmt.cons(meta, data)
            )
        # else: drop silently