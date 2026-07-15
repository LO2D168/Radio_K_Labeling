from radio_k_labeling.bounds import graph_diameter, upper_bound
from radio_k_labeling.graph import adjacency_to_distances
from radio_k_labeling.sat.encodings.order_mask import decode_order_model, mask_id, value_id
from radio_k_labeling.validate import validate_labeling


def path_three():
    return [[], [2], [1, 3], [2]]


def test_bfs_uses_legacy_one_based_layout():
    distances = adjacency_to_distances(path_three())
    assert distances == [[-1, -1, -1, -1], [-1, 0, 1, 2], [-1, 1, 0, 1], [-1, 2, 1, 0]]
    assert graph_diameter(distances) == 2


def test_bound_matches_legacy_formula():
    distances = adjacency_to_distances(path_three())
    assert upper_bound(3, 2, distances) == 7


def test_validator_accepts_and_rejects_radio_labelings():
    distances = adjacency_to_distances(path_three())
    assert validate_labeling({1: 1, 2: 3, 3: 5}, 2, distances) == (True, 5)
    assert validate_labeling({1: 1, 2: 2, 3: 3}, 2, distances) == (False, None)


def test_order_model_mapping_and_legacy_decode():
    assert value_id(2, 3, 5) == 8
    assert mask_id(2, 3, 3, 5) == 23
    model = [value_id(1, 1, 5), value_id(1, 3, 5), value_id(2, 1, 5), value_id(2, 4, 5)]
    assert decode_order_model(model, 2, 5) == [0, 3, 4]
