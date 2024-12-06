# Imports
# Standard Library Imports
import unittest
import pathlib

# External Imports
import numpy as np

# Local Imports
from pepitatools import utils
from pepitatools.configuration import set_config_setting


class TestUtils(unittest.TestCase):
    def test_equalsish(self):
        self.assertTrue(utils.equalsish(2, 2))
        self.assertTrue(utils.equalsish(1 / 7, 1 / 7))
        self.assertTrue(utils.equalsish(0.000001, 0.000002))

        self.assertFalse(utils.equalsish(0.01, 0.02))
        self.assertFalse(utils.equalsish(1000, -1000))

    def test_extract_number(self):
        self.assertTrue(np.isnan(utils.extract_number("abc")))
        self.assertTrue(utils.extract_number("easy as 123") == 123)
        self.assertTrue(
            utils.extract_number("remember remember the 5th of November") == 5
        )
        self.assertTrue(utils.extract_number("4-score and 20 years ago") == 4)
        self.assertTrue(utils.extract_number("pi is approximately 3.14159") == 3.14159)

    def test_get_inputs_hashfile(self):
        log_dir = pathlib.Path(__file__).parent / "tmp_logs"
        log_dir.mkdir(exist_ok=True)
        set_config_setting("log_dir", str(log_dir))

        self.assertTrue(
            utils.get_inputs_hashfile(dummy1=1, dummy2="two", dummy3=3.0)
            == utils.get_inputs_hashfile(dummy1=1, dummy2="two", dummy3=3.0)
        )
        self.assertTrue(
            utils.get_inputs_hashfile(dummy1=1, dummy2="two", dummy3=3.0)
            != utils.get_inputs_hashfile(dummy1=1, dummy2="two", dummy3=4.0)
        )

        # Delete the temporary log directory, and its contents
        for f in log_dir.glob("*"):
            # Clear out the cache directory
            if f.name == ".cache":
                for sub_f in f.glob("*"):
                    sub_f.unlink()
                f.rmdir()
                continue
            f.unlink()
        log_dir.rmdir()

    def test_put_multimap(self):
        dict_ = {}
        utils.put_multimap(dict_, "key", "value")
        self.assertDictEqual(dict_, {"key": ["value"]})

    def test_cocktail(self):
        self.assertEqual(utils.Cocktail("A"), utils.Cocktail("A"))
        self.assertNotEqual(utils.Cocktail("A"), utils.Cocktail("B"))
        self.assertEqual(
            utils.Cocktail(("A", "B"), 50, utils.Ratio(1, 1)),
            utils.Cocktail(("A", "B"), 50, utils.Ratio(1, 1)),
        )
        self.assertNotEqual(
            utils.Cocktail(("A", "B"), 50, utils.Ratio(1, 1)),
            utils.Cocktail(("A", "C"), 50, utils.Ratio(1, 1)),
        )
        self.assertNotEqual(
            utils.Cocktail(("A", "B"), 50, utils.Ratio(1, 1)),
            utils.Cocktail(("A", "B"), 50, utils.Ratio(2, 1)),
        )

    def test_dose(self):
        assert utils.Dose("XYZ99", conversions={"XYZ99": "XYZ 1μM"}).drug == "XYZ"
        assert utils.Dose("XYZ99", conversions={"XYZ99": "XYZ 1μM"}).quantity == 1
        assert utils.Dose("XYZ99", conversions={"XYZ99": "XYZ 1μM"}).unit == "μM"
        assert utils.Dose("XYZ 1μM").drug == "XYZ"
        assert utils.Dose("XYZ 1μM").quantity == 1
        assert utils.Dose("XYZ 1μM").unit == "μM"
        assert utils.Dose("XYZ99", conversions={"XYZ99": "XYZ 1μM"}) == utils.Dose(
            "XYZ 1μM"
        )
        assert utils.Dose("XYZ99", conversions={"XYZ99": "XYZ 1μM"}) != utils.Dose(
            "XYZ 2μM"
        )
        assert utils.Dose("XYZ 1μg/mL").unit == "μg/mL"

        assert float(utils.Dose("XYZ 1μM")) == 1
        assert float(utils.Dose("XYZ99", conversions={"XYZ99": "XYZ 1μM"})) == 1

        assert utils.Dose("XYZ 1μM") + 1 == utils.Dose("XYZ 2μM")
        assert 1 + utils.Dose("XYZ 1μM") == utils.Dose("XYZ 2μM")
        assert utils.Dose("XYZ 1μM") + utils.Dose("XYZ 1μM") == utils.Dose("XYZ 2μM")

        assert utils.Dose("XYZ 1μM") * 1 == utils.Dose("XYZ 1μM")
        assert utils.Dose("XYZ 1μM") * 2 == utils.Dose("XYZ 2μM")
        assert utils.Dose("XYZ 3μM") * 4 == utils.Dose("XYZ 12μM")
        assert utils.Dose("XYZ 8μM") * 0.5 == utils.Dose("XYZ 4μM")

        assert utils.Dose("XYZ99/2", conversions={"XYZ99": "XYZ 1μM"}).quantity == 0.5
        assert utils.Dose("2XYZ99", conversions={"XYZ99": "XYZ 1μM"}).quantity == 2
        assert utils.Dose("XYZ99/4", conversions={"XYZ99": "XYZ 16μM"}).quantity == 4
        assert utils.Dose("XYZ99/2", conversions={"XYZ99": "XYZ 16μM"}).quantity == 8
        assert utils.Dose("2XYZ99", conversions={"XYZ99": "XYZ 16μM"}).quantity == 32
        assert utils.Dose("3XYZ99", conversions={"XYZ99": "XYZ 16μM"}).quantity == 48

    def test_ratio(self):
        assert utils.Ratio(1, 2) == utils.Ratio(1, 2)
        assert utils.Ratio(1, 2) == utils.Ratio(2, 4)
        assert utils.Ratio(12.5, 5) == utils.Ratio(25, 10)
        assert utils.Ratio(1, 2) != utils.Ratio(1, 4)
        assert utils.Ratio(1, 2) != utils.Ratio(2, 2)
        assert utils.Ratio(3.3, 10) != utils.Ratio(1, 3)
        assert utils.Ratio(1, 2) == 0.5
        assert utils.Ratio(3, 1) == 3

        assert utils.equalsish(float(utils.Ratio(5, 20)), 0.25)
        assert utils.equalsish(float(utils.Ratio(6, 10)), 0.6)
        assert utils.equalsish(float(utils.Ratio(11, 5)), 2.2)

        assert utils.Ratio(1, 4) * utils.Ratio(4, 1) == 1
        assert utils.Ratio(1, 4) * utils.Ratio(4, 1) == utils.Ratio(1, 1)
        assert 3 * utils.Ratio(4, 1) == 12
        assert 2 * utils.Ratio(3, 2) == 3
        assert utils.Ratio(4, 1) * 3 == 12
        assert utils.Ratio(3, 2) * 2 == 3
        assert utils.equalsish(utils.Ratio(12.5, 5) * 5, 12.5)
        assert utils.equalsish(5 * utils.Ratio(12.5, 5), 12.5)

        assert utils.Ratio(1, 2).reciprocal() == utils.Ratio(2, 1)
        assert utils.Ratio(7, 3).reciprocal() == utils.Ratio(3, 7)

        assert 2 / utils.Ratio(1, 2) == 4
        assert 5 / utils.Ratio(5, 2) == 2
        assert 4 / utils.Ratio(8, 1) == 0.5

        assert utils.Ratio(1, 9).to_proportion() == utils.Ratio(1, 10)
        assert utils.Ratio(5, 4).to_proportion() == utils.Ratio(5, 9)

        assert utils.Dose("XYZ 1μM") * utils.Ratio(7, 2) == utils.Dose("XYZ 3.5μM")
        assert utils.Dose("XYZ 6μM") * utils.Ratio(2, 3) == utils.Dose("XYZ 4μM")
        assert utils.Dose("XYZ 32μM") / utils.Ratio(2, 3) == utils.Dose("XYZ 48μM")
        assert utils.Dose("XYZ 12μM") / utils.Ratio(4, 1) == utils.Dose("XYZ 3μM")

    def test_solution(self):
        assert utils.Solution("XYZ 1μM") == utils.Solution("XYZ 1μM")
        assert utils.Solution("ABC 10μg/mL") == utils.Solution("ABC 10μg/mL")
        assert utils.Solution("XYZ 1μM") != utils.Solution("XYZ 1μg/mL")
        assert utils.Solution("XYZ 1μM") != utils.Solution("XYZ 10μM")
        assert utils.Solution("XYZ 1μM") != utils.Solution("ABC 1μM")
        assert utils.Solution(
            "XYZ99", conversions={"XYZ99": "XYZ 1μM"}
        ) == utils.Solution("XYZ 1μM")
        assert utils.Solution("XYZ 1μM + ABC 10μg/mL") == utils.Solution(
            "XYZ 1μM + ABC 10μg/mL"
        )
        assert utils.Solution("XYZ 1μM + ABC 10μg/mL") == utils.Solution(
            "XYZ99 + ABC 10μg/mL", conversions={"XYZ99": "XYZ 1μM"}
        )
        assert utils.Solution("XYZ 1μM").doses[0] == utils.Dose("XYZ 1μM")
        assert utils.Solution("XYZ 1μM + ABC 10μg/mL").doses == [
            utils.Dose("XYZ 1μM"),
            utils.Dose("ABC 10μg/mL"),
        ]

        assert float(utils.Solution("XYZ 1μM + ABC 10μg/mL")) == 11

        assert utils.Solution("XYZ 10μM") > utils.Solution("XYZ 2μM")

        assert utils.Solution("XYZ 1μM") * 2 == utils.Solution("XYZ 2μM")
        assert utils.Solution("XYZ 10μM") * 0.5 == utils.Solution("XYZ 5μM")

        assert 2 * utils.Solution("XYZ 1μM") == 2
        assert 3 * utils.Solution("XYZ 1μM + ABC 10μg/mL") == 33

        assert utils.Solution("XYZ 10μM") / 2 == 5
        assert utils.Solution("XYZ 32μM") / 4 == 8

        assert utils.Solution("XYZ 1μM").combine_doses(
            utils.Solution("ABC 10μg/mL")
        ) == utils.Solution("XYZ 1μM + ABC 10μg/mL")
        assert utils.Solution("XYZ 1μM").combine_doses(
            utils.Solution("ABC 10μg/mL")
        ).doses == [utils.Dose("XYZ 1μM"), utils.Dose("ABC 10μg/mL")]

        assert utils.Solution("XYZ 10μM").dilute(0.5) == utils.Solution("XYZ 5μM")
        assert utils.Solution("XYZ 20μM").dilute(0.2) == utils.Solution("XYZ 4μM")

        assert utils.Solution("XYZ 10μM").get_cocktail() == utils.Cocktail("XYZ")
        assert utils.Solution("XYZ 1μM + ABC 10μg/mL").get_cocktail() == utils.Cocktail(
            ("XYZ", "ABC"), ratio=utils.Ratio(1, 10)
        )


if __name__ == "__main__":
    unittest.main()
