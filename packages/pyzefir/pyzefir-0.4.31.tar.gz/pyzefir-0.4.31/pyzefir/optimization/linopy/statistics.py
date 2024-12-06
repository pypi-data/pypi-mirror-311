import pandas as pd
from linopy import Model



class Statistics:
    def __init__(self, model: Model):
        self.model = model

    def dump(self):
        self.get_coefficeints_range()
        self.get_objective()

    def get_coefficeints_range(self):
        coefficients_df = self.model.constraints.coefficientrange
        rhs_df = pd.DataFrame.from_dict(
            {constr_name:
                {"min": constr.rhs.min().item(),
                 "max": constr.rhs.max().item()}
            for constr_name, constr in self.model.constraints.items()
            }, orient="index")
        df = pd.concat([coefficients_df, rhs_df], axis=1,
                       keys=["coefficients", "RHS"])
        df.to_excel("range.xlsx")

    def get_objective(self):
        print('obj')