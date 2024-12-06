# Imports
# Standard Library Imports
import pathlib
import unittest

# External Imports
from pepitatools.configuration import set_config_setting

# Local Imports
from pepitatools import dose_response, utils


class TestDoseResponse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log_dir = pathlib.Path(__file__).parent / "tmp_logs"
        cls.log_dir.mkdir(exist_ok=True)
        set_config_setting("log_dir", str(cls.log_dir))

    @classmethod
    def tearDownClass(cls):
        for f in cls.log_dir.glob("*"):
            if f.name == "dose_response":
                for sub_f in f.glob("*"):
                    sub_f.unlink()
                f.rmdir()
                continue
            f.unlink()
        cls.log_dir.rmdir()

    def test_do_additive_isobole(self):
        self.assertTrue(
            utils.equalsish(
                0.46255,
                dose_response.do_additive_isobole(
                    a_i=25,
                    A_E50_a=65.8,
                    B_E50_b=3.99,
                    E_max_a=1.58,
                    E_max_b=4.17,
                    B_i=1.2,
                    p=1.73,
                    q=1.92,
                ),
            )
        )
        self.assertTrue(
            utils.equalsish(
                2.06255,
                dose_response.do_additive_isobole(
                    a_i=25,
                    A_E50_a=65.8,
                    B_E50_b=3.99,
                    E_max_a=1.58,
                    E_max_b=4.17,
                    B_i=2.8,
                    p=1.73,
                    q=1.92,
                ),
            )
        )

        self.assertTrue(
            utils.equalsish(
                4.46255,
                dose_response.do_additive_isobole(
                    a_i=25,
                    A_E50_a=65.8,
                    B_E50_b=3.99,
                    E_max_a=1.58,
                    E_max_b=4.17,
                    B_i=5.2,
                    p=1.73,
                    q=1.92,
                ),
            )
        )

        self.assertTrue(
            utils.equalsish(
                0.60894,
                dose_response.do_additive_isobole(
                    a_i=100,
                    A_E50_a=65.8,
                    B_E50_b=3.99,
                    E_max_a=1.58,
                    E_max_b=4.17,
                    B_i=2.8,
                    p=1.73,
                    q=1.92,
                ),
            )
        )

        self.assertTrue(
            utils.equalsish(
                3.00894,
                dose_response.do_additive_isobole(
                    a_i=100,
                    A_E50_a=65.8,
                    B_E50_b=3.99,
                    E_max_a=1.58,
                    E_max_b=4.17,
                    B_i=5.2,
                    p=1.73,
                    q=1.92,
                ),
            )
        )

        self.assertTrue(
            utils.equalsish(
                2.28538,
                dose_response.do_additive_isobole(
                    a_i=400,
                    A_E50_a=65.8,
                    B_E50_b=3.99,
                    E_max_a=1.58,
                    E_max_b=4.17,
                    B_i=5.2,
                    p=1.73,
                    q=1.92,
                ),
            )
        )

    def test_do_fic(self):
        self.assertTrue(
            utils.equalsish(
                1,
                dose_response.do_FIC(
                    a_i=25,
                    b_i=0.46255,
                    A_E50_a=65.8,
                    B_E50_b=3.99,
                    E_max_a=1.58,
                    E_max_b=4.17,
                    B_i=1.2,
                    p=1.73,
                    q=1.92,
                ),
            )
        )

        self.assertTrue(
            utils.equalsish(
                1,
                dose_response.do_FIC(
                    a_i=25,
                    b_i=2.06255,
                    A_E50_a=65.8,
                    B_E50_b=3.99,
                    E_max_a=1.58,
                    E_max_b=4.17,
                    B_i=2.8,
                    p=1.73,
                    q=1.92,
                ),
            )
        )

        self.assertTrue(
            utils.equalsish(
                1,
                dose_response.do_FIC(
                    a_i=25,
                    b_i=4.46255,
                    A_E50_a=65.8,
                    B_E50_b=3.99,
                    E_max_a=1.58,
                    E_max_b=4.17,
                    B_i=5.2,
                    p=1.73,
                    q=1.92,
                ),
            )
        )

        self.assertTrue(
            utils.equalsish(
                1,
                dose_response.do_FIC(
                    a_i=100,
                    b_i=0.60894,
                    A_E50_a=65.8,
                    B_E50_b=3.99,
                    E_max_a=1.58,
                    E_max_b=4.17,
                    B_i=2.8,
                    p=1.73,
                    q=1.92,
                ),
            )
        )

        self.assertTrue(
            utils.equalsish(
                1,
                dose_response.do_FIC(
                    a_i=100,
                    b_i=3.00894,
                    A_E50_a=65.8,
                    B_E50_b=3.99,
                    E_max_a=1.58,
                    E_max_b=4.17,
                    B_i=5.2,
                    p=1.73,
                    q=1.92,
                ),
            )
        )

        self.assertTrue(
            utils.equalsish(
                1,
                dose_response.do_FIC(
                    a_i=400,
                    b_i=2.28538,
                    A_E50_a=65.8,
                    B_E50_b=3.99,
                    E_max_a=1.58,
                    E_max_b=4.17,
                    B_i=5.2,
                    p=1.73,
                    q=1.92,
                ),
            )
        )

    def test_filter_valid(self):
        self.assertListEqual(
            dose_response.filter_valid([1, 1, 2, 3, 5, 8], minimum=3), [3, 5, 8]
        )
        self.assertListEqual(
            dose_response.filter_valid([1, 1, 2, 3, 5, 8], tolerance=2), [1, 3, 5, 8]
        )
        self.assertListEqual(
            dose_response.filter_valid([1, 1, 2, 3, 5, 8], tolerance=3), [1, 5, 8]
        )
        self.assertListEqual(
            dose_response.filter_valid([1, 1, 2, 3, 5, 8], minimum=3, tolerance=3),
            [
                3,
                8,
            ],
        )

    def test_model(self):
        model = dose_response._get_neo_model()
        self.assertLess(model.effective_concentration(0.001), 1)
        self.assertLess(model.get_absolute_E_max(), 50)
        self.assertLess(model.get_condition_E_max(), 50)
        self.assertTrue(utils.equalsish(1, model.get_pct_survival(xs=0.001)))
        self.assertTrue(
            utils.equalsish(0.0, model.get_pct_survival(xs=2000), delta=0.03)
        )  # THIS TEST IS CHANGED
        self.assertEqual(model.get_pct_survival(ys=100), 1)
        self.assertLessEqual(model.get_pct_survival(ys=0.001), 0)
        self.assertTrue(
            utils.equalsish(0, model.get_pct_survival(ys=model.get_absolute_E_max()))
        )
        self.assertEqual(model.get_x_units(), "μM")
        self.assertGreater(model.get_ys(0.001), 99)
        self.assertLess(model.get_ys(2000), 50)


if __name__ == "__main__":
    unittest.main()
