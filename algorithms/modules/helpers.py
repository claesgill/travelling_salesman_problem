def get_prosentage(pop_size, percent):
    return int(pop_size * percent / 100)

def print_prosentage_done(total, rest):
    percentage = (rest * 100) / total
    if percentage == 100:
        print(f"{int(percentage)}%")
    else:
        print(f"{int(percentage)}%", end="\r")