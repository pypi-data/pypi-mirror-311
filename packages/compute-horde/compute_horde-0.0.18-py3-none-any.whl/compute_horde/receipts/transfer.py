import contextlib
import csv
import io
import logging
import shutil
import tempfile

import pydantic
import requests

from compute_horde.executor_class import ExecutorClass
from compute_horde.receipts.schemas import (
    JobAcceptedReceiptPayload,
    JobFinishedReceiptPayload,
    JobStartedReceiptPayload,
    Receipt,
    ReceiptPayload,
    ReceiptType,
)

logger = logging.getLogger(__name__)


class ReceiptFetchError(Exception):
    pass


def get_miner_receipts(hotkey: str, ip: str, port: int) -> list[Receipt]:
    """Get receipts from a given miner"""
    with contextlib.ExitStack() as exit_stack:
        try:
            receipts_url = f"http://{ip}:{port}/receipts/receipts.csv"
            response = exit_stack.enter_context(requests.get(receipts_url, stream=True, timeout=5))
            response.raise_for_status()
        except requests.RequestException as e:
            raise ReceiptFetchError("failed to get receipts from miner") from e

        temp_file = exit_stack.enter_context(tempfile.TemporaryFile())
        shutil.copyfileobj(response.raw, temp_file)
        temp_file.seek(0)

        receipts = []
        wrapper = io.TextIOWrapper(temp_file)
        csv_reader = csv.DictReader(wrapper)
        for raw_receipt in csv_reader:
            try:
                receipt_type = ReceiptType(raw_receipt["type"])
                receipt_payload: ReceiptPayload

                match receipt_type:
                    case ReceiptType.JobStartedReceipt:
                        receipt_payload = JobStartedReceiptPayload(
                            job_uuid=raw_receipt["job_uuid"],
                            miner_hotkey=raw_receipt["miner_hotkey"],
                            validator_hotkey=raw_receipt["validator_hotkey"],
                            timestamp=raw_receipt["timestamp"],  # type: ignore[arg-type]
                            executor_class=ExecutorClass(raw_receipt["executor_class"]),
                            max_timeout=int(raw_receipt["max_timeout"]),
                            is_organic=raw_receipt.get("is_organic") == "True",
                            ttl=int(raw_receipt["ttl"]),
                        )

                    case ReceiptType.JobFinishedReceipt:
                        receipt_payload = JobFinishedReceiptPayload(
                            job_uuid=raw_receipt["job_uuid"],
                            miner_hotkey=raw_receipt["miner_hotkey"],
                            validator_hotkey=raw_receipt["validator_hotkey"],
                            timestamp=raw_receipt["timestamp"],  # type: ignore[arg-type]
                            time_started=raw_receipt["time_started"],  # type: ignore[arg-type]
                            time_took_us=int(raw_receipt["time_took_us"]),
                            score_str=raw_receipt["score_str"],
                        )

                    case ReceiptType.JobAcceptedReceipt:
                        receipt_payload = JobAcceptedReceiptPayload(
                            job_uuid=raw_receipt["job_uuid"],
                            miner_hotkey=raw_receipt["miner_hotkey"],
                            validator_hotkey=raw_receipt["validator_hotkey"],
                            timestamp=raw_receipt["timestamp"],  # type: ignore[arg-type]
                            time_accepted=raw_receipt["time_accepted"],  # type: ignore[arg-type]
                            ttl=int(raw_receipt["ttl"]),
                        )

                receipt = Receipt(
                    payload=receipt_payload,
                    validator_signature=raw_receipt["validator_signature"],
                    miner_signature=raw_receipt["miner_signature"],
                )

            except (KeyError, ValueError, pydantic.ValidationError):
                logger.warning(f"Miner sent invalid receipt {raw_receipt=}")
                continue

            if receipt.payload.miner_hotkey != hotkey:
                logger.warning(f"Miner sent receipt of a different miner {receipt=}")
                continue

            if not receipt.verify_miner_signature():
                logger.warning(f"Invalid miner signature of receipt {receipt=}")
                continue

            if not receipt.verify_validator_signature():
                logger.warning(f"Invalid validator signature of receipt {receipt=}")
                continue

            receipts.append(receipt)

        return receipts
