## Project structure layout

```shell
.
├── area_classification/
│   ├── clustering/
│   │   ├── __init__.py
│   │   └── clustering.py
│   ├── downloading_data/
│   │   ├── __init__.py
│   │   ├── ew_lad_bulk_download.py
│   │   ├── ni_lgd_downloading_data.py
│   │   ├── scot_ca_README.md
│   │   └── scot_tables_reformatting.py
│   ├── post_processing/
│   │   ├── cluster_std_means_to_parent_clusters.py
│   │   ├── cluster_summaries.py
│   │   ├── cluster_table_restructure.py
│   │   ├── cluster_variables_mean.py
│   │   ├── create_radial_plots.py
│   │   └── post_processing.py
│   ├── pre_processing/
│   │   ├── __init__.py
│   │   ├── aggregating_variables.py
│   │   ├── convert_to_percentages.py
│   │   ├── drop_variables.py
│   │   ├── pre_processing.py
│   │   ├── prepare_clustering_data.py
│   │   ├── select_variables.py
│   │   ├── standard_illness_ratio.py
│   │   └── totals_columns_select_uk.py
│   ├── utilities/
│   │   ├── __init__.py
│   │   ├── disability_age_group_conversion.py
│   │   ├── load_config.py
│   │   ├── loading_data.py
│   │   └── qa_functions.py
│   ├── __init__.py
│   ├── aggregation_setup.yaml
│   ├── config.md
│   ├── config.yaml
│   └── main_pipeline.py
├── data/
│   ├── lookups/
│   │   └── UK_selected_codes_lookup.csv
│   └── README.md
├── docs/
│   ├── analytical_quality_assurance/
│   │   ├── aqa_plan.md
│   │   ├── assumptions_caveats.md
│   │   └── data_log.md
│   ├── specifications/
│   │   ├── Clustering.md
│   │   ├── Downloading_data.md
│   │   ├── Post_processing.md
│   │   ├── Pre-processing.md
│   │   └── Standardised_Illness_Ratio.md
│   ├── user_guide/
│   │   ├── naming_conventions.md
│   │   ├── repo_structure.md
│   │   └── using_pytest.md
│   └── README.md
├── tests/
│   ├── data/
│   │   ├── utilities/
│   │   │   ├── expected_config.yaml
│   │   │   └── test_config.yaml
│   │   └── sir_test_expected_output.csv
│   ├── downloading_data/
│   │   ├── test_ew_lad_bulk_download.py
│   │   └── test_scot_tables_reformatting.py
│   ├── integration_tests/
│   │   ├── test_integration_cluster_summaries.py
│   │   └── test_integration_prepare_clustering_data.py
│   ├── post_processing/
│   │   ├── test_cluster_summaries.py
│   │   ├── test_cluster_table_restructure.py
│   │   └── test_cluster_variables_mean.py
│   ├── pre_processing/
│   │   ├── test_aggragating_vairables.py
│   │   ├── test_convert_to_percentages.py
│   │   ├── test_drop_variables.py
│   │   ├── test_prepare_clustering_data.py
│   │   ├── test_select_variables.py
│   │   ├── test_standard_illness_ratio.py
│   │   └── test_totals_columns_select_uk.py
│   ├── utilities/
│   │   └── test_load_config.py
│   ├── README.md
│   ├── test_load_config.py
│   └── test_loading_data.py
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── setup.cfg
└── setup.py
```
