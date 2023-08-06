import numpy as np
import pandas as pd
import random
import html
import base64
import pkgutil
import warnings

from tqdm import tqdm
from IPython.display import display_html
from copy import deepcopy
from json import dump, load, dumps

# We don't need need interpret  in runtime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interpret.glassbox import ExplainableBoostingClassifier

ROUND = 4


def _resort_categorical_level(col_mapping):
    """
    Resort the levels in the categorical encoders if all levels can be converted
    to numbers (integer or float).

    Args:
        col_mapping: the dictionary that maps level string to int

    Returns:
        New col_mapping if all levels can be converted to numbers, otherwise
        the original col_mapping
    """

    def is_number(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    if all(map(is_number, col_mapping.keys())):
        key_tuples = [(k, float(k)) for k in col_mapping.keys()]
        sorted_key_tuples = sorted(key_tuples, key=lambda x: x[1])

        new_mapping = {}
        value = 1

        for t in sorted_key_tuples:
            new_mapping[t[0]] = value
            value += 1

        return new_mapping

    else:
        return col_mapping


def _get_feature_type(ebm, feature_index):
    col_type = ebm.feature_types_in_[feature_index]
    if col_type == "continuous":
        return "continuous"
    elif col_type == "nominal":
        return "categorical"
    else:
        raise Exception("Unsupported feature type", col_type)


def _get_main_bin_labels(ebm, feature_index):
    """Returns main effect bin labels for a given feature index.
    Args:
        feature_index: An integer for feature index.
    Returns:
        List of labels for bins.
    """

    col_type = ebm.feature_types_in_[feature_index]
    if col_type == "continuous":
        min_val = ebm.feature_bounds_[feature_index][0]
        cuts = ebm.bins_[feature_index][0]
        max_val = ebm.feature_bounds_[feature_index][1]
        return list(np.concatenate(([min_val], cuts, [max_val])))
    elif col_type == "nominal":
        cur_map = ebm.bins_[feature_index][0]
        return list(cur_map.keys())
    else:  # pragma: no cover
        raise Exception("Unknown column type")


def _get_pair_bin_labels(ebm, feature_index):
    """Returns pair interaction effect bin labels for a given feature index.
    Args:
        feature_index: An integer for feature index.
    Returns:
        List of labels for bins.
    """

    col_type = ebm.feature_types_in_[feature_index]
    if col_type == "continuous":
        min_val = ebm.feature_bounds_[feature_index][0]
        # The first element is main effect bin cuts
        # If there is a second element, then the pair effect bin cuts are
        # different and are stored there.
        if len(ebm.bins_[feature_index]) > 1:
            cuts = ebm.bins_[feature_index][1]
        else:
            cuts = ebm.bins_[feature_index][0]
        max_val = ebm.feature_bounds_[feature_index][1]
        return list(np.concatenate(([min_val], cuts, [max_val])))
    elif col_type == "nominal":
        cur_map = ebm.bins_[feature_index][0]
        return list(cur_map.keys())
    else:  # pragma: no cover
        raise Exception("Unknown column type")


def _get_hist_counts(ebm, feature_index):
    col_type = ebm.feature_types_in_[feature_index]
    if col_type == "continuous":
        return list(ebm.histogram_weights_[feature_index][1:-1])
    elif col_type == "nominal":
        return list(ebm.histogram_weights_[feature_index][1:-1])
    else:  # pragma: no cover
        raise Exception("Cannot get counts for type: {0}".format(col_type))


def _get_hist_edges(ebm, feature_index):
    col_type = ebm.feature_types_in_[feature_index]
    if col_type == "continuous":
        return list(ebm.histogram_edges_[feature_index])
    elif col_type == "nominal":
        cur_map = ebm.bins_[feature_index][0]
        return list(cur_map.keys())
    else:  # pragma: no cover
        raise Exception("Cannot get counts for type: {0}".format(col_type))


def get_model_data(ebm: "ExplainableBoostingClassifier", resort_categorical=False):
    """
    Get the model data for GAM Changer.
    Args:
        ebm: Trained EBM model. ExplainableBoostingClassifier or
            ExplainableBoostingRegressor object.
        resort_categorical: Whether to sort the levels in categorical variable
            by increasing order if all levels can be converted to numbers.
    Returns:
        A Python dictionary of model data
    """

    # Main model info on each feature
    features = []

    # Track the encoding of categorical feature levels
    labelEncoder = {}

    # Track the score range
    score_range = [np.inf, -np.inf]

    for i, term in tqdm(enumerate(ebm.term_features_)):
        cur_feature = {}
        cur_feature["importance"] = float(ebm.term_importances()[i])

        # Handle interaction term differently from cont/cat
        if i >= len(ebm.feature_names_in_):
            cur_feature["type"] = "interaction"

            cur_id = term
            cur_feature["id"] = list(cur_id)

            # Info for each individual feature
            cur_feature["name1"] = ebm.feature_names_in_[cur_id[0]]
            cur_feature["name2"] = ebm.feature_names_in_[cur_id[1]]
            cur_feature["name"] = f'{cur_feature["name1"]} x {cur_feature["name2"]}'

            cur_feature["type1"] = _get_feature_type(ebm, cur_id[0])
            cur_feature["type2"] = _get_feature_type(ebm, cur_id[1])

            # Skip the first item from both dimensions
            cur_feature["additive"] = np.round(ebm.term_scores_[i], ROUND)[
                1:-1, 1:-1
            ].tolist()
            cur_feature["error"] = np.round(ebm.standard_deviations_[i], ROUND)[
                1:-1, 1:-1
            ].tolist()

            # Get the bin label info
            cur_feature["binLabel1"] = _get_pair_bin_labels(ebm, cur_id[0])
            cur_feature["binLabel2"] = _get_pair_bin_labels(ebm, cur_id[1])

            # Encode categorical levels as integers
            if cur_feature["type1"] == "categorical":
                level_str_to_int = ebm.bins_[cur_id[0]][0]
                cur_feature["binLabel1"] = list(
                    map(lambda x: level_str_to_int[x], cur_feature["binLabel1"])
                )

            if cur_feature["type2"] == "categorical":
                level_str_to_int = ebm.bins_[cur_id[1]][0]
                cur_feature["binLabel2"] = list(
                    map(lambda x: level_str_to_int[x], cur_feature["binLabel2"])
                )

            # Get density info
            if cur_feature["type1"] == "categorical":
                level_str_to_int = ebm.bins_[cur_id[0]][0]
                cur_feature["histEdge1"] = _get_hist_edges(ebm, cur_id[0])
                cur_feature["histEdge1"] = list(
                    map(lambda x: level_str_to_int[x], cur_feature["histEdge1"])
                )
            else:
                cur_feature["histEdge1"] = np.round(
                    _get_hist_edges(ebm, cur_id[0]), ROUND
                ).tolist()

            cur_feature["histCount1"] = np.round(
                _get_hist_counts(ebm, cur_id[0]), ROUND
            ).tolist()

            if cur_feature["type2"] == "categorical":
                level_str_to_int = ebm.bins_[cur_id[1]][0]
                cur_feature["histEdge2"] = _get_hist_edges(ebm, cur_id[1])
                cur_feature["histEdge2"] = list(
                    map(lambda x: level_str_to_int[x], cur_feature["histEdge2"])
                )
            else:
                cur_feature["histEdge2"] = np.round(
                    _get_hist_edges(ebm, cur_id[1]), ROUND
                ).tolist()

            cur_feature["histCount2"] = np.round(
                _get_hist_counts(ebm, cur_id[1]), ROUND
            ).tolist()

        else:
            # Main effects here
            cur_feature["name"] = ebm.feature_names_in_[i]
            cur_feature["type"] = _get_feature_type(ebm, i)

            # Skip the first item (reserved for missing value)
            cur_feature["additive"] = np.round(ebm.term_scores_[i], ROUND).tolist()[
                1:-1
            ]
            cur_feature["error"] = np.round(
                ebm.standard_deviations_[i], ROUND
            ).tolist()[1:-1]
            cur_id = term[0]
            cur_feature["id"] = [cur_id]
            cur_feature["count"] = ebm.bin_weights_[cur_id].tolist()[1:-1]

            # Track the global score range
            score_range[0] = float(
                min(
                    score_range[0],
                    np.min(ebm.term_scores_[i] - ebm.standard_deviations_[i]),
                )
            )
            score_range[1] = float(
                max(
                    score_range[1],
                    np.max(ebm.term_scores_[i] + ebm.standard_deviations_[i]),
                )
            )

            # Add the binning information for continuous features
            if cur_feature["type"] == "continuous":
                # Add the bin information
                cur_feature["binEdge"] = _get_main_bin_labels(ebm, cur_id)

                # Add the hist information
                cur_feature["histEdge"] = np.round(
                    _get_hist_edges(ebm, cur_id), ROUND
                ).tolist()
                cur_feature["histCount"] = np.round(
                    _get_hist_counts(ebm, cur_id), ROUND
                ).tolist()

            elif cur_feature["type"] == "categorical":
                # Get the level value mapping
                level_str_to_int = ebm.bins_[cur_id][0]

                if resort_categorical:
                    level_str_to_int = _resort_categorical_level(level_str_to_int)

                cur_feature["binLabel"] = list(
                    map(
                        lambda x: level_str_to_int[x],
                        _get_main_bin_labels(ebm, cur_id),
                    )
                )

                # Add the hist information
                # For categorical data, the edges are strings
                cur_feature["histEdge"] = list(
                    map(
                        lambda x: level_str_to_int[x],
                        _get_hist_edges(ebm, cur_id),
                    )
                )

                cur_feature["histCount"] = np.round(
                    _get_hist_counts(ebm, cur_id), ROUND
                ).tolist()

                if resort_categorical:
                    cur_bin_info = list(
                        zip(
                            cur_feature["binLabel"],
                            cur_feature["additive"],
                            cur_feature["error"],
                            cur_feature["count"],
                        )
                    )
                    cur_bin_info = sorted(cur_bin_info, key=lambda x: x[0])

                    cur_feature["binLabel"] = [k[0] for k in cur_bin_info]
                    cur_feature["additive"] = [k[1] for k in cur_bin_info]
                    cur_feature["error"] = [k[2] for k in cur_bin_info]
                    cur_feature["count"] = [k[3] for k in cur_bin_info]

                    cur_hist_info = list(
                        zip(cur_feature["histEdge"], cur_feature["histCount"])
                    )
                    cur_hist_info = sorted(cur_hist_info, key=lambda x: x[0])

                    cur_feature["histEdge"] = [k[0] for k in cur_hist_info]
                    cur_feature["histCount"] = [k[1] for k in cur_hist_info]

                # Add the label encoding information
                labelEncoder[cur_feature["name"]] = {
                    str(i): s for s, i in level_str_to_int.items()
                }

        features.append(cur_feature)

    score_range = list(map(lambda x: round(x, 4), score_range))

    data = {
        "intercept": float(ebm.intercept_[0])
        if hasattr(ebm, "classes_")
        else float(ebm.intercept_),
        "isClassifier": hasattr(ebm, "classes_"),
        "features": features,
        "labelEncoder": labelEncoder,
        "scoreRange": score_range,
    }

    return data


def get_sample_data(
    ebm: "ExplainableBoostingClassifier", x_test, y_test, resort_categorical=False
):
    """
    Get the sample data for GAM Changer.
    Args:
        ebm: Trained EBM model. ExplainableBoostingClassifier or
            ExplainableBoostingRegressor object.
        x_test: Sample features. 2D np.ndarray or pd.DataFrame with dimension [n, k]:
            n samples and k features.
        y_test: Sample labels. 1D np.ndarray or pd.Series with size = n samples.
        resort_categorical: Whether to sort the levels in categorical variable
            by increasing order if all levels can be converted to numbers.
    Returns:
        A Python dictionary of sample data.
    """

    assert isinstance(x_test, (pd.DataFrame, np.ndarray))
    assert isinstance(y_test, (pd.Series, np.ndarray))

    feature_names = []
    feature_types = []

    # Sample data does not record interaction features
    for i, name in enumerate(ebm.feature_names_in_):
        feature_names.append(name)
        feature_types.append(_get_feature_type(ebm, i))

    # Transform the dataframe to object array
    x_test_copy = deepcopy(x_test)
    y_test_copy = deepcopy(y_test)

    if isinstance(x_test, pd.DataFrame):
        x_test_copy = x_test.to_numpy()

    if isinstance(y_test, pd.Series):
        y_test_copy = y_test.to_numpy()

    # Drop all rows with any NA values
    if pd.isnull(x_test_copy).any():
        na_row_indexes = pd.isnull(x_test_copy).any(axis=1)
        x_test_copy = x_test_copy[~na_row_indexes]
        y_test_copy = y_test_copy[~na_row_indexes]

        warnings.warn(
            "Sample data contains missing values. Currently GAM Changer does "
            + f"not support missing values. Dropped {np.sum(na_row_indexes)} rows with NAs."
        )

    # Encode the categorical variables as integers
    for i, cur_type in enumerate(feature_types):
        if cur_type == "categorical":
            level_str_to_int = ebm.bins_[i][0]

            if resort_categorical:
                level_str_to_int = _resort_categorical_level(level_str_to_int)

            def get_level_int(x):
                if str(x) in level_str_to_int:
                    return level_str_to_int[str(x)]
                else:
                    # Current sample has an unseen level, we label it as max
                    # level + 1
                    return max(level_str_to_int.values()) + 1

            x_test_copy[:, i] = list(map(lambda x: get_level_int(x), x_test_copy[:, i]))

    sample_data = {
        "featureNames": feature_names,
        "featureTypes": feature_types,
        "samples": x_test_copy.tolist(),
        "labels": y_test_copy.tolist(),
    }

    return sample_data


def _overwrite_bin_definition(
    ebm: "ExplainableBoostingClassifier", index_id, new_bins, new_scores
):
    """
    Overwrite the bin definitions and scores for continuous variables.

    Args:
        ebm: EBM object
        index_id: Feature's index id in the ebm object
        new_bins: New bin definition
        new_score: New bin scores

    In python, to overwrite the bins, we want to overwrite pair
    `edge[:] with score[2:]` and pair `col_min_ with score [1]`.

    In GAM Changer and EBM.JS, stored bins are `python_label[:-1]` and `python_score[1:]`

    To map GAM Changer and EBM.JS's `newBins`, `newScores` back to Python:

    ```
    newBins[0] => col_min_
    newBins[1:] => col_bin_edges_

    newScores[:] => additive_terms_[1:]
    ```

    We also want to update the standard deviation information:

    Case 1: Bin definition has not changed:
        We zero out the SDs of bins that have been modified

    Case 2: Bin definition has changed (even just a subset):
        We zero out all the SDs of bins

    In Python, SDs share the same index as scores.
    """

    assert len(new_bins) == len(new_scores)

    # Check if GAM Changer has changed the bin definition
    binDefChanged = False

    if len(new_bins) - 1 != len(ebm.bins_[index_id][0]):
        binDefChanged = True

    else:
        for i in range(1, len(new_bins)):
            if new_bins[i] != round(ebm.bins_[index_id][0][i - 1], ROUND):
                binDefChanged = True
                break

    # Update the SDs
    if binDefChanged:
        ebm.standard_deviations_[index_id] = np.zeros(len(new_scores) + 1)
    else:
        # Iterate through the scores to zero out SDs of modified bins
        for i in range(1, len(ebm.term_scores_[index_id]) - 1):
            if round(ebm.term_scores_[index_id][i], ROUND) != new_scores[i - 1]:
                ebm.standard_deviations_[index_id][i] = 0

    # Overwrite the scores
    ebm.term_scores_[index_id] = np.array(
        [ebm.term_scores_[index_id][0]] + new_scores + [ebm.term_scores_[index_id][-1]]
    ).astype(np.float64)

    # Overwrite the bin edges

    # GAM Changer won't change the edge for col_min_, because it
    # will always be one of the end points in any interpolations
    # So we don't really need to change col_min_, change here for testing purpose
    ebm.feature_bounds_[index_id][0] = new_bins[0]
    ebm.bins_[index_id][0] = np.array(new_bins[1:]).astype(np.float64)


def get_edited_model(ebm: "ExplainableBoostingClassifier", gamchanger_export):
    """
    Return a copy of ebm that is modified based on the edits from GAM Changer.

    Args:
        ebm: EBM object
        gamchanger_export: Python dictionary: loaded from the GAM Changer
            export (*.gamchanger)

    Returns:
        An edited deep copy of ebm object.
    """
    ebm_copy = deepcopy(ebm)

    history = gamchanger_export["historyList"]

    # Mapping from feature name to feature type
    feature_name_to_type = dict(
        zip(ebm_copy.feature_names_in_, ebm_copy.feature_types_in_)
    )

    # Keep track which feature has been updated in ebm_copy
    updated_features = set()

    # Use the ebm's mapping to map level name to bin index
    ebm_col_mapping = ebm_copy.bins_

    # We iterate through the history list from the newest edit to the older edit
    # For each modified feature, we overwrite the bin definitions/scores on an EBM
    # copy using the latest edit info on that feature.
    # Note that GAM Changer can only change the bin definitions of continuous features

    for i in range(len(history) - 1, -1, -1):
        cur_history = history[i]

        # Original edit does not change the graph
        if cur_history["type"] == "original":
            continue

        cur_name = cur_history["featureName"]
        cur_index = ebm_copy.feature_names_in_.index(cur_name)

        # If we have already updated EBM on this feature, skip earlier edits
        if cur_name in updated_features:
            continue

        if feature_name_to_type[cur_name] == "continuous":
            # Collect bin edges and scores
            bin_data = cur_history["state"]["pointData"]
            bin_edges, bin_scores = [], []

            # bin_data is a linked list, bin_data[0] is guaranteed to be the start
            # point of all bins
            cur_bin = bin_data["0"]

            while cur_bin["rightPointID"]:
                bin_edges.append(cur_bin["x"])
                bin_scores.append(cur_bin["y"])
                cur_bin = bin_data[str(cur_bin["rightPointID"])]

            # Handle the last bin
            bin_edges.append(cur_bin["x"])
            bin_scores.append(cur_bin["y"])

            assert len(bin_edges) == len(bin_data)

            # Overwrite EBM bin definitions/additive terms with bin_edges and bin_scores
            _overwrite_bin_definition(ebm_copy, cur_index, bin_edges, bin_scores)
            updated_features.add(cur_name)

        elif feature_name_to_type[cur_name] == "nominal":
            # Get the current level mapping
            cur_mapping = ebm_col_mapping[cur_index][0]

            # Collect bin edges and scores
            bin_data = cur_history["state"]["pointData"]
            bin_edges, bin_scores = [], []

            for k in bin_data:
                point = bin_data[k]
                bin_edges.append(point["x"])
                bin_scores.append(point["y"])

            assert len(bin_edges) == len(bin_scores)

            # Update the additive term
            for j, edge in enumerate(bin_edges):
                cur_score = bin_scores[j]
                cur_bin_index = cur_mapping[edge]

                if (
                    round(ebm_copy.term_scores_[cur_index][cur_bin_index], ROUND)
                    != cur_score
                ):
                    ebm_copy.term_scores_[cur_index][cur_bin_index] = cur_score

            updated_features.add(cur_name)

        else:
            raise ValueError(
                "Encounter unknown feature type {}".format(
                    feature_name_to_type[cur_name]
                )
            )

    return ebm_copy


def _make_html(ebm, x_test, y_test, resort_categorical):
    """
    Function to create an HTML string to bundle GAM Changer's html, css, and js.
    We use base64 to encode the js so that we can use inline defer for <script>

    We add another script to pass Python data as inline json, and dispatch an
    event to transfer the data

    Args:
        ebm: Trained EBM model. ExplainableBoostingClassifier or
            ExplainableBoostingRegressor object.
        x_test: Sample features. 2D np.ndarray or pd.DataFrame with dimension [n, k]:
            n samples and k features.
        y_test: Sample labels. 1D np.ndarray or pd.Series with size = n samples.
        resort_categorical: Whether to sort the levels in categorical variable
            by increasing order if all levels can be converted to numbers.

    Return:
        HTML code with deferred JS code in base64 format
    """
    # HTML template for GAM Changer widget
    html_top = """<!DOCTYPE html><html lang="en"><head><meta charset='utf-8'><meta name='viewport' content='width = device-width, initial-scale = 1'><title>GAM Changer</title><style>html,body{position:relative;width:100%;height:100%}body{color:#333;margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif}a{color:rgb(0,100,200);text-decoration:none}a:hover{text-decoration:underline}a:visited{color:rgb(0,80,160)}label{display:block}input,button,select,textarea{font-family:inherit;font-size:inherit;-webkit-padding:0.4em 0;padding:0.4em;margin:0 0 0.5em 0;box-sizing:border-box;border:1px solid #ccc;border-radius:2px}input:disabled{color:#ccc}</style>"""
    html_bottom = """</head><body></body></html>"""

    # Read the bundled JS file
    js_string = pkgutil.get_data(__name__, "gamchanger.js")
    # js_b = bytes(js_string, encoding='utf-8')

    # Encode the JS & CSS with base 64
    js_base64 = base64.b64encode(js_string).decode("utf-8")

    # Generate the model and sample data
    model_data = get_model_data(ebm, resort_categorical=resort_categorical)

    if x_test is not None and y_test is not None:
        sample_data = get_sample_data(
            ebm, x_test, y_test, resort_categorical=resort_categorical
        )
    else:
        sample_data = None

    # Pass the data to GAM Changer using message event
    data_json = dumps({"model": model_data, "sample": sample_data})

    # Pass data into JS by using another script to dispatch an event
    messenger_js = """
        (function() {{
            let data = {data};
            let event = new Event('gamchangerData');
            event.data = data;
            console.log('before');
            console.log(data);
            document.dispatchEvent(event);
        }}())
    """.format(
        data=data_json
    )
    messenger_js = messenger_js.encode()
    messenger_js_base64 = base64.b64encode(messenger_js).decode("utf-8")

    # Inject the JS to the html template
    html_str = (
        html_top
        + """<script defer src='data:text/javascript;base64,{}'></script>""".format(
            js_base64
        )
        + """<script defer src='data:text/javascript;base64,{}'></script>""".format(
            messenger_js_base64
        )
        + html_bottom
    )

    return html.escape(html_str)


def _make_html_with_data(model_data, sample_data):
    """
    Function to create an HTML string to bundle GAM Changer's html, css, and js.
    We use base64 to encode the js so that we can use inline defer for <script>

    We add another script to pass Python data as inline json, and dispatch an
    event to transfer the data

    Args:
        model_data: A dictionary of the EBM model weights.
        sample_data: A dictionary of the test samples.

    Return:
        HTML code with deferred JS code in base64 format
    """
    # HTML template for GAM Changer widget
    html_top = """<!DOCTYPE html><html lang="en"><head><meta charset='utf-8'><meta name='viewport' content='width = device-width, initial-scale = 1'><title>GAM Changer</title><style>html,body{position:relative;width:100%;height:100%}body{color:#333;margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif}a{color:rgb(0,100,200);text-decoration:none}a:hover{text-decoration:underline}a:visited{color:rgb(0,80,160)}label{display:block}input,button,select,textarea{font-family:inherit;font-size:inherit;-webkit-padding:0.4em 0;padding:0.4em;margin:0 0 0.5em 0;box-sizing:border-box;border:1px solid #ccc;border-radius:2px}input:disabled{color:#ccc}</style>"""
    html_bottom = """</head><body></body></html>"""

    # Read the bundled JS file
    js_string = pkgutil.get_data(__name__, "gamchanger.js")
    # js_b = bytes(js_string, encoding='utf-8')

    # Encode the JS & CSS with base 64
    js_base64 = base64.b64encode(js_string).decode("utf-8")

    # Pass the data to GAM Changer using message event
    data_json = dumps({"model": model_data, "sample": sample_data})

    # Pass data into JS by using another script to dispatch an event
    messenger_js = """
        (function() {{
            let data = {data};
            let event = new Event('gamchangerData');
            event.data = data;
            console.log('before');
            console.log(data);
            document.dispatchEvent(event);
        }}())
    """.format(
        data=data_json
    )
    messenger_js = messenger_js.encode()
    messenger_js_base64 = base64.b64encode(messenger_js).decode("utf-8")

    # Inject the JS to the html template
    html_str = (
        html_top
        + """<script defer src='data:text/javascript;base64,{}'></script>""".format(
            js_base64
        )
        + """<script defer src='data:text/javascript;base64,{}'></script>""".format(
            messenger_js_base64
        )
        + html_bottom
    )

    return html.escape(html_str)


def visualize(
    ebm,
    x_test=None,
    y_test=None,
    resort_categorical=False,
    model_data=None,
    sample_data=None,
):
    """
    Render GAM Changer in the output cell.

    Args:
        ebm: Trained EBM model. ExplainableBoostingClassifier or
            ExplainableBoostingRegressor object.
        x_test: Sample features. 2D np.ndarray or pd.DataFrame with dimension [n, k]:
            n samples and k features.
        y_test: Sample labels. 1D np.ndarray or pd.Series with size = n samples.
        model_data: Pre-generated EBM weights in a dictionary
        sample_data: Pre-generated sample data in a dictionary
        resort_categorical: Whether to sort the levels in categorical variable
            by increasing order if all levels can be converted to numbers.
    """
    if model_data is None and sample_data is None:
        html_str = _make_html(ebm, x_test, y_test, resort_categorical)
    else:
        html_str = _make_html_with_data(model_data, sample_data)

    # Randomly generate an ID for the iframe to avoid collision
    iframe_id = "gam-changer-iframe-" + str(int(random.random() * 1e8))

    iframe = """
        <iframe
            srcdoc="{}"
            frameBorder="0"
            width="100%"
            height="645px"
            id="{}">
        </iframe>
    """.format(
        html_str, iframe_id
    )

    # Display the iframe
    display_html(iframe, raw=True)
