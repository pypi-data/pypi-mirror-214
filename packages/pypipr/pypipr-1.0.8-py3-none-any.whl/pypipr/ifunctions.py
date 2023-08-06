'''
Improved functions untuk mempermudah penggunaan
'''


from .lib import *


def iscandir(
    folder_name=".",
    glob_pattern="*",
    recursive=True,
    scan_file=True,
    scan_folder=True,
):
    """
    Mempermudah scandir untuk mengumpulkan folder dan file.

    ```python
    print(generator.iscandir())
    print(iscandir("./", recursive=False, scan_file=False))
    ```
    """
    path_obj = pathlib.Path(folder_name)
    if recursive:
        path_obj = path_obj.rglob(glob_pattern)
    else:
        path_obj = path_obj.glob(glob_pattern)

    for i in path_obj:
        if scan_folder and i.is_dir():
            yield i
        if scan_file and i.is_file():
            yield i


def irange(start, finish, step=1):
    """
    Meningkatkan fungsi range() dari python untuk pengulangan menggunakan huruf

    ```python
    print(generator.irange('a', 'c'))
    print(irange('z', 'a', 10))
    print(irange('a', 'z', 10))
    print(irange(1, '7'))
    print(irange(10, 5))
    ```
    """

    def casting_class():
        start_int = isinstance(start, int)
        finish_int = isinstance(finish, int)
        start_str = isinstance(start, str)
        finish_str = isinstance(finish, str)
        start_numeric = start.isnumeric() if start_str else False
        finish_numeric = finish.isnumeric() if finish_str else False

        if start_numeric and finish_numeric:
            # irange("1", "5")
            return (int, str)

        if (start_numeric or start_int) and (finish_numeric or finish_int):
            # irange("1", "5")
            # irange("1", 5)
            # irange(1, "5")
            # irange(1, 5)
            return (int, int)

        if start_str and finish_str:
            # irange("a", "z")
            # irange("p", "g")
            return (ord, chr)

        """
        kedua if dibawah ini sudah bisa berjalan secara logika, tetapi
        perlu dimanipulasi supaya variabel start dan finish bisa diubah.
        """
        # irange(1, 'a') -> irange('1', 'a')
        # irange(1, '5') -> irange(1, 5)
        # irange('1', 5) -> irange(1, 5)
        # irange('a', 5) -> irange('a', '5')
        #
        # if start_str and finish_int:
        #     # irange("a", 5) -> irange("a", "5")
        #     finish = str(finish)
        #     return (ord, chr)
        #
        # if start_int and finish_str:
        #     # irange(1, "g") -> irange("1", "g")
        #     start = str(start)
        #     return (ord, chr)

        raise Exception(
            f"[{start} - {finish}] tidak dapat diidentifikasi kesamaannya"
        )

    counter_class, converter_class = casting_class()
    start = counter_class(start)
    finish = counter_class(finish)

    step = 1 if is_empty(step) else int(step)

    faktor = 1 if finish > start else -1
    step *= faktor
    finish += faktor

    for i in range(start, finish, step):
        yield converter_class(i)


def iexec(python_syntax, import_pypipr=True):
    """
    improve exec() python function untuk mendapatkan outputnya

    ```python
    print(iexec('print(9*9)'))
    ```
    """
    if import_pypipr:
        python_syntax = f"from pypipr.pypipr import *\n\n{python_syntax}"

    stdout_backup = sys.stdout

    sys.stdout = io.StringIO()
    exec(python_syntax)
    output = sys.stdout.getvalue()

    sys.stdout = stdout_backup

    return output


