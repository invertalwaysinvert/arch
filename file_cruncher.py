import os
import sys
import queue
import gzip
import base64


def compress_and_encode_file(file_path):
    # Read the content of the file
    with open(file_path, "rb") as file:
        file_content = file.read()

    # Compress the file content using gzip
    compressed_content = gzip.compress(file_content)

    # Encode the compressed content using base64
    encoded_content = base64.b64encode(compressed_content)

    return encoded_content.decode("ascii")


def convert_to_file_entry(path: str):
    if ".DS_Store" in path:
        return None

    if "nvim/" in path:
        return None

    content = compress_and_encode_file(path)

    # Permission
    permission = os.stat(path).st_mode
    permission = oct(permission)[-3:]

    # Format path
    path = "/".join(path.split("/")[1:])

    # Output
    content = """
  - content: {content}
    encoding: gz+b64
    path: /{path}
    permissions: '0{permission}'""".format(
        content=content, path=path, permission=permission
    )
    if path.startswith("home"):
        content = content + "\n    owner: arch:arch\n    defer: true"
    return content


def files_to_write():
    root = "airootfs"
    next = queue.SimpleQueue()
    next.put(root)
    entries = []
    while not next.empty():
        path = next.get()
        if os.path.isdir(path):
            children = os.listdir(path)
            children = list(map(lambda x: f"{path}/{x}", children))
            for child in children:
                next.put(child)
        else:
            if output := convert_to_file_entry(path):
                entries.append(output.rstrip())
    return "".join(entries)
