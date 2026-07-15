"""The legacy order-plus-mask SAT variable mapping."""


def value_id(vertex: int, label: int, span: int) -> int:
    """Return the legacy ``getVal(vertex, label)`` variable id."""
    return (vertex - 1) * span + label


def mask_id(vertex: int, label: int, vertex_count: int, span: int) -> int:
    """Return the legacy ``getMask(vertex, label)`` variable id."""
    return vertex_count * span + (vertex - 1) * span + label


def decode_order_model(model: list[int], vertex_count: int, span: int) -> list[int]:
    """Decode positive order variables exactly as the legacy checker does."""
    labels = [0] * (vertex_count + 1)
    limit = vertex_count * span
    for literal in model:
        if 1 <= literal <= limit:
            index = literal - 1
            vertex = index // span + 1
            label = index % span + 1
            labels[vertex] = label
    return labels
