"""Main module."""
# import dependencies

from pyomo.environ import ConcreteModel, Set, Var, Objective, minimize, maximize, Constraint, Reals,PositiveReals
import numpy as np
import pandas as pd
from .constant import CET_ADDI, ORIENT_IO, ORIENT_OO,ORIENT_UO,ORIENT_HYPERYX, RTS_VRS, RTS_CRS, OPT_DEFAULT, OPT_LOCAL
from .utils import tools
import ast

class HYPERt:
    """Data Envelopment Analysis (DEA)
    """
    def __init__(self, data,sent = "inputvar=outputvar",  \
                 orient=ORIENT_HYPERYX, rts=RTS_VRS, baseindex=None,refindex=None):
        """DEA: Directional distance function

        Args:
            data (pandas.DataFrame): input pandas.
            sent (str): inputvars=outputvars[: unoutputvars]. e.g.: "K L CO2= Y"
            orient(str): ORIENT_HYPERYX , or choose some variables in sent,eg:L=Y, CO2=Y
            rts (String): RTS_VRS (variable returns to scale) or RTS_CRS (constant returns to scale)
            baseindex (String, optional): estimate index. Defaults to None. e.g.: "Year=[2010]"
            refindex (String, optional): reference index. Defaults to None. e.g.: "Year=[2010]"
        """
        # Initialize DEA model

        self.rts = rts
        self.outputvars, self.inputvars ,self.y, self.x,self.yref, self.xref= \
            tools.assert_valid_deat(sent,data,baseindex,refindex )


        self.xcol = self.x.columns
        print("sss",self.xcol)
        self.ycol = self.y.columns
        if orient in [ORIENT_HYPERYX]:
            self.orient = orient
            self.xindexs = None
            self.yindexs = None
        else:
            self.orient = None
            if '=' in orient:
                xorient = orient.split('=')[0].strip(' ').split(' ')
                yorient = orient.split('=')[1].strip(' ').split(' ')

                ltx = [1 if _ in xorient else 0 for _ in self.xcol]
                lty = [1 if _ in yorient else 0 for _ in self.ycol]
                self.xindexs = [i for i, x in enumerate(ltx) if x == 1]
                self.yindexs = [i for i, x in enumerate(lty) if x == 1]
                print(self.xindexs)

            else:
                raise ValueError(
                    "You need to use '=' to specify y and x orientation.")


        # print(self.xcol)

        self.I = self.x.index          ## I 是 被评价决策单元的索引      ## 当前被评价决策单元的序号 self.x[I0]
        self.__modeldict = {}

        for i in self.I:
            self.I0 = i
            self.__model__ = ConcreteModel()

            self.__model__.I2 = Set(initialize=  self.xref.index)       ## I2 是 参考决策单元的数量

            self.__model__.K = Set(initialize=range(len(self.x.iloc[0])))   ## K 是投入个数
            self.__model__.L = Set(initialize=range(len(self.y.iloc[0])))   ## L 是产出个数 被评价单元和参考单元的K，L一样

            # Initialize variable
            self.__model__.theta = Var(Set(initialize=range(1)),bounds=(0, 1), doc='theta')
            self.__model__.theta2 = Var(Set(initialize=range(1)),bounds=(0, 1), \
                                       doc='theta^2')

            self.__model__.lamda = Var(self.__model__.I2, bounds=(0.0, None), doc='intensity variables')

            # Setup the objective function and constraints
            self.__model__.objective = Objective(
                rule=self.__objective_rule(), sense=minimize, doc='objective function')

            self.__model__.input = Constraint(
                self.__model__.K, rule=self.__input_rule(), doc='input constraint')
            self.__model__.output = Constraint(
                self.__model__.L, rule=self.__output_rule(), doc='output constraint')


            if self.rts == RTS_VRS:
                self.__model__.vrs = Constraint(
                     rule=self.__vrs_rule(), doc='various return to scale rule')

            self.__modeldict[i] = self.__model__

            # self.__model__.objective.pprint()
            # self.__model__.input.pprint()
            # self.__model__.output.pprint()
            # self.__model__.vrs.pprint()


        # # Optimize model


    def __objective_rule(self):
        """Return the proper objective function"""

        def objective_rule(model):
            return model.theta2[0]*1  + sum(model.lamda[i2] *0 for i2 in model.I2)
        return objective_rule


    def __input_rule(self):
        """Return the proper input constraint"""

        if (self.orient == ORIENT_HYPERYX) :
            def input_rule(model, k):
                return sum(model.lamda[i2] * self.xref.loc[i2,self.xcol[k]] for i2 in model.I2) <= \
                    model.theta2 * self.x.loc[self.I0,self.xcol[k]]

        else:
            if type(self.xindexs) != type(None):
                def input_rule(model, k):
                    if k not in self.xindexs:
                        return Constraint.Skip
                    return sum(model.lamda[i2] * self.xref.loc[i2,self.xcol[k]] for i2 in model.I2) <= \
                        model.theta2 * self.x.loc[self.I0,self.xcol[k]]
            else:
                raise ValueError(
                    "You need to use '=' to specify y and x orientation.")
        return input_rule

    def __output_rule(self):
        """Return the proper output constraint"""
        def output_rule(model, l):
            return sum(model.lamda[i2] * self.yref.loc[i2,self.ycol[l]] for i2 in model.I2) \
                >= self.y.loc[self.I0,self.ycol[l]]
        return output_rule

    def __vrs_rule(self):

        def vrs_rule(model):
            return sum(model.lamda[i2] for i2 in model.I2) == model.theta[0] * 1
        return vrs_rule

    def optimize(self,  solver=OPT_DEFAULT):
        """Optimize the function by requested method

        Args:
            solver (string): The solver chosen for optimization. It will optimize with default solver if OPT_DEFAULT is given.
        """
        # TODO(error/warning handling): Check problem status after optimization
        data2 = pd.DataFrame()
        for ind, problem in self.__modeldict.items():
            _, data2.loc[ind,"optimization_status"] = tools.optimize_model2(problem, ind, solver)
            data2.loc[ind, "theta2"] = np.asarray(list(problem.theta2[:].value))
            data2.loc[ind, "theta"] = np.sqrt(np.asarray(list(problem.theta2[:].value)))

        return data2

    def info(self, dmu = "all"):
        """Show the infomation of the lp model

        Args:
            dmu (string): The solver chosen for optimization. Default is "all".
        """
        if dmu =="all":
            for ind, problem in self.__modeldict.items():
                print(ind,"\n",problem.pprint())

        print(self.__modeldict[int(dmu)].pprint())


