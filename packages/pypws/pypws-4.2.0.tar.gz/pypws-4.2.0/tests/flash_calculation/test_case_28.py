import os
import pathlib
import sys

# When running locally the environment variable PYPWS_RUN_LOCALLY needs to be set to True.
# Check if the environment variable is set
if os.getenv('PYPWS_RUN_LOCALLY') != None and os.getenv('PYPWS_RUN_LOCALLY').lower() == 'true':
    # Navigate to the PYPWS directory by searching upwards until it is found.
    current_dir = pathlib.Path(__file__).resolve()

    while current_dir.name.lower() != 'package':
        current_dir = current_dir.parent

    # Insert the path to the pypws package into sys.path.
    sys.path.insert(0, f'{current_dir}')

from pypws.calculations import FlashCalculation
from pypws.entities import Material, MaterialComponent, State
from pypws.enums import ResultCode

"""
This sample demonstrates how to use the flash calculation along with with the dependent entities.
"""

def test_case_28():

    # Set the case properties.
    state_temperature = 350.0
    state_pressure = 2.0E+05
    state_liquid_fraction = 0.7

    # Define the initial state of the vessel.
    state = State(temperature = state_temperature, pressure = state_pressure, liquid_fraction = state_liquid_fraction)

    # Define the material.
    # N-DECANE+N-UNDECANE+WATER
    material = Material('Case28_Material', [MaterialComponent('N-DECANE', 0.333), MaterialComponent('N-UNDECANE', 0.333), MaterialComponent('WATER', 0.334)], component_count = 3)

    # Create a flash calculation using the material and state.
    flash_calculation = FlashCalculation(material, state)

    # Run the flash calculation.
    print('Running flash_calculation...')
    resultCode = flash_calculation.run()

    # Print any messages.
    if len(flash_calculation.messages) > 0:
        print('Messages:')
        for message in flash_calculation.messages:
            print(message)

    if resultCode == ResultCode.SUCCESS:
        print(f'SUCCESS: flash_calculation ({flash_calculation.calculation_elapsed_time}ms)')
    else:
        assert False, f'FAILED flash_calculation with result code {resultCode}'
