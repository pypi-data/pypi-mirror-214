import unittest

from autotraino.gluon import AutogluonTrainer
from datasets import load_dataset


class TestPlayground(unittest.TestCase):
    def test_playground(self):
        d = load_dataset("mstz/adult", "income")["train"].to_pandas()

        # train the model
        trainer = AutogluonTrainer(save_path="./test_save")
        trainer = trainer.fit(d, target_feature="over_threshold", time_limit=100)

        trainer.predict(d)
        trainer.predict_proba(d)

        print(trainer.names)
        print(trainer.is_fit)
        print(trainer.target_feature)
        print(trainer[trainer.names[0]])


if __name__ == "main":
    unittest.main()
