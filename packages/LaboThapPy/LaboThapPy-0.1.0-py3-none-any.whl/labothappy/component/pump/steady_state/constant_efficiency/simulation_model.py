from component.base_component import BaseComponent
from connector.mass_connector import MassConnector
from connector.work_connector import WorkConnector
from connector.heat_connector import HeatConnector

from CoolProp.CoolProp import PropsSI

class PumpCstEff(BaseComponent):
    """
    Component: Pump

    Model: Constant efficiency

    **Descritpion**:

        This model determines the exhaust specific enthalpy and the exhaust temperature of a pump. This model can be used for on-design models of systems.

    **Assumptions**:

        - Steady-state operation.
        - Efficiency stays constant for all the conditions.

    **Connectors**:

        su (MassConnector): Mass connector for the suction side.

        ex (MassConnector): Mass connector for the exhaust side.

    **Parameters**:

        eta_is: Isentropic efficiency. [-]

    **Inputs**:

        su_p: Suction side pressure. [Pa]

        su_T: Suction side temperature. [K]

        ex_p: Exhaust side pressure. [Pa]

        su_fluid: Suction side fluid. [-]

    **Ouputs**:

        ex_h: Exhaust side specific enthalpy. [J/kg] 

        ex_T: Exhaust side temperature. [K]
    """

    def __init__(self):
        super().__init__()
        self.su = MassConnector()
        self.ex = MassConnector()
        self.W_pp = WorkConnector()

    def get_required_inputs(self): # Used in check_calculablle to see if all of the required inputs are set
        self.sync_inputs()
        # Return a list of required inputs
        return ['su_p', 'su_T', 'ex_p', 'su_fluid']
    
    def sync_inputs(self):
        """Synchronize the inputs dictionary with the connector states."""
        if self.su.fluid is not None:
            self.inputs['su_fluid'] = self.su.fluid
        if self.su.T is not None:
            self.inputs['su_T'] = self.su.T
        elif self.su.h is not None:
            self.inputs['su_h'] = self.su.h
        if self.su.p is not None:
            self.inputs['su_p'] = self.su.p
        if self.ex.p is not None:
            self.inputs['ex_p'] = self.ex.p

    def set_inputs(self, **kwargs):
        """Set inputs directly through a dictionary and update connector properties."""
        self.inputs.update(kwargs) # This line merges the keyword arguments ('kwargs') passed to the 'set_inputs()' method into the eisting 'self.inputs' dictionary.

        # Update the connectors based on the new inputs
        if 'su_fluid' in self.inputs:
            self.su.set_fluid(self.inputs['su_fluid'])
        if 'su_T' in self.inputs:
            self.su.set_T(self.inputs['su_T'])
        elif 'su_h' in self.inputs:
            self.su.set_h(self.inputs['su_h'])
        if 'su_p' in self.inputs:
            self.su.set_p(self.inputs['su_p'])
        if 'ex_p' in self.inputs:
            self.ex.set_p(self.inputs['ex_p'])

    def get_required_parameters(self):
        return ['eta_is']

    def print_setup(self):
        print("=== Pump Setup ===")
        print("Connectors:")
        print(f"  - su: fluid={self.su.fluid}, T={self.su.T}, p={self.su.p}, m_dot={self.su.m_dot}")
        print(f"  - ex: fluid={self.ex.fluid}, T={self.ex.T}, p={self.ex.p}, m_dot={self.ex.m_dot}")

        print("\nInputs:")
        for input_name in self.get_required_inputs():
            if input_name in self.input_values:
                print(f"  - {input_name}: {self.input_values[input_name]}")
            else:
                print(f"  - {input_name}: Not set")

        print("\nParameters:")
        for param in self.get_required_parameters():
            if param in self.params:
                print(f"  - {param}: {self.params[param]}")
            else:
                print(f"  - {param}: Not set")
        print("======================")

    def solve(self):
        # Perform checks to ensure the model can be calculated and has parameters
        self.check_calculable()
        self.check_parametrized()

        if not (self.calculable and self.parametrized):
            self.solved = False
            return

        try:
            """PUMP MODEL"""
            # Calculate the outlet enthalpy based on isentropic efficiency
            h_ex_is = PropsSI('H', 'P', self.ex.p, 'S', self.su.s, self.su.fluid)
            h_ex = self.su.h + (h_ex_is - self.su.h) * self.params['eta_is']
            w_pp = h_ex - self.su.h
            W_dot_pp = self.su.m_dot*w_pp

            """Update connectors after the calculations"""
            self.update_connectors(h_ex, w_pp, W_dot_pp)

            # Mark the model as solved if successful
            self.solved = True
        except Exception as e:
            # Handle any errors that occur during solving
            self.solved = False
            print(f"Convergence problem in pump model: {e}")

        
    def update_connectors(self, h_ex, w_pp, W_dot_pp):
        """Update the connectors with the calculated values."""
        self.ex.set_h(h_ex)
        self.ex.set_fluid(self.su.fluid)
        self.ex.set_m_dot(self.su.m_dot)
        self.W_pp.set_W_dot(W_dot_pp)

    def print_results(self):
        print("=== Pump Results ===")
        print(f"  - h_ex: {self.ex.h} [J/kg]")
        print(f"  - T_ex: {self.ex.T} [K]")
        print(f"  - W_dot_pp: {self.W_pp.W_dot} [W]")
        print("=========================")

    def print_states_connectors(self):
        print("=== Pump States ===")
        print("Mass connectors:")
        print(f"  - su: fluid={self.su.fluid}, T={self.su.T} [K], p={self.su.p} [Pa], h={self.su.h} [J/kg], s={self.su.s} [J/K.kg], m_dot={self.su.m_dot} [kg/s]")
        print(f"  - ex: fluid={self.ex.fluid}, T={self.ex.T} [K], p={self.ex.p} [Pa], h={self.ex.h} [J/kg], s={self.ex.s} [J/K.kg], m_dot={self.ex.m_dot} [kg/s]")
        print("=========================")
        print("Work connector:")
        print(f"  - W_dot_pp: {self.W_pp.W_dot} [W]")
        print("=========================")
