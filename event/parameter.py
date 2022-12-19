from event.hist import Hist, BinaryHist

class Parameter:
    def __init__(self, expected_value, sample=None, is_binary=False):
        self.expected_value = expected_value
        self.hist = None
        if sample is not None:
            if is_binary:
                self.hist = BinaryHist(sample)
            else:
                self.hist = Hist(sample)

    def get_probability(self, real_value):
        return self.hist.get_probability_of_event(real_value, self.predicted_value)

