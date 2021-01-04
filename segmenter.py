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
        self.rows = []
        for i, region in enumerate(self.regions_without_staff):
            staff_lines = self.regions_with_staff[i] - region
            staff_lines = get_thresholded(
                staff_lines, threshold_otsu(staff_lines))
            row_pos = self.staff_row_position(staff_lines)
            rows = self.lines_rows(row_pos)
            self.rows.append(rows)

    def staff_row_position(self, staff_lines):
        img = np.copy(staff_lines)
        found = 0
        row_position = -1
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if(img[i][j] == 0):
                    row_position = i
                    found = 1
                    break
            if found == 1:
                break
        return row_position

    def lines_rows(self, row_position):
        start = row_position
        start -= self.most_common
        rows = []
        row = [start]
        i = 1
        for x in range(7*self.thickness):
            if i < self.thickness:
                start += 1
                i += 1
                row.append(start)
            else:
                rows.append(row)
                row = []
                start += self.spacing+1
                row.append(start)
                i = 1
        return [np.average(x) for x in rows]

    def draw_staff(self):
        image = np.copy(self.no_staff_img)
        for x in range(len(self.rows)):
            image[self.rows[x], :] = 0
        return image

    def open_region(self, region):
        thickness = 3*np.copy(self.thickness)
        if thickness % 2 == 0:
            thickness += 1
        return opening(region, np.ones((thickness, thickness)))

    def segment(self):
        line_indices = get_line_indices(histogram(self.bin_img, 0.8))

        if len(line_indices) == 5:
            self.regions_without_staff = [
                np.copy(self.open_region(self.no_staff_img))]
            self.regions_with_staff = [np.copy(self.bin_img)]
            return

        generated_lines_img = np.copy(self.no_staff_img)
        lines = []
        for index in line_indices:
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

            regions_with_staff.append(
                self.bin_img[y0:y1, 0:self.bin_img.shape[1]])
            staff_block = self.no_staff_img[y0:y1,
                                            0:self.no_staff_img.shape[1]]

            regions_without_staff.append(self.open_region(staff_block))

        self.regions_without_staff = regions_without_staff
        self.regions_with_staff = regions_with_staff
