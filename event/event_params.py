from common_utils import Point

# Inner:------------------------------------------------------
INNER_PARAM_MASS = "param_mass"
def mass_function(zmeyka):
    return len(zmeyka)


# Outer:------------------------------------------------------
OUTER_PARAM_DU = "outer_param_du"
def du_function(du_point):
    return du_point.norm()

OUTER_PARAM_DX = "outer_param_du"
def dx_function(du_point):
    return du_point.x




