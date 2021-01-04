from rle import *


class Staff(object):
    def __init__(self, bin_img):
        self.bin_img = np.copy(bin_img)
        self.rle, self.vals = hv_rle(self.bin_img)
        self.most_common = get_most_common(self.rle)
        self.thickness, self.spacing = self.calculate_thickness_spacing()
        self.thick_space = self.thickness + self.spacing

    def calculate_thickness_spacing():
        bw_patterns = [most_common_bw_pattern(
            col, self.most_common) for col in self.rle]
        bw_patterns = [x for x in bw_patterns if x]  # Filter empty patterns

        flattened = []
        for col in bw_patterns:
            flattened += col

        pair, count = Counter(flattened).most_common()[0]

        line_thickness = min(pair)
        line_spacing = max(pair)

        return line_thickness, line_spacing

    def whitene(rle, vals, max_height):
        rlv = []
        for length, value in zip(rle, vals):
            if value == 0 and length < max_height:
                value = 1
            rlv.append((length, value))

        n_rle, n_vals = [], []
        count = 0
        for length, value in rlv:
            if value == 1:
                count = count + length
            else:
                if count > 0:
                    n_rle.append(count)
                    n_vals.append(1)

                count = 0
                n_rle.append(length)
                n_vals.append(0)
        if count > 0:
            n_rle.append(count)
            n_vals.append(1)

        return n_rle, n_vals

    def remove_staff_lines():
        n_rle, n_vals = [], []
        for i in range(len(self.rle)):
            rl, val = whitene(self.rle[i], self.vals[i], 2 * self.thickness)
            n_rle.append(rl)
            n_vals.append(val)

        return hv_decode(n_rle, n_vals, self.bin_img.shape)
