import os
import pathlib
import sys
import pytest

# When running locally the environment variable PYPWS_RUN_LOCALLY needs to be set to True.
# Check if the environment variable is set
PYPWS_RUN_LOCALLY = os.getenv('PYPWS_RUN_LOCALLY')
if PYPWS_RUN_LOCALLY and PYPWS_RUN_LOCALLY.lower() == 'true':
    # Navigate to the PYPWS directory by searching upwards until it is found.
    current_dir = pathlib.Path(__file__).resolve()

    while current_dir.name.lower() != 'package':
        if current_dir.parent == current_dir:  # Check if the current directory is the root directory
            raise FileNotFoundError("The 'pypws' directory was not found in the path hierarchy.")
        current_dir = current_dir.parent

    # Insert the path to the pypws package into sys.path.
    sys.path.insert(0, f'{current_dir}')


# from pypws.calculations import UDSTemperatureLimitsCalculation
from pypws.entities import Material, MaterialComponent
from pypws.enums import Phase, ResultCode

@pytest.mark.skip(reason="Skipping this test unconditionally")
def test_case_141():
    
    """
    Test for UDS temperature limits calculation with the following inputs
    
    Material = "PROPANE"
    Phase = "lIQUID"
    
    """
    
    # Define the material
    material = Material(
		name="PROPANE",
		components=[
			MaterialComponent(
				name="PROPANE",
				mole_fraction=1.0
			)
		]
	)
    
    # Define the phase
    phase = Phase.LIQUID
    
    # Create a uds temperature limits calculation.
    uds_temperature_limits_calculation = UDSTemperatureLimitsCalculation(material = material, phase_to_be_released = phase)
    
    # Run the calculation
    print ('Running uds_temperature_limits_calculation')
    result_code = uds_temperature_limits_calculation.run()
    
    # Print any messages.
    if len(uds_temperature_limits_calculation.messages) > 0:
        print('Messages:')
        for message in uds_temperature_limits_calculation.messages:
            print(message)

    if result_code == ResultCode.SUCCESS:
        print(f'SUCCESS: uds_temperature_limits_calculation ({uds_temperature_limits_calculation.calculation_elapsed_time}ms)')
    else:
        assert False, f'FAILED uds_temperature_limits_calculation with result code {result_code}'