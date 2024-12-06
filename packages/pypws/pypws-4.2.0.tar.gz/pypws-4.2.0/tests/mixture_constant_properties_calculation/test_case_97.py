import os
import pathlib
import sys

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


from pypws.calculations import MixtureConstantPropertiesCalculation
from pypws.entities import Material, MaterialComponent, State
from pypws.enums import ResultCode


def test_case_97():

    # Set the material
    material = Material("NATURAL GAS", [MaterialComponent("METHANE", 0.85), MaterialComponent("ETHANE", 0.1), MaterialComponent("PROPANE", 0.05)], component_count = 3)

    # Create a mixture constant properties calculation using the material.
    mixture_constant_properties_calculation = MixtureConstantPropertiesCalculation(material)

    # Run the calculation
    print('Running mixture_constant_properties_calculation...')
    resultCode = mixture_constant_properties_calculation.run()

    # Print any messages.
    if len(mixture_constant_properties_calculation.messages) > 0:
        print('Messages:')
        for message in mixture_constant_properties_calculation.messages:
            print(message)

    if resultCode == ResultCode.SUCCESS:
        print(f'SUCCESS: mixture_constant_properties_calculation ({mixture_constant_properties_calculation.calculation_elapsed_time}ms)')
    else:
        assert False, f'FAILED mixture_constant_properties_calculation with result code {resultCode}'