import unittest
from app import app_processes



class TestChartDataFunctions(unittest.TestCase):

    def test_dictionary_sums_up_expenses_for_categories(self):
        """
        Test that sumCategoryData(expenseArrOfTups) returns a dictionary with correctly summed up expenses
        """

        input = [('Food', 2.50), ('Food', 3), ('Entertainment', 15.50), ('Other', 25), ('Food', 2.50)]

        expected = {"Food": 8.0,
                    "Entertainment": 15.5,
                    "Health": 0,
                    "Debt": 0,
                    "Gift": 0,
                    "Education": 0,
                    "Travel": 0,
                    "Other": 25}

        result = app_processes.sumCategoryData(input)

        self.assertEqual(result, expected)


    def test_category_and_percent_of_total_expense_converts_to_percentage(self):
        """
        Test that convertToChartData(categoryDic) returns an array of arrays that has the correct percentage of total expenses for respective categories
        """

        input = {"Food": 8.0,
                "Entertainment": 15.5,
                "Health": 0,
                "Debt": 0,
                "Gift": 0,
                "Education": 0,
                "Travel": 0,
                "Other": 25}

        # sum of expenses = 48.5; food = 8 / 48.5 * 100; entertainment = 15.5 / 48.5 * 100; other = 25 / 48.5 * 100
        expected = [['Food', 16.49],
                    ['Entertainment', 31.96],
                    ['Health', 0],
                    ['Debt', 0],
                    ['Gift', 0],
                    ['Education', 0],
                    ['Travel', 0],
                    ['Other', 51.55]]

        result = app_processes.convertToChartData(input)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