def iopen(path, data=None, regex=None, css_select=None, xpath=None, file_append=False):
    """
    Membaca atau Tulis pada path yang bisa merupakan FILE maupun URL.

    Baca File :
    - Membaca seluruh file.
    - Jika berhasil content dapat diparse dengan regex.
    - Apabila File berupa html, dapat diparse dengan css atau xpath.

    Tulis File :
    - Menulis pada file.
    - Jika file tidak ada maka akan dibuat.
    - Jika file memiliki content maka akan di overwrite.

    Membaca URL :
    - Mengakses URL dan mengembalikan isi html nya berupa teks.
    - Content dapat diparse dengan regex, css atau xpath.

    Tulis URL :
    - Mengirimkan data dengan metode POST ke url.
    - Jika berhasil dan response memiliki content, maka dapat diparse dengan regex, css atau xpath.


    ```python
    # FILE
    print(iopen("__iopen.txt", "mana aja"))
    print(iopen("__iopen.txt", regex="(\w+)"))
    # URL
    print(iopen("https://www.google.com/", css_select="a"))
    print(iopen("https://www.google.com/", dict(coba="dulu"), xpath="//a"))
    ```
    """
    path = to_str(path)
    content = ""

    if is_valid_url(path):
        req = dict(
            url=path,
            headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"
            },
        )

        if data:
            req["data"] = urllib.parse.urlencode(data).encode()

        req = urllib.request.Request(**req)

        # Connect to URL
        try:
            with urllib.request.urlopen(req) as url_open:
                content = url_open.read().decode()
        except Exception as e:
            # print(f"An error occurred: {str(e)}")
            return False

    else:
        # Write File
        if data is not None:
            mode = "a" if file_append else "w"
            with open(path, mode, encoding="utf-8") as f:
                content = f.write(data)
        # Read File
        else:
            try:
                with open(path, "r") as f:
                    content = f.read()
            except Exception as e:
                # print(f"An error occurred: {str(e)}")
                return False

    """ Parse """
    if regex:
        return re.findall(regex, content)
    if css_select:
        return lxml.html.fromstring(content).cssselect(css_select)
    if xpath:
        return lxml.html.fromstring(content).xpath(xpath)

    """ Return """
    return content


def isplit(text, separator="", include_separator=False):
    """
    Memecah text menjadi list berdasarkan separator.

    ```python
    t = '/ini/contoh/path/'
    print(isplit(t, separator='/'))
    ```
    """
    if include_separator:
        separator = f"({separator})"

    result = re.split(separator, text, flags=re.IGNORECASE | re.MULTILINE)

    return result


def ijoin(
    iterable,
    separator="",
    start="",
    end="",
    remove_empty=False,
    recursive=True,
    recursive_flat=False,
    str_strip=False,
):
    """
    Simplify Python join functions like PHP function.
    Iterable bisa berupa sets, tuple, list, dictionary.

    ```python
    arr = {'asd','dfs','weq','qweqw'}
    print(ijoin(arr, ', '))

    arr = '/ini/path/seperti/url/'.split('/')
    print(ijoin(arr, ','))
    print(ijoin(arr, ',', remove_empty=True))

    arr = {'a':'satu', 'b':(12, 34, 56), 'c':'tiga', 'd':'empat'}
    print(ijoin(arr, separator='</li>\\n<li>', start='<li>', end='</li>', recursive_flat=True))
    print(ijoin(arr, separator='</div>\\n<div>', start='<div>', end='</div>'))
    print(ijoin(10, ' '))
    ```
    """
    if not is_iterable(iterable):
        iterable = [iterable]

    separator = to_str(separator)

    if isinstance(iterable, dict):
        iterable = iterable.values()

    if remove_empty:
        iterable = (i for i in filter_empty(iterable))

    if recursive:
        rec_flat = dict(start=start, end=end)
        if recursive_flat:
            rec_flat = dict(start="", end="")
        rec = lambda x: ijoin(
            iterable=x,
            separator=separator,
            **rec_flat,
            remove_empty=remove_empty,
            recursive=recursive,
            recursive_flat=recursive_flat,
        )
        iterable = ((rec(i) if is_iterable(i) else i) for i in iterable)

    iterable = (str(i) for i in iterable)

    if str_strip:
        iterable = (i.strip() for i in iterable)

    result = start

    for index, value in enumerate(iterable):
        if index:
            result += separator
        result += value

    result += end

    return result


def ireplace(
    string: str,
    replacements: dict,
    flags=re.DOTALL | re.MULTILINE | re.IGNORECASE,
):
    """
    STRing TRanslate mengubah string menggunakan kamus dari dict.
    Replacement dapat berupa text biasa ataupun regex pattern.
    Apabila replacement berupa regex, gunakan raw string `r"..."`
    Untuk regex capturing gunakan `(...)`, dan untuk mengaksesnya gunakan `\\1`, `\\2`, .., dst.

    ```python
    text = 'aku ini mau ke sini'
    replacements = {
        "sini": "situ",
        r"(ini)": r"itu dan \\1",
    }
    print(ireplace(text, replacements))
    ```
    """
    for i, v in replacements.items():
        string = re.sub(i, v, string, flags=flags)
    return string



if __name__ == "__main__":
    print_colorize("Anda menjalankan module pypipr", color=colorama.Fore.RED)
