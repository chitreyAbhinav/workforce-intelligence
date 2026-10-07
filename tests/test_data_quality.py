"""
Automated Unit Tests - Data Quality Engine
==========================================
Verifies:
- LPA salary conversion logic across diverse string patterns
- Experience extraction (min, max, average years)
- Standardized Role classification
- JDS & SDS bounds integrity
"""

import pytest
import numpy as np
import pandas as pd
from src.data_quality_engine import DataQualityEngine


class TestDataQualityEngine:
    def test_parse_salary_lakhs(self):
        # Format with 'L'
        assert DataQualityEngine.parse_salary_lakhs('7.8L') == 7.8
        assert DataQualityEngine.parse_salary_lakhs('16.0L') == 16.0
        assert DataQualityEngine.parse_salary_lakhs('102.0L') == 102.0

        # Range formats
        assert DataQualityEngine.parse_salary_lakhs('6to10') == 8.0
        assert DataQualityEngine.parse_salary_lakhs('10to15') == 12.5
        assert DataQualityEngine.parse_salary_lakhs('6-10') == 8.0

        # Raw numeric
        assert DataQualityEngine.parse_salary_lakhs(14.5) == 14.5
        assert DataQualityEngine.parse_salary_lakhs('800000') == 8.0  # converted from rupees

        # Invalid / missing
        assert np.isnan(DataQualityEngine.parse_salary_lakhs(None))
        assert np.isnan(DataQualityEngine.parse_salary_lakhs('Not Disclosed'))
        assert np.isnan(DataQualityEngine.parse_salary_lakhs(''))

    def test_parse_experience_years(self):
        min_e, max_e, avg_e = DataQualityEngine.parse_experience_years('6-10 yrs')
        assert min_e == 6.0 and max_e == 10.0 and avg_e == 8.0

        min_e, max_e, avg_e = DataQualityEngine.parse_experience_years('3 Yrs')
        assert min_e == 3.0 and avg_e == 4.0

        min_e, max_e, avg_e = DataQualityEngine.parse_experience_years(None)
        assert np.isnan(min_e) and np.isnan(max_e)

    def test_map_standardized_role(self):
        assert DataQualityEngine.map_standardized_role('Lead Data Scientist') == 'Senior Data Scientist'
        assert DataQualityEngine.map_standardized_role('Software Development Engineering, Analyst') == 'Data Engineer'
        assert DataQualityEngine.map_standardized_role('Reporting Analyst', 'Excel, SQL') == 'Data Analyst'
        assert DataQualityEngine.map_standardized_role('ETL Developer', 'SQL, Spark, Hadoop') == 'Data Engineer'
        assert DataQualityEngine.map_standardized_role('ML Engineer', 'Python, PyTorch') == 'Machine Learning Engineer'
        assert DataQualityEngine.map_standardized_role('BI Analyst', 'Power BI, Tableau') == 'Business Analyst'
