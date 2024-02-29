import os


def read_file(path):
    with open(path, 'r') as file:
        data = file.read()

    # print(data)
    return data

def write_list_to_file(lst, filename):
    with open(filename, 'w') as f:
        if isinstance(lst, list):
            for item in lst:
                item = item.replace("\"", "")
                f.write("%s\n" % item)
        elif isinstance(lst, str):
            lst = lst.replace("\"", "")
            f.write(lst)

def write_txt_to_file(text, filename):
    with open(filename, 'w') as f:
        f.write(text)

def remove_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path} has been sucessfully removed'")
    except OSError as e:
        print(f"Error: {file_path} - {e.strerror}")

if __name__ == '__main__':
    # read_file("narratives/1.txt")
    my_list = ["apple", "banana"]
    file_path = "../format_result/5.txt"
    write_list_to_file(my_list, file_path)
