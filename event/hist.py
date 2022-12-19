import matplotlib.pyplot as plt

class Hist:
    def __init__(self, sample):
        self.sample = sample

    def get_probability_of_event(self, real_value, predicted_value):
        # Считаем все образцы, которые попадают в событие
        counter_of_fitted = 0
        left_val = min(real_value, predicted_value)
        right_val = max(real_value, predicted_value)
        for example in self.sample:
            if left_val <= example <= right_val:
                counter_of_fitted+=1
        prob_of_event = counter_of_fitted/len(self.sample)
        return prob_of_event

    def show_hist(self):
        plt.hist(self.sample, density=True, edgecolor="black")
        plt.show()


class BinaryHist:
    def __init__(self, sample):
        self.sample = sample

    def get_probability_of_event(self, real_binary_value):
        ones_mass = sum(self.sample)/len(self.sample)
        if real_binary_value == 0:
            return 1 - ones_mass
        if real_binary_value == 1:
            return ones_mass

        return None

    def show_hist(self):
        plt.hist(self.sample, density=True, edgecolor="black")
        plt.show()
