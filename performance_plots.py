import matplotlib.pyplot as plt  
import numpy as np
    
    
def main():
     
    Aircraft_Classes  = ['commuter', 'regional', 'short_range']
    Max_Power         = [ 10000, 10000 ,10000  ] # need to update
    L_D_aircraft      = [15, 16, 17]
    Aircraft_Weight   = [0,0,0 ]
    Structural_Weight = [0,0,0 ] 
    Passenger_Weight  = [0,0,0 ]
    Crew_Weight       = [0,0,0 ]
    Payload_Weight    = [0,0,0 ]
    
    
    n_A              = len(Aircraft_Classes) 
    n_sims           = 10000
    hybridization    = 1.0
    
    Range                 = np.zeros(n_sims)
    Pack_Energy           = np.zeros(n_sims) 
    Energy_Pack_Mass      = np.zeros(n_sims)
    Power_Conversion_Mass = np.zeros(n_sims)
    System_Voltage       = np.zeros(n_sims)
    
    for ac in range(n_A): 
        # ---------------------Aircraft ------------------------  
        P_aircraft          = Max_Power[ac] * hybridization
        eta_em              = np.random.normal(loc=0.95, scale=0.05) 
        eta_p               = 0
        LD                  = np.random.normal(loc = L_D_aircraft[ac], scale = 1) 
        M_struct            = Structural_Weight[ac]
        M_pass              = Passenger_Weight[ac]
        M_crew              = Crew_Weight[ac]
        M_payload           = Payload_Weight[ac]  
        eta_propulsion      = np.random.normal(loc=0.86, scale=0.02) 
        
        # ------------------- Energy Storage -------------------    
        n_p                 = 210   # number of cells in parallel 
        n_s                 = 120   # number of cells in series 
        M_cell              = 0.048 # unit mass of cell
        e_cell              = np.random.normal(loc=3500, scale=100)  # specific energy of battery cell
        Q_cell              = np.random.normal(loc=20, scale=1) 
        V_cell              = np.random.normal(loc=4.2,scape=1)      # voltage of battery cell 
        alpha               = np.random.normal(loc=1.42, scale=0.05) # BMS packaging factor 
        eta_battery         = np.random.normal(loc=0.9, scale=0.02)  
    
        # ---------------------Power Conversion --------------    
        P_motor             = np.random.normal(loc=2000, scale=100)  # should this be P_aircraft? 
        T_torque_density    = np.random.normal(loc=1.5, scale=0.05) 
        omega               = np.random.normal(loc=2500, scale=200) 
        Pd_motor_cooling    = np.random.normal(loc=50, scale=5) 
        eta_motor           = np.random.normal(loc=0.98, scale=0.02) 
        
    
        # -----------------------Inverter-----------------------    
        P_inverter          = np.random.normal(loc=200, scale=5)  # should this be P_aircraft? 
        Pd_inverter         = np.random.normal(loc=50, scale=5) 
        eta_inverter        = np.random.normal(loc=0.9, scale=0.02)  
        Pd_inverter_cooling = np.random.normal(loc=50, scale=5) 
        V                   = 0
        E0                  = 2.51e3 
        r_cond              = np.random.normal(loc=10, scale=0.1) 
        rho                 = 0
        rho_theta_insul     = 0
        L                   = 0
        rho_cond            = 0
        rho_insul           = 0
            
        # ------------------------ Cables ----------------------------    
        theta_a             = np.random.normal(loc=253, scale=20)   # in Kelvin
        I                   = 0
        T_4                 = 0
        D                   = np.random.normal(loc=2000, scale=100) 
        g                   = np.random.normal(loc=9.81, scale=0.01)   
    
        R,E,M_e, M_p , M_c, V_p = compute_performance(n_p, n_s, M_cell, e_cell, alpha, P_motor, T_torque_density, omega, Pd_motor_cooling, eta_motor, 
                P_inverter, Pd_inverter, eta_inverter, eta_propulsion, eta_battery, P_aircraft, Pd_inverter_cooling, V, E0, r_cond, rho, rho_theta_insul, 
                L, rho_cond, rho_insul, eta_em, eta_p, LD, M_struct, M_pass, M_crew, M_payload, theta_a, I, T_4, D, g , Q_cell, V_cell)            
         
        Range[R]
        Pack_Energy[E]
        Energy_Pack_Mass[M_e]
        Power_Conversion_Mass[M_p]
        System_Voltage[V_p]  
        
    plot_results(Range, Aircraft_Weight,  Pack_Energy,Energy_Pack_Mass, Power_Conversion_Mass, System_Voltage)
    
    return         
        
def plot_results(Range, Aircraft_Weight,  Pack_Energy,Energy_Pack_Mass, Power_Conversion_Mass, System_Voltage):
    
    fig =  plt.figure() 
    axis =  fig.add_subplot()
    
    
    return 
    
