import asyncio
import os
import tempfile
from urllib.parse import quote

import ipfs_hamt_directory_py
import orjson


async def create_car(output_car, documents, limit, name_template) -> (str, bytes):
    with tempfile.TemporaryDirectory() as td:
        input_data = os.path.join(td, 'input_data.txt')
        with open(input_data, 'wb') as f:
            async for document in documents:
                document = orjson.loads(document)
                if limit <= 0:
                    break
                item_name = name_template.format(
                    md5=document['md5'],
                    extension=document.get('metadata', {}).get('extension', 'pdf'),
                )
                f.write(quote(item_name, safe='').encode())
                f.write(b' ')
                f.write(document['cid'].encode())
                f.write(b' ')
                f.write(str(document.get('filesize') or 0).encode())
                f.write(b'\n')
                limit -= 1
        return await asyncio.get_event_loop().run_in_executor(
            None, lambda: ipfs_hamt_directory_py.from_file(input_data, output_car, td),
        )
