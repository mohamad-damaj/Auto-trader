from xgboost import XGBClassifier 

class trading_model():
    def __init__(self):
        self.model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    

    def load(self, path: str):
        """
        Load a saved model.
        """
        self.model.load_model(path)
    
    