def compute_performance(n_p, n_s, M_cell, e_cell, alpha, P_motor, T_torque_density, omega, Pd_motor_cooling, eta_motor, 
         P_inverter, Pd_inverter, eta_inverter, eta_propulsion, eta_battery, P_aircraft, Pd_inverter_cooling, V, E0, r_cond, rho, rho_theta_insul, 
         L, rho_cond, rho_insul, eta_em, eta_p, LD, M_struct, M_pass, M_crew, M_payload, theta_a, I, T_4, D, g,Q_cell, V_cell):

    # SECTION I: Electrochemical Energy Storage Systems (Batteries)
    M_energy_storage =  energy_storage(n_p, n_s, M_cell, e_cell, alpha)

    # SECTION II: Electrical Power Conversion Machines
    M_electric_power_conversion =  power_conversion(P_motor, T_torque_density, omega, Pd_motor_cooling, eta_motor, 
        P_inverter, Pd_inverter, eta_inverter, eta_propulsion, eta_battery, P_aircraft, Pd_inverter_cooling)
    
    # SECTION III: Cabling Mass
    M_cable ,  theta_max =  cable_mass(V, E0, r_cond, rho, rho_theta_insul,L, rho_cond, rho_insul, theta_a, I, T_4)

    # SECTION IV: Overall Performance

    # Equation (25): Total Drivetrain Mass (M_drivetrain) is the sum of storage, power conversion, and cabling masses
    M_drivetrain = M_energy_storage + M_electric_power_conversion + M_cable # Equation (25)

    # Equation (24): Total Aircraft Mass (M_0) including masses of structure, passengers, crew, payload, and drivetrain
    M_0 = M_struct + M_pass + M_crew + M_payload + M_drivetrain # Equation (24)

    # Equation (23): Aircraft Range Equation
    Range =  aircraft_flight_range(E_pack,L, eta_em, eta_p, D, g, M_0)
    
    # Equation (27a): Total Battery Pack Charge
    Q_pack = n_p * Q_cell  # Equation (27a)

    # Equation (27b): Total Battery Pack Voltage (V_pack)
    V_pack = n_s* V_cell  # Equation (27b)

    # Equation (26): Total Battery Pack Energy (E_pack), derived from charge and voltage
    E_pack = Q_pack * V_pack # Equation (26)

    return Range, E_pack ,M_energy_storage, M_electric_power_conversion , M_cable, V_pack 

def cable_mass(V, E0, r_cond, rho, rho_theta_insul,L, rho_cond, rho_insul, theta_a, I, T_4):

    # Equation (18): Cable Insulation Radius based on voltage and electric field constraints
    # E0 is the electric field
    r_insul = r_cond * np.exp(V / (E0 * r_cond))  # Equation (18)

    # Equation (20): Conductor Resistance (thermal constraint based on material properties)
    R_prime = rho / (np.pi * r_cond ** 2)  # Equation (20)

    # Equation (21): Thermal Resistance of the insulation
    T_1 = rho_theta_insul / (2 * np.pi) * np.log(r_insul / r_cond)  # Equation (21)

    # Equation (22): Total Cable Mass calculation based on conductor and insulation volume and density
    M_cable = np.pi * L * (r_cond ** 2 * rho_cond + (r_insul ** 2 - r_cond ** 2) * rho_insul)  # Equation (22)

    # Equation (19): Maximum Temperature (conductor temperature based on current, resistance, and thermal resistances)
    theta_max = theta_a + I**2 * R_prime * (T_1 + T_4)  # Equation (19)
    
    return M_cable, theta_max

def energy_storage(n_p, n_s, M_cell, e_cell, alpha):
    
    # Equation (2): Total dry battery mass (higher fidelity for Eq. (1))
    M_pack = M_cell * n_p * n_s  # Equation (2)
    E_pack = e_cell*M_pack

    # Equation (3): Battery Control & Thermal Management System Mass
    M_BMS = (alpha -1 ) * M_pack  # Equation (3)

    # Equation (4): Total Energy Storage Mass
    M_energy_storage = (1 + alpha) * (E_pack / e_cell) * n_p * n_s
    
    return M_energy_storage

def power_conversion(P_motor, T_torque_density, omega, Pd_motor_cooling, eta_motor, 
        P_inverter, Pd_inverter, eta_inverter, eta_propulsion, eta_battery, P_aircraft, Pd_inverter_cooling): 

    # Equation (6): Motor Mass, with motor power calculated based on aircraft power, motor efficiency, and propeller efficiency
    P_motor = P_aircraft / (eta_motor * eta_propulsion)
    M_motor = P_motor / (T_torque_density * omega)  # Equation (6)

    # Equation (7) or (9): Motor Cooling System Mass (using higher fidelity if needed)
    P_inverter = P_aircraft / (eta_inverter * eta_motor * eta_propulsion)  # Derived power of the inverter based on efficiencies
    M_motor_cooling = P_inverter * (1 - eta_motor) / Pd_motor_cooling  # Equation (7) or Equation (9) as per fidelity

    # Equation (10): Inverter Mass
    M_inverter = P_inverter / Pd_inverter  # Equation (10)
    # Alternative: M_inverter = (k_1 / f_s) + k_2 * f_s * V**2 for different fidelity level (Eq. (13))

    # Equation (11) or (12): Inverter Cooling System Mass (using higher fidelity if needed)
    P_battery = P_aircraft / (eta_battery * eta_inverter * eta_motor * eta_propulsion)  # Battery power derived based on efficiencies
    M_inverter_cooling = P_battery * (1 - eta_inverter) / Pd_inverter_cooling  # Equation (11) or Equation (12)

    # Equation (15): Total Motor Drive Mass
    M_total_motor_drive = M_motor + M_motor_cooling + M_inverter + M_inverter_cooling  # Equation (15)

    # Equation (16): Electric Power Conversion Mass (using detailed formula for high fidelity)
    M_electric_power_conversion = (P_aircraft / (eta_motor * eta_propulsion)) * ((1 / T_torque_density) + ((1-eta_motor) / (eta_inverter * Pd_motor_cooling)) + (1 / (eta_inverter * Pd_inverter)) + ((1 - eta_inverter) / (eta_battery * eta_inverter * Pd_inverter_cooling)))  # Equation (16)

    return M_electric_power_conversion

def aircraft_flight_range(E_pack,L, eta_em, eta_p, D, g, M_0):
    R = eta_em * eta_p * (L/D) * E_pack / (g * M_0)  # Equation (23)
    return R 

if __name__ == '__main__':
    main() 
    plt.show()    