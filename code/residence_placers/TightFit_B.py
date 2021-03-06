from time import sleep

from districtobjects.Bungalow import Bungalow
from districtobjects.FamilyHome import FamilyHome
from districtobjects.Mansion import Mansion


# a modified evolver, returns first valid solution it finds


class TightFit_B(object):
    name = "TightFit_B"
    expects = ['Waterbodies', "Playgrounds"]
    puts = ["Residences"]

    def getPlan(self):
        return self.plan.deepCopy()

    @staticmethod
    def determine_goal(plan, r):

        if isinstance(r, Bungalow):
            return plan.NUMBER_OF_HOUSES * plan.MINIMUM_BUNGALOW_PERCENTAGE
        elif isinstance(r, Mansion):
            return plan.NUMBER_OF_HOUSES * plan.MINIMUM_MANSION_PERCENTAGE
        elif isinstance(r, FamilyHome):
            return plan.NUMBER_OF_HOUSES * plan.MINIMUM_FAMILYHOMES_PERCENTAGE

    @staticmethod
    def translate(plan, clearance, h, w, x, y, k):
        res = [clearance + x *
               (w + clearance), clearance + y * (h + clearance)]
        if k == 1:
            res[0] = plan.width - res[0]
        elif k == 2:
            res[1] = plan.height - res[1]
        return res

    def coords(self, plan, rt, factor, t, frame, slow):

        r = rt(0, 0)
        c = r.minimumClearance * factor
        h = r.height
        w = r.width
        goal = self.determine_goal(plan, r)
        x_init = 0

        placed_houses = 0

        while placed_houses < goal:
            x_init += 1
            y = -1
            x = x_init
            cur_x = self.translate(plan, c, h, w, x - 1, 0, t)[0]
            if cur_x > plan.width or cur_x < 0:
                return plan
            while x > 0 and placed_houses < goal:
                x -= 1
                y += 1
                res = self.translate(plan, c, h, w, x, y, t)
                house = rt(res[0], res[1])
                if plan.correctlyPlaced(house):
                    plan.addResidence(house)
                    placed_houses += 1
                    if frame is not None:
                        frame.repaint(plan)
                        if slow:
                            sleep(0.1)
        return plan

    def develop_ground_plan(self, plan, i, j, k, frame, slow):
        try:
            plan = self.coords(plan, FamilyHome, i, 0, frame, slow)
            plan = self.coords(plan, Bungalow, j, 1, frame, slow)
            plan = self.coords(plan, Mansion, k, 2, frame, slow)
            return plan
        except Exception:
            return plan

    def __init__(self, plan, i, j, k, frame=None, slow=False):

        self.factors = [i, j, k]
        self.plan = self.develop_ground_plan(plan.deepCopy(), i, j, k, frame, slow).deepCopy()
        # frame.repaint(self.plan)
