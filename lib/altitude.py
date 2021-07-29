#Method that calculates altitude based on given pressure in Pa

def altitude_from_pressure(pressure):
    """Returns altitude in meters with pressure input in Pascal"""

    P_SL = 101325 # Pascal
    T_SL = 15 + 273.15 #K
    L = -0.0065 # [K/m]
    h_SL = 0 #m
    R = 8.31432 #Nm/molK
    g = 9.80665 #m/s^2
    M = 0.0289644 #kg/mol

    h = h_SL + (T_SL/L)*((pressure/P_SL)**((-R*L)/(g*M))-1)
    return h