from rle import *
from commonfunctions import *
from staff import calculate_thickness_spacing, remove_staff_lines


class Segmenter(object):
    def __init__(self, bin_img):
        self.bin_img = bin_img
        self.rle, self.vals = hv_rle(self.bin_img)
        self.most_common = get_most_common(self.rle)
        self.thickness, self.spacing = calculate_thickness_spacing(
            self.rle, self.most_common)
        self.thick_space = self.thickness + self.spacing
        self.no_staff_img = remove_staff_lines(
            self.rle, self.vals, self.thickness, self.bin_img.shape)

        self.segment()

    def open_region(self, region):
        thickness = np.copy(self.thickness)
        # if thickness % 2 == 0:
        #     thickness += 1
        return opening(region, np.ones((thickness, thickness)))

    def segment(self):
        self.line_indices = get_line_indices(histogram(self.bin_img, 0.8))
        if len(self.line_indices) < 10:
            self.regions_without_staff = [
                np.copy(self.open_region(self.no_staff_img))]
            self.regions_with_staff = [np.copy(self.bin_img)]
            return

        generated_lines_img = np.copy(self.no_staff_img)
        lines = []
        for index in self.line_indices:
            line = ((0, index), (self.bin_img.shape[1]-1, index))
            lines.append(line)

        end_of_staff = []
        for index, line in enumerate(lines):
            if index > 0 and (line[0][1] - end_of_staff[-1][1] < 4*self.spacing):
                pass
            else:
                p1, p2 = line
                x0, y0 = p1
                x1, y1 = p2
                end_of_staff.append((x0, y0, x1, y1))

        box_centers = []
        spacing_between_staff_blocks = []
        for i in range(len(end_of_staff)-1):
            spacing_between_staff_blocks.append(
                end_of_staff[i+1][1] - end_of_staff[i][1])
            if i % 2 == 0:
                offset = (end_of_staff[i+1][1] - end_of_staff[i][1])//2
                center = end_of_staff[i][1] + offset
                box_centers.append((center, offset))

        max_staff_dist = np.max(spacing_between_staff_blocks)
        max_margin = max_staff_dist // 2
        margin = max_staff_dist // 10

        end_points = []
        regions_without_staff = []
        regions_with_staff = []
        for index, (center, offset) in enumerate(box_centers):
            y0 = int(center) - max_margin - offset + margin
            y1 = int(center) + max_margin + offset - margin
            end_points.append((y0, y1))

            region = self.bin_img[y0:y1, 0:self.bin_img.shape[1]]
            regions_with_staff.append(region)
            staff_block = self.no_staff_img[y0:y1,
                                            0:self.no_staff_img.shape[1]]

            regions_without_staff.append(self.open_region(staff_block))

        self.regions_without_staff = regions_without_staff
        self.regions_with_staff = regions_with_staff
