from typing import TypeVar, List

CHUNK_LIST = TypeVar('CHUNK_LIST')

def chunk(l: list[CHUNK_LIST], n):
    # looping till length l
    chunked = []
    for i in range(0, len(l), n): 
        chunked.append(l[i:i + n])
    return chunked