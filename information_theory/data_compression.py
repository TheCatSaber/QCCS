from __future__ import annotations

import itertools
from dataclasses import dataclass
import math
from queue import PriorityQueue
from typing import Optional

from cryptography_ import BitString

from .classical_entropy import ClassicalPDF, verify_classical_pdf


def typical_sequences(PDF: ClassicalPDF, n: int) -> list[BitString]:
    verify_classical_pdf(PDF)
    if len(PDF) != 2 or {PDF[0].symbol, PDF[1].symbol} != {"0", "1"}:
        raise ValueError("PDF for typical sequence must be for 0 and 1")

    if n <= 0:
        raise ValueError("Number of sequences required must be at least 1")

    index_of_zero = 0 if PDF[0].symbol == "0" else 1

    no_zeros = int(round(PDF[index_of_zero].probability * n, 0))

    positions = itertools.combinations(range(n), no_zeros)
    sequences: list[BitString] = []
    for pos in positions:
        this_sequence: BitString = [0 if i in pos else 1 for i in range(n)]
        sequences.append(this_sequence)

    return sequences


@dataclass
class BinaryTree:
    weight: float
    symbol: Optional[str]
    left: Optional[BinaryTree]
    right: Optional[BinaryTree]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BinaryTree):
            return NotImplemented

        return (
            math.isclose(self.weight, other.weight, abs_tol=1e-8)
            and (self.symbol == other.symbol)
            and (self.left == other.left)
            and (self.right == other.right)
        )


@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: BinaryTree


def Huffman_coding(PDF: ClassicalPDF) -> BinaryTree:
    verify_classical_pdf(PDF)
    priority_queue: PriorityQueue[PrioritizedItem] = PriorityQueue()
    for symbol in PDF:
        priority_queue.put(
            PrioritizedItem(
                symbol.probability,
                BinaryTree(symbol.probability, symbol.symbol, None, None),
            )
        )
    while True:
        a = priority_queue.get().item
        if priority_queue.empty():
            return a
        b = priority_queue.get().item

        new_node = BinaryTree(a.weight + b.weight, None, a, b)
        priority_queue.put(PrioritizedItem(new_node.weight, new_node))


def Huffman_create_coding(
    tree: BinaryTree,
) -> dict[str, BitString]:
    coding_dict: dict[str, BitString] = {}

    def _DFS(node: BinaryTree, current_string: BitString) -> None:
        if node.symbol is not None:
            coding_dict[node.symbol] = current_string
            return
        if node.left is None or node.right is None:
            raise RuntimeError("None in Binary Tree when there should not be.")
        _DFS(node.left, current_string + [0])
        _DFS(node.right, current_string + [1])

    _DFS(tree, [])
    return coding_dict
