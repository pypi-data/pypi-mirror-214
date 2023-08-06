from devvio_util.primitives.summary import Summary
from devvio_util.primitives.transaction import Transaction
from devvio_util.primitives.utils import InputBuffer
from devvio_util.primitives.validation import Validation
from devvio_util.primitives.chainstate import Chainstate


class FinalBlock:
    def __init__(self,
                 final_blk: InputBuffer or str = None,
                 prior: Chainstate = None,
                 keys=None,
                 is_legacy: bool = False,
                 do_validate: bool = False):
        self._canonical = None
        if isinstance(final_blk, str):
            # TODO: fetch attributes on request, clean up InputBuffer object on request
            self._canonical = InputBuffer(final_blk)
        self._shard_index = None
        self._block_height = None
        self._block_time = None
        self._prev_hash = None
        self._merkle = None
        self._summary = None
        self._tx_size = None
        self._sum_size = None
        self._val_count = None
        self._vals = None
        self._is_legacy = is_legacy
        self._txs = []

        if final_blk and isinstance(final_blk, InputBuffer):
            self.from_buffer(final_blk, prior, keys, is_legacy, do_validate)
        elif self._canonical:
            self.from_buffer(self._canonical, prior, keys, is_legacy, do_validate)
        else:
            raise Exception(f"Invalid FinalBlock input type {type(final_blk)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._canonical:
            self._canonical.__exit__()

    def get_indexes(self, buffer: InputBuffer):
        version_ = buffer.get_next_uint8()
        if not version_:
            raise Exception("Invalid FinalBlock: buffer empty!")

        if version_ > 1:
            raise Exception(f"Invalid FinalBlock: bad {version_}")

        num_bytes_ = buffer.get_next_uint64()
        if not num_bytes_:
            raise Exception("Invalid FinalBlock: wrong size!")

        if not self._is_legacy:
            self._shard_index = buffer.get_next_uint64()
            self._block_height = buffer.get_next_uint64()

        self._block_time = buffer.get_next_uint64()
        self._prev_hash = buffer.get_next_prev_hash()
        self._merkle = buffer.get_next_merkle()

        self._tx_size = buffer.get_next_uint64()
        self._sum_size = buffer.get_next_uint64()
        self._val_count = buffer.get_next_uint32()

    def from_buffer(self, buffer: InputBuffer, prior: Chainstate = None, keys=None,
                    is_legacy: bool = False, do_validate: bool = False):
        # Back to begin
        buffer.seek(0)
        self._is_legacy = is_legacy
        self.get_indexes(buffer)

        tx_start = buffer.tell()

        while buffer.tell() < tx_start + self._tx_size:
            one_tx = Transaction(buffer, self._is_legacy)
            self._txs.append(one_tx)

        # if (do_validate):
        #     summary = Summary()
        #     for tx in self._txs:
        #         tx.isValid(None, keys, summary)

        self._summary = Summary(buffer)
        if prior:
            prior.update(self._summary)
        self._vals = Validation(buffer)

    def __bool__(self):
        return self._block_height is not None

    def get_shard_index(self) -> int:
        return self._shard_index

    def get_block_height(self) -> int:
        return self._block_height

    def get_block_time(self) -> int:
        return self._block_time

    def get_tx_size(self) -> int:
        return self._tx_size

    def get_sum_size(self) -> int:
        return self._sum_size

    def get_val_count(self) -> int:
        return self._val_count

    def get_summary(self) -> Summary:
        return self._summary

    def get_txs(self) -> list:
        return self._txs
