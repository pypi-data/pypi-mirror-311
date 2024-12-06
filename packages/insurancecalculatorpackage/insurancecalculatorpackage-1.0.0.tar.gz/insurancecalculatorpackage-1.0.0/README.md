# Insurance Calculator

Insurance calculator is a Python package for insurance premium calculations. It includes functions to calculate life, motor, and health insurance premiums.

## Installation

Install the library using pip:

```bash
pip install insurance-calculator-omkhulbe
```

## Usage
Just create the object. For ex.
```python
calc = Calculator()
print(calc.calculate_life_premium(34, "female", 0.02, 150000, 20))
print(calc.calculate_health_premium(21, "female", 0.02, 25000, 1))
print(calc.calculate_motor_premium(4, 20000, 120, 2))
```
### For Life Insurance Parameter are as follows:
Age, Gender, Base Rate(0.02 = 2%), Sum Assured, Tenure

It provides the monthly premium amount.

### For Health Insurance Parameter are as follows:
Age, Gender, Base Rate(0.02 = 2%), Sum Assured, Tenure

It provides the overall premium as per the tenure.

### For Motor Insurance Parameter are as follows:
Vehicle Age, Initial IDV, Base Premium, Tenure

It provides three outputs Current IDV, Yearly Premium, Total Premium.