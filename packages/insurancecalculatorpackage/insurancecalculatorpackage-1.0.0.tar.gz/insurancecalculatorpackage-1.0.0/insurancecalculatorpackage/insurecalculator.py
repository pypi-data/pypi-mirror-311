class Calculator:
    def calculate_life_premium(self, age, gender, base_rate, sum_assured, policy_term):
        if gender == 'male':
            gender_factor = 0.08
        elif gender == 'female':
            gender_factor = 0.06
        if age < 35:
            age_factor = 1 + (age / 200)
        else:
            age_factor = 1 + (age / 100)
        to_pay = sum_assured * base_rate * age_factor * policy_term * gender_factor
        return round(to_pay / policy_term / 12)

    def calculate_motor_premium(self, age, initial_idv, base_premium, tenure):
        depreciation_rates = {
            0: 0.05,  # 5% depreciation for 0-1 years old
            1: 0.15,  # 15% for 1-2 years old
            2: 0.25,  # 25% for 2-3 years old
            3: 0.35,  # 35% for 3-4 years old
            4: 0.45,  # 45% for 4-5 years old
        }
        max_age = 10

        if age >= 5:
            vehicle_age_factor = 0.5 + (age - 5) * 0.02  # Incremental 2% depreciation for vehicles >5 years old
        else:
            vehicle_age_factor = depreciation_rates.get(age, 0.0)

        if age > max_age:
            raise ValueError("Vehicle age exceeds maximum allowed limit for insurance.")

        depreciation_rate = vehicle_age_factor
        current_idv = initial_idv * (1 - depreciation_rate)

        age_factor = max(0.5, 1 - (age * 0.05))
        annual_premium = base_premium * age_factor

        total_premium = annual_premium * tenure

        return current_idv, annual_premium, total_premium

    def calculate_health_premium(self, age, gender, base_rate, sum_assured, policy_term):
        if gender == 'male':
            gender_factor = 0.30
        elif gender == 'female':
            gender_factor = 0.25
        age_factor = 1 + (age / 200)
        return sum_assured * base_rate * age_factor * policy_term * gender_factor

