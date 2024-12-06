import pytest  # type: ignore
import sys
from model_interpreter.interpreter import ModelInterpreter  # type: ignore
from hypothesis import given, strategies as st, settings, HealthCheck
import pandas as pd  # type: ignore

sys.path.append("../")


class TestKernelTransform(object):
    """Tests for ModelInterpreter.transform(). Specifically for the kernel explainer"""

    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_expected_output_name_value_dicts(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that transform returns the expected output when return_type = "name_value_dicts" """

        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(kernel_single_row, return_type="name_value_dicts")
        keys_to_check = {"Name", "Value"}
        check_flag = all(
            isinstance(item, dict) and keys_to_check == set(item.keys())
            for item in df_transformed
        )
        expected = True
        actual = check_flag

        assert expected == actual

    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_expected_output_name_value_dicts_contents(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that the dictionaries in the output when transform return_type is "name_value_dicts" contain the expected outputs"""

        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(kernel_single_row, return_type="name_value_dicts")
        check_flag = all(
            isinstance(item["Name"], str) and isinstance(item["Value"], float)
            for item in df_transformed
        )
        expected = True
        actual = check_flag

        assert expected == actual

    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_expected_output_rounded_decimals(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that the dictionaries in the output when transform return_type is "name_value_dicts" contain the expected outputs"""

        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(
            kernel_single_row, return_type="name_value_dicts", return_precision=10
        )
        check_flag = all(
            round(item["Value"], 10) == item["Value"] for item in df_transformed
        )
        expected = True
        actual = check_flag

        assert expected == actual

    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_expected_output_tuples(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that transform returns the expected output when return_type = "tuples" """

        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(kernel_single_row, return_type="tuples")
        check_flag = all(isinstance(item, tuple) for item in df_transformed)
        expected = True
        actual = check_flag

        assert expected == actual

    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_expected_output_dicts(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that transform returns the expected output when return_type = "dicts" """

        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(kernel_single_row, return_type="dicts")
        check_flag = all(isinstance(item, dict) for item in df_transformed)
        expected = True
        actual = check_flag

        assert expected == actual

    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_expected_output_single_dict(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that transform returns the expected output when return_type = "single_dict" """

        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(kernel_single_row, return_type="single_dict")
        check_flag = isinstance(df_transformed, dict)
        expected = True
        actual = check_flag

        assert expected == actual

    # sorting types
    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_expected_output_abs(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that transform returns the expected output when sorting = "abs" """

        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(
            kernel_single_row, sorting="abs", return_type="dicts"
        )
        newlist = sorted(
            df_transformed,
            key=lambda df_transformed: list(map(abs, df_transformed.values())),
            reverse=True,
        )
        expected = df_transformed
        actual = newlist

        assert expected == actual

    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_expected_output_label_1(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that transform returns the expected output when sorting = "label" and
        pred_label = 1
        """
        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(
            kernel_single_row, sorting="label", pred_label=1, return_type="dicts"
        )
        newlist = sorted(
            df_transformed,
            key=lambda df_transformed: list(df_transformed.values()),
            reverse=True,
        )
        expected = df_transformed
        actual = newlist

        assert expected == actual

    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_expected_output_label_0(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that transform returns the expected output when sorting = "label" and
        pred_label = 0
        """
        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(
            kernel_single_row, sorting="label", pred_label=0, return_type="dicts"
        )
        newlist = sorted(
            df_transformed,
            key=lambda df_transformed: list(df_transformed.values()),
            reverse=False,
        )
        expected = df_transformed
        actual = newlist

        assert expected == actual

    # n_return
    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    @given(s=st.integers().filter(lambda x: x > 0))
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_kernel_expected_output_n_return(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        s: int,
        features: list,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that transform returns the expected output when n_return = any integer>0"""

        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(
            kernel_single_row, n_return=s, return_type="dicts"
        )

        if 0 < s <= len(features):
            expected = len(df_transformed)
            actual = s
        else:
            expected = len(df_transformed)
            actual = len(features)

        assert expected == actual

    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    @given(s=st.booleans())
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_kernel_expected_output_return_feature_values(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        s: int,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that transform returns the expected output when return_feature_values = True or False"""

        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(
            kernel_single_row, return_feature_values=s, return_type="dicts"
        )

        if not s:
            count = len(df_transformed[1].values())
            expected = count
            actual = 1
        else:
            count = len(list(df_transformed[1].values())[0])
            expected = count
            actual = 2

        assert expected == actual

    # feature_mappings
    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_expected_output_return_feature_mappings(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that transform returns the expected output when feature_mappings = mapping_dict"""
        mapping_dict = {
            "MedInc": "MedInc feature",
            "HouseAge": "Age of house",
            "AveRooms": "Average number of rooms",
            "AveBedrms": "Average number of bedrooms",
            "Population": "Population feature",
            "AveOccup": "Average occupation",
        }

        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(
            kernel_single_row, feature_mappings=mapping_dict, return_type="dicts"
        )

        all_keys = set().union(
            *(df_transformed.keys() for df_transformed in df_transformed)
        )

        check_flag = set(list(all_keys)) == set(list(mapping_dict.values()))
        expected = True
        actual = check_flag
        assert expected == actual

    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_expected_output_return_group_mappings(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test that transform returns the expected output when feature_mappings = grouping_dict"""
        grouping_dict = {
            "MedInc": "MedInc feature",
            "HouseAge": "Age of house",
            "AveRooms": "Number of rooms",
            "AveBedrms": "Number of rooms",
            "Population": "Population feature",
            "AveOccup": "Average occupation",
        }

        model_type = request.getfixturevalue(Model)
        MI.fit(model_type, kernel_X_train, is_classification=is_classification)
        df_transformed = MI.transform(
            kernel_single_row, feature_mappings=grouping_dict, return_type="dicts"
        )

        all_keys = set().union(
            *(df_transformed.keys() for df_transformed in df_transformed)
        )
        check_flag = set(list(all_keys)) == set(list(grouping_dict.values()))
        expected = True
        actual = check_flag

        assert expected == actual

    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_error_sorting_input_not_supported(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test to check ValueError if x.transform() sorting method is not supported"""
        with pytest.raises(
            ValueError,
            match="sorting method not supported",
        ):
            model_type = request.getfixturevalue(Model)
            MI.fit(model_type, kernel_X_train, is_classification=is_classification)
            MI.transform(kernel_single_row, sorting="XYZ", return_type="dicts")

    @pytest.mark.parametrize(
        "Model, is_classification",
        [("balanced_bagging_classifier", True), ("balanced_bagging_regressor", False)],
    )
    def test_kernel_error_return_type_not_supported(
        self,
        MI: ModelInterpreter,
        Model,
        kernel_X_train: pd.Series,
        kernel_single_row: pd.DataFrame,
        is_classification: bool,
        request,
    ) -> None:
        """Test to check ValueError if x.transform() return_type method is not supported"""
        with pytest.raises(
            ValueError,
            match="return_type not supported",
        ):
            model_type = request.getfixturevalue(Model)
            MI.fit(model_type, kernel_X_train, is_classification=is_classification)
            MI.transform(kernel_single_row, return_type="XYZ")
