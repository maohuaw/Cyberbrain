from __future__ import annotations

import os
import sys

from google.protobuf import text_format

from cyberbrain.generated import communication_pb2, communication_pb2_grpc

python_version = {(3, 7): "py37", (3, 8): "py38"}[sys.version_info[:2]]


def get_value(value_dict: dict[str, any]):
    """Accept an argument like {'py37': 1, 'py38': 2}.

    Used for version-dependent tests.
    """
    return value_dict[python_version]


def return_GetFrame(
    rpc_stub: communication_pb2_grpc.CommunicationStub, frame_name: str
) -> Frame:
    return rpc_stub.GetFrame(communication_pb2.FrameLocater(frame_name=frame_name))


def assert_GetFrame(
    rpc_stub: communication_pb2_grpc.CommunicationStub, frame_name: str
):
    # print(rpc_stub.GetFrame(communication_pb2.FrameLocater(frame_name=frame_name)))
    golden_filepath = f"test/data/{python_version}/{frame_name}.pbtext"

    directory = os.path.dirname(golden_filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Generates golden data.
    if not os.path.exists(golden_filepath):
        with open(golden_filepath, "wt") as f:
            f.write("# proto-file: communication.proto\n# proto-message: Frame\n\n")
            f.write(
                str(
                    rpc_stub.GetFrame(
                        communication_pb2.FrameLocater(frame_name=frame_name)
                    )
                )
            )
        return

    # Assuming run in root directory.
    with open(golden_filepath, "rt") as f:
        response_text = f.read()

    frame_proto = return_GetFrame(rpc_stub, frame_name)

    assert frame_proto == text_format.Parse(
        response_text, communication_pb2.Frame()
    ), frame_proto
