import csv
import datetime

def file_reader(filename) -> list:
    with open(filename) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        return list(tsv_file)

def getting_today_timestamp() -> float:
    current_time = datetime.datetime.now()
    current_timestamp = current_time.timestamp()
    return current_timestamp

def filtering_data_columns(datalist: list,
                           *columns: str) -> list:
    header = datalist[1]

    column_indexes = [header.index(col) for col in columns]

    filtered_data = [list(columns)]
    for row in datalist[2:]:
        try:
            filtered_row = [row[index] for index in column_indexes]
            filtered_data.append(filtered_row)
        except IndexError:
            raise ValueError(f"Row {row} is missing required columns.") from None

    return filtered_data

def filtiring_stars_by_fov(datalist: list,
                           ra: float,
                           dec: float,
                           fov_h: float,
                           fov_v: float,
                           ):
    fov_h_max, fov_h_min = (ra+fov_h/2)%360,(ra-fov_h/2)%360
    fov_v_max, fov_v_min = dec+fov_v/2, ra-fov_v/2
    if fov_v_max > 90:
        raise ValueError(f"fov_h must be less than 90")
    elif fov_v_min < -90:
        raise ValueError(f"fov_h must be less than -90")

    for row in datalist[1:]:
        try:
            star_ra = float(row[0])
            star_dec = float(row[1])
            if not(fov_h_min <= star_ra <= 360 and
                            0 <= star_ra <= fov_h_max and
                     fov_v_min <= star_dec <= fov_v_max):
                datalist.remove(row)
        except ValueError:
            continue
    return

#Insertion sort algorithm
def sorting_brightest_N_stars(datalist: list,
                              number_of_sturs: int
                              ):
    for i in range(2, len(datalist)):

        a = datalist[i]
        j = i - 1
        while j >= 1 and a[3] < datalist[j][3]:
            datalist[j + 1] = datalist[j]
            j -= 1

        datalist[j + 1] = a
    for row in datalist[number_of_sturs+1:]:
        datalist.remove(row)
    return

def find_distance(first_ra: float,
                  first_dec: float,
                  second_ra: float,
                  second_dec: float,
                  ) -> float:
    distance = ((first_ra-second_ra)**2 + (first_dec-second_dec)**2)**0.5
    return distance

def add_distance_columns(datalist: list,
                         ra: float,
                         dec: float,
                         ):
    datalist[0].append('distance')
    for row in datalist[1:]:
        row.append(find_distance(ra, dec, float(row[1]), float(row[2])))
    return

def create_csv(stars_data: list,):
    csv_file_path = "{0}.csv".format(str(getting_today_timestamp()))
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(stars_data)

def main():
    print(-0.3 % 360)
    ra = float(input("Input RA: "))
    dec = float(input("Input DEC: "))
    fov_h = float(input("Input FOV_H: "))
    fov_v = float(input("Input FOV_V: "))
    number_of_stars = int(input("Input number_of_stars: "))

    tcv_file = file_reader("cleaned_stars.tsv")

    needed_columns = ("source_id", "ra_ep2000", "dec_ep2000", "b")

    stars_data = filtering_data_columns(tcv_file, *needed_columns)

    filtiring_stars_by_fov(stars_data, ra, dec, fov_h, fov_v,)

    sorting_brightest_N_stars(stars_data, number_of_stars)

    add_distance_columns(stars_data,ra,dec)

    create_csv(stars_data)

if __name__ == "__main__":
    main()
