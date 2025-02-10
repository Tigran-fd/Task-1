import csv
import datetime

def read_file(filename: str) -> list:
    with open(filename) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        return list(tsv_file)

def get_timestamp() -> str:
    current_time = datetime.datetime.now()
    return str(current_time.timestamp())

def filter_columns(datalist: list,
                   columns: list) -> list:

    header = datalist[1]
    column_indexes = [header.index(col) for col in columns]

    filtered_data = []

    for row in datalist[2:]:
        try:
            filtered_row = [row[index] for index in column_indexes]
            filtered_data.append(filtered_row)
        except IndexError:
            raise IndexError(f"Row {row} is missing required columns.") from None

    return filtered_data

def filter_stars_by_fov(datalist: list,
                        ra: float,
                        dec: float,
                        fov_h: float,
                        fov_v: float) -> list:
    fov_h_max, fov_h_min = (ra + fov_h / 2) % 360, (ra - fov_h / 2) % 360
    fov_v_max, fov_v_min = dec + fov_v / 2, dec - fov_v / 2

    if fov_v_max > 90 or fov_v_min < -90:
        raise ValueError("FOV should be in the range [-90, 90].")

    filtered_data = []

    for row in datalist:
        try:
            star_ra = float(row[1])
            star_dec = float(row[2])
            if fov_h_min <= star_ra <= fov_h_max and fov_v_min <= star_dec <= fov_v_max:
                filtered_data.append(row)
        except ValueError:
            continue

    return filtered_data

def sort_brightest_n_stars(datalist: list,
                           number_of_stars: int) -> list:
    sorted_data = []

    for current_star in datalist:
        try:
            brightness = float(current_star[3])
        except ValueError:
            sorted_data.append(current_star)
            continue
        position = len(sorted_data) - 1
        while position >= 0 and float(sorted_data[position][3]) < brightness:
            position -= 1

        sorted_data.insert(position + 1, current_star)

    return sorted_data[:number_of_stars]

def calculate_distance(ra_1: float,
                       dec_1: float,
                       ra_2: float,
                       dec_2: float) -> float:
    return ((ra_1 - ra_2) ** 2 + (dec_1 - dec_2) ** 2) ** 0.5

def add_distance_columns(datalist: list,
                         ra: float,
                         dec: float) -> list:
    for row in datalist:
        row.append(calculate_distance(ra, dec, float(row[1]), float(row[2])))
    return datalist

def create_csv(stars_data: list,
               header: list) -> None:
    csv_file_path = f"{get_timestamp()}.csv"
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(stars_data)

def main():
    ra = float(input("Input RA: "))
    dec = float(input("Input DEC: "))
    fov_h = float(input("Input FOV_H: "))
    fov_v = float(input("Input FOV_V: "))
    number_of_stars = int(input("Input number_of_stars: "))

    tsv_file = read_file("cleaned_stars.tsv")

    needed_columns = ["source_id", "ra_ep2000", "dec_ep2000", "b"]

    stars_data = filter_columns(tsv_file, needed_columns)

    filtered_data = filter_stars_by_fov(stars_data, ra, dec, fov_h, fov_v)

    sorted_data = sort_brightest_n_stars(filtered_data, number_of_stars)

    data_with_distance_columns = add_distance_columns(sorted_data, ra, dec)

    csv_file_columns = needed_columns + ["distance"]

    create_csv(data_with_distance_columns, csv_file_columns)

if __name__ == "__main__":
    main()
