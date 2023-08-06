
# About
The Python Package Index Project (pypipr)

pypi : https://pypi.org/project/pypipr


# Setup
Install with pip
```
pip install pypipr
```

Import with * for fastest access
```python
from pypipr.pypipr import *
```

# CONSTANT

`LINUX`

`WINDOWS`

# FUNCTION

## avg

`avg`

Simple Average Function karena tidak disediakan oleh python  

```python  
n = [1, 22, 2, 3, 13, 2, 123, 12, 31, 2, 2, 12, 2, 1]  
print(avg(n))  
```

Output:
```py
16.285714285714285
```

## basename

`basename`

Mengembalikan nama file dari path  

```python  
print(basename("/ini/nama/folder/ke/file.py"))  
```

Output:
```py
file.py
```

## batchmaker

`batchmaker`

Alat Bantu untuk membuat teks yang berulang.  
Gunakan {[start][separator][finish]([separator][step])}.  
```  
[start] dan [finish]    -> bisa berupa huruf maupun angka  
([separator][step])     -> bersifat optional  
[separator]             -> selain huruf dan angka  
[step]                  -> berupa angka positif  
```  

```python  
s = "Urutan {1/6/3} dan {10:9} dan {j k} dan {Z - A - 15} saja."  
print(generator.batchmaker(s))  
print(batchmaker(s))  
```

Output:
```py
<generator object generator.batchmaker at 0x7c61eb7d00>
('Urutan 1 dan 10 dan j dan Z saja.', 'Urutan 1 dan 10 dan j dan K saja.', 'Urutan 1 dan 10 dan k dan Z saja.', 'Urutan 1 dan 10 dan k dan K saja.', 'Urutan 1 dan 9 dan j dan Z saja.', 'Urutan 1 dan 9 dan j dan K saja.', 'Urutan 1 dan 9 dan k dan Z saja.', 'Urutan 1 dan 9 dan k dan K saja.', 'Urutan 4 dan 10 dan j dan Z saja.', 'Urutan 4 dan 10 dan j dan K saja.', 'Urutan 4 dan 10 dan k dan Z saja.', 'Urutan 4 dan 10 dan k dan K saja.', 'Urutan 4 dan 9 dan j dan Z saja.', 'Urutan 4 dan 9 dan j dan K saja.', 'Urutan 4 dan 9 dan k dan Z saja.', 'Urutan 4 dan 9 dan k dan K saja.')
```

## calculate

`calculate`

Mengembalikan hasil dari perhitungan teks menggunakan modul pint.  
Mendukung perhitungan matematika dasar dengan satuan.  

Return value:  
- Berupa class Quantity dari modul pint  

Format:  
- f"{result:~P}"            -> pretty  
- f"{result:~H}"            -> html  
- result.to_base_units()    -> SI  
- result.to_compact()       -> human readable  

```python  
fx = "3 meter * 10 cm * 3 km"  
res = calculate(fx)  
print(res)  
print(res.to_base_units())  
print(res.to_compact())  
print(f"{res:~P}")  
print(f"{res:~H}")  
```

Output:
```py
90 centimeter * kilometer * meter
900.0 meter ** 3
900.0 meter ** 3
90 cm·km·m
90 cm km m
```

## chunck_array

`chunck_array`

Membagi array menjadi potongan-potongan dengan besaran yg diinginkan  

```python  
array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]  
print(generator.chunck_array(array, 5))  
print(chunck_array(array, 5))  
```

Output:
```py
<generator object generator.chunck_array at 0x7c61f7fe40>
([2, 3, 12, 3, 3], [42, 42, 1, 43, 2], [42, 41, 4, 24, 32], [42, 3, 12, 32, 42], [42])
```

## console_run

`console_run`

Menjalankan command seperti menjalankan command di Command Terminal  

```py  
console_run('dir')  
console_run('ls')  
```

## create_folder

`create_folder`

Membuat folder.  
Membuat folder secara recursive dengan permission.  

```py  
create_folder("contoh_membuat_folder")  
create_folder("contoh/membuat/folder/recursive")  
create_folder("./contoh_membuat_folder/secara/recursive")  
```

## datetime_from_string

`datetime_from_string`

Parse iso_string menjadi datetime object  

```python  
print(datetime_from_string("2022-12-12 15:40:13").isoformat())  
print(datetime_from_string("2022-12-12 15:40:13", timezone="Asia/Jakarta").isoformat())  
```

Output:
```py
2022-12-12T15:40:13+00:00
2022-12-12T15:40:13+07:00
```

## datetime_now

`datetime_now`

Memudahkan dalam membuat Datetime untuk suatu timezone tertentu  

```python  
print(datetime_now("Asia/Jakarta"))  
print(datetime_now("GMT"))  
print(datetime_now("Etc/GMT+7"))  
```

Output:
```py
2023-06-16 15:34:30.771887+07:00
2023-06-16 08:34:30.773421+00:00
2023-06-16 01:34:30.778299-07:00
```

## dict_first

`dict_first`

Mengambil nilai (key, value) pertama dari dictionary dalam bentuk tuple.  

```python  
d = {  
    "key2": "value2",  
    "key3": "value3",  
    "key1": "value1",  
}  
print(dict_first(d, remove=True))  
print(dict_first(d))  
```

Output:
```py
('key2', 'value2')
('key3', 'value3')
```

## dirname

`dirname`

Mengembalikan nama folder dari path.  
Tanpa trailing slash di akhir.  

```python  
print(dirname("/ini/nama/folder/ke/file.py"))  
```

Output:
```py
/ini/nama/folder/ke
```

## exit_if_empty

`exit_if_empty`

Keluar dari program apabila seluruh variabel  
setara dengan empty  

```py  
var1 = None  
var2 = '0'  
exit_if_empty(var1, var2)  
```

## explode

`explode`

Memecah text menjadi list berdasarkan separator.  

```python  
t = '/ini/contoh/path/'  
print(explode(t, separator='/'))  
```

Output:
```py
['', 'ini', 'contoh', 'path', '']
```

## filter_empty

`filter_empty`

## get_class_method

`get_class_method`

Mengembalikan berupa tuple yg berisi list dari method dalam class  

```python  
class ExampleGetClassMethod:  
    def a():  
        return [x for x in range(10)]  

    def b():  
        return [x for x in range(10)]  

    def c():  
        return [x for x in range(10)]  

    def d():  
        return [x for x in range(10)]  

print(get_class_method(ExampleGetClassMethod))  
```

Output:
```py
(<function ExampleGetClassMethod.a at 0x7c61d428e0>, <function ExampleGetClassMethod.b at 0x7c61d42840>, <function ExampleGetClassMethod.c at 0x7c61d42a20>, <function ExampleGetClassMethod.d at 0x7c61d42ac0>)
```

## get_filemtime

`get_filemtime`

Mengambil informasi last modification time file dalam nano seconds  

```python  
print(get_filemtime(__file__))  
```

Output:
```py
1686901831479416922
```

## get_filesize

`get_filesize`

Mengambil informasi file size dalam bytes  

```python  
print(get_filesize(__file__))  
```

Output:
```py
43701
```

## github_pull

`github_pull`

Menjalankan command `git pull`  

```py  
github_pull()  
```

## github_push

`github_push`

Menjalankan command status, add, commit dan push  

```py  
github_push('Commit Message')  
```

## iexec

`iexec`

improve exec() python function untuk mendapatkan outputnya  

```python  
print(iexec('print(9*9)'))  
```

Output:
```py
81

```

## implode

`implode`

Simplify Python join functions like PHP function.  
Iterable bisa berupa sets, tuple, list, dictionary.  

```python  
arr = {'asd','dfs','weq','qweqw'}  
print(implode(arr, ', '))  

arr = '/ini/path/seperti/url/'.split('/')  
print(implode(arr, ','))  
print(implode(arr, ',', remove_empty=True))  

arr = {'a':'satu', 'b':(12, 34, 56), 'c':'tiga', 'd':'empat'}  
print(implode(arr, separator='</li>\n<li>', start='<li>', end='</li>', recursive_flat=True))  
print(implode(arr, separator='</div>\n<div>', start='<div>', end='</div>'))  
print(implode(10, ' '))  
```

Output:
```py
qweqw, asd, dfs, weq
,ini,path,seperti,url,
ini,path,seperti,url
<li>satu</li>
<li>12</li>
<li>34</li>
<li>56</li>
<li>tiga</li>
<li>empat</li>
<div>satu</div>
<div><div>12</div>
<div>34</div>
<div>56</div></div>
<div>tiga</div>
<div>empat</div>
10
```

## input_char

`input_char`

Meminta masukan satu huruf tanpa menekan Enter.  

```py  
input_char("Input char : ")  
input_char("Input char : ", default='Y')  
input_char("Input Char without print : ", echo_char=False)  
```

## iopen

`iopen`

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

Output:
```py
8
['mana', 'aja']
[<Element a at 0x7c631948c0>, <Element a at 0x7c61e23d40>, <Element a at 0x7c61ba3430>, <Element a at 0x7c61ba34d0>, <Element a at 0x7c61ba3520>, <Element a at 0x7c61ba3570>, <Element a at 0x7c61ba35c0>, <Element a at 0x7c61ba3610>, <Element a at 0x7c61ba3660>, <Element a at 0x7c61ba36b0>, <Element a at 0x7c61ba3700>, <Element a at 0x7c61ba3750>, <Element a at 0x7c61ba37a0>, <Element a at 0x7c61ba37f0>, <Element a at 0x7c61ba3840>, <Element a at 0x7c61ba3890>, <Element a at 0x7c61ba38e0>, <Element a at 0x7c61ba3930>]
False
```

## irange

`irange`

Improve python range() function untuk pengulangan menggunakan huruf  

```python  
print(generator.irange('a', 'z'))  
print(irange('H', 'a'))  
print(irange('1', '5', 3))  
print(irange('1', 5, 3))  
# print(irange('a', 5, 3))  
print(irange(-10, 4, 3))  
print(irange(1, 5))  
```

Output:
```py
<generator object generator.irange at 0x7c64594bf0>
['H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a']
['1', '4']
[1, 4]
[-10, -7, -4, -1, 2]
[1, 2, 3, 4, 5]
```

## is_empty

`is_empty`

Mengecek apakah variable setara dengan nilai kosong pada empty.  

Pengecekan nilai yang setara menggunakan simbol '==', sedangkan untuk  
pengecekan lokasi memory yang sama menggunakan keyword 'is'  

```python  
print(is_empty("teks"))  
print(is_empty(True))  
print(is_empty(False))  
print(is_empty(None))  
print(is_empty(0))  
print(is_empty([]))  
```

Output:
```py
False
False
True
True
True
True
```

## is_iterable

`is_iterable`

Mengecek apakah suatu variabel bisa dilakukan forloop atau tidak  

```python  
s = 'ini string'  
print(is_iterable(s))  

l = [12,21,2,1]  
print(is_iterable(l))  

r = range(100)  
print(is_iterable(r))  

d = {'a':1, 'b':2}  
print(is_iterable(d.values()))  
```

Output:
```py
False
True
True
True
```

## is_valid_url

`is_valid_url`

Mengecek apakah path merupakan URL yang valid atau tidak.  
Cara ini merupakan cara yang paling efektif.  

```python  
print(is_valid_url("https://chat.openai.com/?model=text-davinci-002-render-sha"))  
print(is_valid_url("https://chat.openai.com/?model/=text-dav/inci-002-render-sha"))  
```

Output:
```py
True
True
```

## iscandir

`iscandir`

Mempermudah scandir untuk mengumpulkan folder dan file.  

```python  
print(generator.iscandir())  
print(iscandir("./", recursive=False, scan_file=False))  
```

Output:
```py
<generator object generator.iscandir at 0x7c61f7e040>
(PosixPath('.vscode'), PosixPath('pypipr'), PosixPath('dist'), PosixPath('.git'))
```

## log

`log`

Decorator untuk mempermudah pembuatan log karena tidak perlu mengubah fungsi yg sudah ada.  
Melakukan print ke console untuk menginformasikan proses yg sedang berjalan didalam program.  

```py  
@log  
def some_function():  
    pass  

@log()  
def some_function_again():  
    pass  

@log("Calling some function")  
def some_function_more():  
    pass  

some_function()  
some_function_again()  
some_function_more()  
```

## print_colorize

`print_colorize`

Print text dengan warna untuk menunjukan text penting  

```py  
print_colorize("Print some text")  
print_colorize("Print some text", color=colorama.Fore.RED)  
```

## print_dir

`print_dir`

Print property dan method yang tersedia pada variabel  

```python  
p = pathlib.Path("https://www.google.com/")  
print_dir(p, colorize=False)  
```

Output:
```py
           __bytes__ : b'https:/www.google.com'
           __class__ : .
             __dir__ : ['__module__', '__doc__', '__slots__', '__new__', '_make_child_relpath', '__enter__', '__exit__', 'cwd', 'home', 'samefile', 'iterdir', '_scandir', 'glob', 'rglob', 'absolute', 'resolve', 'stat', 'owner', 'group', 'open', 'read_bytes', 'read_text', 'write_bytes', 'write_text', 'readlink', 'touch', 'mkdir', 'chmod', 'lchmod', 'unlink', 'rmdir', 'lstat', 'rename', 'replace', 'symlink_to', 'hardlink_to', 'link_to', 'exists', 'is_dir', 'is_file', 'is_mount', 'is_symlink', 'is_block_device', 'is_char_device', 'is_fifo', 'is_socket', 'expanduser', '__reduce__', '_parse_args', '_from_parts', '_from_parsed_parts', '_format_parsed_parts', '_make_child', '__str__', '__fspath__', 'as_posix', '__bytes__', '__repr__', 'as_uri', '_cparts', '__eq__', '__hash__', '__lt__', '__le__', '__gt__', '__ge__', 'drive', 'root', 'anchor', 'name', 'suffix', 'suffixes', 'stem', 'with_name', 'with_stem', 'with_suffix', 'relative_to', 'is_relative_to', 'parts', 'joinpath', '__truediv__', '__rtruediv__', 'parent', 'parents', 'is_absolute', 'is_reserved', 'match', '_cached_cparts', '_drv', '_hash', '_parts', '_pparts', '_root', '_str', '__getattribute__', '__setattr__', '__delattr__', '__ne__', '__init__', '__reduce_ex__', '__getstate__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__', '_flavour']
             __doc__ : Path subclass for non-Windows systems.

    On a POSIX system, instantiating a Path should return this object.
    
           __enter__ : https:/www.google.com
          __fspath__ : https:/www.google.com
        __getstate__ : (None, {'_drv': '', '_root': '', '_parts': ['https:', 'www.google.com'], '_str': 'https:/www.google.com'})
            __hash__ : 4473962716942053088
            __init__ : None
   __init_subclass__ : None
          __module__ : pathlib
          __reduce__ : (<class 'pathlib.PosixPath'>, ('https:', 'www.google.com'))
            __repr__ : PosixPath('https:/www.google.com')
          __sizeof__ : 72
           __slots__ : ()
             __str__ : https:/www.google.com
    __subclasshook__ : NotImplemented
      _cached_cparts : ['https:', 'www.google.com']
             _cparts : ['https:', 'www.google.com']
                _drv : 
            _flavour : <pathlib._PosixFlavour object at 0x7c6393dd10>
               _hash : 4473962716942053088
              _parts : ['https:', 'www.google.com']
               _root : 
                _str : https:/www.google.com
            absolute : /data/data/com.termux/files/home/pypipr/https:/www.google.com
              anchor : 
            as_posix : https:/www.google.com
                 cwd : /data/data/com.termux/files/home/pypipr
               drive : 
              exists : False
          expanduser : https:/www.google.com
                home : /data/data/com.termux/files/home
         is_absolute : False
     is_block_device : False
      is_char_device : False
              is_dir : False
             is_fifo : False
             is_file : False
            is_mount : False
         is_reserved : False
           is_socket : False
          is_symlink : False
             iterdir : <generator object Path.iterdir at 0x7c61d47060>
            joinpath : https:/www.google.com
                name : www.google.com
              parent : https:
             parents : <PosixPath.parents>
               parts : ('https:', 'www.google.com')
             resolve : /data/data/com.termux/files/home/pypipr/https:/www.google.com
                root : 
                stem : www.google
              suffix : .com
            suffixes : ['.google', '.com']
```

## print_log

`print_log`

Akan melakukan print ke console.  
Berguna untuk memberikan informasi proses program yg sedang berjalan.  

```py  
print_log("Standalone Log")  
```

## random_bool

`random_bool`

Menghasilkan nilai random True atau False.  
Fungsi ini merupakan fungsi tercepat untuk mendapatkan random bool.  
Fungsi ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan  
overhead yg besar.  

```python  
print(random_bool())  
```

Output:
```py
False
```

## serialize

`serialize`

Mengubah variabel data menjadi string untuk yang dapat dibaca untuk disimpan.  
String yang dihasilkan berbentuk syntax YAML/JSON/HTML.  

```python  
data = {  
    'a': 123,  
    't': ['disini', 'senang', 'disana', 'senang'],  
    'l': (12, 23, [12, 42]),  
}  
print(serialize(data))  
print(serialize(data, syntax='html'))  
```

Output:
```py
a: 123
l: !!python/tuple
- 12
- 23
-   - 12
    - 42
t:
- disini
- senang
- disana
- senang

<table>
    <tbody>
        <tr>
            <th>a</th>
            <td>
                <span>123</span>
            </td>
        </tr>
        <tr>
            <th>t</th>
            <td>
                <ul>
                    <li>
                        <span>disini</span>
                    </li>
                    <li>
                        <span>senang</span>
                    </li>
                    <li>
                        <span>disana</span>
                    </li>
                    <li>
                        <span>senang</span>
                    </li>
                </ul>
            </td>
        </tr>
        <tr>
            <th>l</th>
            <td>
                <ul>
                    <li>
                        <span>12</span>
                    </li>
                    <li>
                        <span>23</span>
                    </li>
                    <li>
                        <ul>
                            <li>
                                <span>12</span>
                            </li>
                            <li>
                                <span>42</span>
                            </li>
                        </ul>
                    </li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

```

## serialize_html

`serialize_html`

Serialisasi python variabel menjadi HTML.  
```  
List -> <ul>...</ul>  
Dict -> <table>...</table>  
```  

```python  
data = {  
    'abc': 123,  
    'list': [1, 2, 3, 4, 5],  
    'dict': {'a': 1, 'b':2, 'c':3},  
}  
print(serialize_html(data))  
```

Output:
```py
<table>
  <tbody>
    <tr>
      <th>abc</th>
      <td>
        <span>123</span>
      </td>
    </tr>
    <tr>
      <th>list</th>
      <td>
        <ul>
          <li>
            <span>1</span>
          </li>
          <li>
            <span>2</span>
          </li>
          <li>
            <span>3</span>
          </li>
          <li>
            <span>4</span>
          </li>
          <li>
            <span>5</span>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <th>dict</th>
      <td>
        <table>
          <tbody>
            <tr>
              <th>a</th>
              <td>
                <span>1</span>
              </td>
            </tr>
            <tr>
              <th>b</th>
              <td>
                <span>2</span>
              </td>
            </tr>
            <tr>
              <th>c</th>
              <td>
                <span>3</span>
              </td>
            </tr>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
</table>

```

## set_timeout

`set_timeout`

Menjalankan fungsi ketika sudah sekian detik.  
Apabila timeout masih berjalan tapi kode sudah selesai dieksekusi semua, maka  
program tidak akan berhenti sampai timeout selesai, kemudian fungsi dijalankan,  
kemudian program dihentikan.  

```python  
set_timeout(3, lambda: print("Timeout 3"))  
x = set_timeout(7, lambda: print("Timeout 7"))  
print(x)  
print("menghentikan timeout 7")  
x.cancel()  
```

Output:
```py
<Timer(Thread-2, started 534192831744)>
menghentikan timeout 7
```

## sets_ordered

`sets_ordered`

Hanya mengambil nilai unik dari suatu list  

```python  
array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]  
print(generator.sets_ordered(array))  
print(sets_ordered(array))  
```

Output:
```py
<generator object generator.sets_ordered at 0x7c61d86810>
[2, 3, 12, 42, 1, 43, 41, 4, 24, 32]
```

## str_cmp

`str_cmp`

Membandingakan string secara incase-sensitive menggunakan lower().  
Lebih cepat dibandingkan upper(), casefold(), re.fullmatch(), len().  
perbandingan ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan  
overhead yg besar.  
```python  
print(str_cmp('teks1', 'Teks1'))  
```

Output:
```py
True
```

## strtr

`strtr`

STRing TRanslate mengubah string menggunakan kamus dari dict.  
Replacement dapat berupa text biasa ataupun regex pattern.  
Apabila replacement berupa regex, gunakan raw string `r"..."`  
Untuk regex capturing gunakan `(...)`, dan untuk mengaksesnya gunakan `\1`, `\2`, .., dst.  

```python  
text = 'aku ini mau ke sini'  
replacements = {  
    "sini": "situ",  
    r"(ini)": r"itu dan \1",  
}  
print(strtr(text, replacements))  
```

Output:
```py
aku itu dan ini mau ke situ
```

## to_str

`to_str`

Mengubah value menjadi string literal  

```python  
print(to_str(5))  
print(to_str([]))  
print(to_str(False))  
print(to_str(True))  
print(to_str(None))  
```

Output:
```py
5

False
True

```

## unserialize

`unserialize`

Mengubah string data hasil dari serialize menjadi variabel.  
String data adalah berupa syntax YAML.  

```python  
data = {  
    'a': 123,  
    't': ['disini', 'senang', 'disana', 'senang'],  
    'l': (12, 23, [12, 42])  
}  
s = serialize(data)  
print(unserialize(s))  
```

## unserialize_html

`unserialize_html`

Mengambil data yang berupa list `<ul>`, dan table `<table>` dari html  
dan menjadikannya data python berupa list.  
setiap data yang ditemukan akan dibungkus dengan tuple sebagai separator.  
```  
list (<ul>)     -> list         -> list satu dimensi  
table (<table>) -> list[list]   -> list satu dimensi didalam list  
```  
apabila data berupa ul maka dapat dicek type(data) -> html_ul  
apabila data berupa ol maka dapat dicek type(data) -> html_ol  
apabila data berupa dl maka dapat dicek type(data) -> html_dl  
apabila data berupa table maka dapat dicek type(data) -> html_table  

```python  
pprint.pprint(unserialize_html(iopen("https://harga-emas.org/")), depth=10)  
pprint.pprint(unserialize_html(iopen("https://harga-emas.org/1-gram/")), depth=10)  
```

Output:
```py
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram'],
 [['Harga Emas Hari Ini - Jumat, 16 Juni 2023'],
  ['Spot Emas USD↑1.961,18 (+1,93) / oz',
   'Kurs IDR15.140,00 / USD',
   'Emas IDR↑954.628 (+939) / gr'],
  ['LM Antam (Jual)↑1.061.000 (+9.000) / gr',
   'LM Antam (Beli)↑942.000 (+9.000) / gr']],
 [['Harga Emas Hari Ini'],
  ['Gram', 'Gedung Antam Jakarta', 'Pegadaian'],
  ['per Gram (Rp)', 'per Batangan (Rp)', 'per Gram (Rp)', 'per Batangan (Rp)'],
  ['1000',
   '1.002 (+9)',
   '1.001.600 (+9.000)',
   '1.017.415 (-1.025)',
   '1.017.415.000 (-1.025.000)'],
  ['500',
   '2.003 (+18)',
   '1.001.640 (+9.000)',
   '1.017.456 (-1.026)',
   '508.728.000 (-513.000)'],
  ['250',
   '4.008 (+36)',
   '1.002.060 (+9.000)',
   '1.017.888 (-1.024)',
   '254.472.000 (-256.000)'],
  ['100',
   '10.031 (+90)',
   '1.003.120 (+9.000)',
   '1.018.980 (-1.020)',
   '101.898.000 (-102.000)'],
  ['50',
   '20.078 (+180)',
   '1.003.900 (+9.000)',
   '1.019.780 (-1.020)',
   '50.989.000 (-51.000)'],
  ['25',
   '40.219 (+360)',
   '1.005.480 (+9.000)',
   '1.021.400 (-1.040)',
   '25.535.000 (-26.000)'],
  ['10',
   '101.050 (+900)',
   '1.010.500 (+9.000)',
   '1.026.600 (-1.000)',
   '10.266.000 (-10.000)'],
  ['5',
   '203.200 (+1.800)',
   '1.016.000 (+9.000)',
   '1.032.200 (-1.000)',
   '5.161.000 (-5.000)'],
  ['3',
   '340.889 (+3.000)',
   '1.022.667 (+9.000)',
   '1.039.333 (-1.000)',
   '3.118.000 (-3.000)'],
  ['2',
   '515.500 (+4.500)',
   '1.031.000 (+9.000)',
   '1.048.000 (-1.000)',
   '2.096.000 (-2.000)'],
  ['1',
   '1.061.000 (+9.000)',
   '1.061.000 (+9.000)',
   '1.079.000 (-1.000)',
   '1.079.000 (-1.000)'],
  ['0.5',
   '2.322.000 (+18.000)',
   '1.161.000 (+9.000)',
   '1.182.000 (-2.000)',
   '591.000 (-1.000)'],
  ['Update harga LM Antam :16 Juni 2023, pukul 08:16Harga pembelian kembali '
   ':Rp. 942.000/gram (+9.000)',
   'Update harga LM Pegadaian :16 Juni 2023']],
 [['Spot Harga Emas Hari Ini (Market Open)'],
  ['Satuan', 'USD', 'Kurs\xa0Dollar', 'IDR'],
  ['Ounce\xa0(oz)', '1.961,18 (+1,93)', '15.140,00', '29.692.265'],
  ['Gram\xa0(gr)', '63,05', '15.140,00', '954.628 (+939)'],
  ['Kilogram\xa0(kg)', '63.053,40', '15.140,00', '954.628.494'],
  ['Update harga emas :16 Juni 2023, pukul 15:34Update kurs :13 Febuari 2023, '
   'pukul 09:10']],
 [['Gram', 'UBS Gold 99.99%'],
  ['Jual', 'Beli'],
  ['/ Batang', '/ Gram', '/ Batang', '/ Gram'],
  ['100',
   '95.685.000 (+400.000)',
   '956.850 (+4.000)',
   '94.300.000 (+900.000)',
   '943.000 (+9.000)'],
  ['50',
   '47.895.000 (+200.000)',
   '957.900 (+4.000)',
   '47.150.000 (+450.000)',
   '943.000 (+9.000)'],
  ['25',
   '24.050.000 (+100.000)',
   '962.000 (+4.000)',
   '23.575.000 (+225.000)',
   '943.000 (+9.000)'],
  ['10',
   '9.670.000 (+40.000)',
   '967.000 (+4.000)',
   '9.430.000 (+90.000)',
   '943.000 (+9.000)'],
  ['5',
   '4.887.000 (+20.000)',
   '977.400 (+4.000)',
   '4.715.000 (+45.000)',
   '943.000 (+9.000)'],
  ['1',
   '1.010.000 (+4.000)',
   '1.010.000 (+4.000)',
   '943.000 (+9.000)',
   '943.000 (+9.000)'],
  ['', 'Update :16 Juni 2023, pukul 10:55']],
 [['Konversi Satuan'],
  ['Satuan', 'Ounce (oz)', 'Gram (gr)', 'Kilogram (kg)'],
  ['Ounce\xa0(oz)', '1', '31,1034767696', '0,0311034768'],
  ['Gram\xa0(gr)', '0,0321507466', '1', '0.001'],
  ['Kilogram\xa0(kg)', '32,1507466000', '1.000', '1']],
 [['Pergerakan Harga Emas Dunia'],
  ['Waktu', 'Emas'],
  ['Unit', 'USD', 'IDR'],
  ['Angka', '+/-', 'Angka', '+/-'],
  ['Hari Ini', 'Kurs', '', '', '15.140', '%'],
  ['oz', '1.959,25', '+1,93+0,10%', '29.663.045', '+29.220+0,10%'],
  ['gr', '62,99', '+0,06+0,10%', '953.689', '+939+0,10%'],
  ['30 Hari', 'Kurs', '', '', '15.140', '%'],
  ['oz', '1.984,24', '-23,06-1,16%', '30.041.394', '-349.128-1,16%'],
  ['gr', '63,79', '-0,74-1,16%', '965.853', '-11.225-1,16%'],
  ['2 Bulan', 'Kurs', '', '', '15.140', '%'],
  ['oz', '1.991,63', '-30,45-1,53%', '30.153.278', '-461.013-1,53%'],
  ['gr', '64,03', '-0,98-1,53', '969.450', '-14.822-1,53%'],
  ['6 Bulan', 'Kurs', '', '', '15.630', '-490-3,13%'],
  ['oz', '1.793,13', '+168,05+9,37%', '28.026.622', '+1.665.643+5,94%'],
  ['gr', '57,65', '+5,40+9,37%', '901.077', '+53.552+5,94%'],
  ['1 Tahun', 'Kurs', '', '', '14.746', '+394+2,67%'],
  ['oz', '1.852,26', '+108,92+5,88%', '27.313.426', '+2.378.839+8,71%'],
  ['gr', '59,55', '+3,50+5,88%', '878.147', '+76.481+8,71%'],
  ['2 Tahun', 'Kurs', '', '', '14.244', '+896+6,29%'],
  ['oz', '1.859,27', '+101,91+5,48%', '26.483.442', '+3.208.823+12,12%'],
  ['gr', '59,78', '+3,28+5,48%', '851.462', '+103.166+12,12%'],
  ['3 Tahun', 'Kurs', '', '', '14.155', '+985+6,96%'],
  ['oz', '1.729,14', '+232,04+13,42%', '24.475.994', '+5.216.271+21,31%'],
  ['gr', '55,59', '+7,46+13,42%', '786.921', '+167.707+21,31%'],
  ['5 Tahun', 'Kurs', '', '', '13.902', '+1.238+8,91%'],
  ['oz', '1.280,09', '+681,09+53,21%', '17.795.811', '+11.896.454+66,85%'],
  ['gr', '41,16', '+21,90+53,21%', '572.149', '+382.480+66,85%']])
Timeout 3
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram'],
 [[''],
  ['Emas 24 KaratHarga Emas 1 Gram', ''],
  ['USD', '63,05↑', '+0,06+0,10%'],
  ['KURS', '14.945,75↑', '+41,75+0,28%'],
  ['IDR', '942.380,37↑', '+3.557,29+0,38%'],
  ['Jumat, 16 Juni 2023 15:34']],
 [[''],
  ['Emas 1 Gram (IDR)Emas 1 Gram (USD)Kurs USD-IDR',
   'Hari Ini',
   '1 Bulan',
   '1 Tahun',
   '5 Tahun',
   'Max',
   '']],
 [['Pergerakkan Harga Emas 1 Gram'],
  ['', 'Penutupan Kemarin', 'Pergerakkan Hari Ini', 'Rata-rata'],
  ['USD', '62,99', '62,99 - 63,05', '63,02'],
  ['KURS', '14.904,00', '14.904,00 - 14.945,75', '14.924,88'],
  ['IDR', '938.823,08', '938.823,08 - 942.380,37', '940.601,73'],
  [''],
  ['', 'Awal Tahun', 'Pergerakkan YTD', '+/- YTD'],
  ['USD', '58,64', '58,23 - 65,97', '+4,41 (7,52%)'],
  ['KURS', '15.538,50', '14.669,40 - 15.629,15', '-592,75(-3,81%)'],
  ['IDR', '911.153,72', '888.842,84 - 982.694,10', '+31.226,65 (3,43%)'],
  [''],
  ['', 'Tahun Lalu / 52 Minggu', 'Pergerakkan 52 Minggu', '+/- 52 Minggu'],
  ['USD', '58,52', '52,31 - 65,97', '+4,53 (7,74%)'],
  ['KURS', '14.767,85', '14.653,00 - 15.785,40', '+177,90 (1,20%)'],
  ['IDR', '864.259,47', '795.009,21 - 982.694,10', '+78.120,90 (9,04%)']])
```

# CLASS

## ComparePerformance

`ComparePerformance`

Menjalankan seluruh method dalam class,  
Kemudian membandingkan waktu yg diperlukan.  
Nilai 100 berarti yang tercepat.  
  
```python  
class ExampleComparePerformance(ComparePerformance):  
    # number = 1  
    z = 10  
  
    def a(self):  
        return (x for x in range(self.z))  
  
    def b(self):  
        return tuple(x for x in range(self.z))  
  
    def c(self):  
        return [x for x in range(self.z)]  
  
    def d(self):  
        return list(x for x in range(self.z))  
  
pprint.pprint(ExampleComparePerformance().compare_result(), depth=100)  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
```

Output:
```py
{'a': <generator object ExampleComparePerformance.a.<locals>.<genexpr> at 0x7c61d85f20>,
 'b': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
 'c': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 'd': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
{'a': 104, 'b': 109, 'c': 100, 'd': 152}
{'a': 144, 'b': 139, 'c': 100, 'd': 186}
{'a': 143, 'b': 137, 'c': 100, 'd': 166}
{'a': 117, 'b': 135, 'c': 100, 'd': 149}
{'a': 126, 'b': 141, 'c': 100, 'd': 158}
```

## RunParallel

`RunParallel`

Menjalankan program secara bersamaan.  
  
- `class RunParallel` didesain hanya untuk pemrosesan data saja.  
- Penggunaannya `class RunParallel` dengan cara membuat instance sub class beserta data yg akan diproses, kemudian panggil fungsi yg dipilih `run_asyncio / run_multi_threading / run_multi_processing`, kemudian dapatkan hasilnya.  
- `class RunParallel` tidak didesain untuk menyimpan data, karena setiap module terutama module `multiprocessing` tidak dapat mengakses data kelas dari proses yg berbeda.  
- Semua methods akan dijalankan secara paralel kecuali method dengan nama yg diawali underscore `_`  
- Method untuk multithreading/multiprocessing harus memiliki 2 parameter, yaitu: `result: dict` dan `q: queue.Queue`. Parameter `result` digunakan untuk memberikan return value dari method, dan Parameter `q` digunakan untuk mengirim data antar proses.  
- Method untuk asyncio harus menggunakan keyword `async def`, dan untuk perpindahan antar kode menggunakan `await asyncio.sleep(0)`, dan keyword `return` untuk memberikan return value.  
- Return Value berupa dictionary dengan key adalah nama function, dan value adalah return value dari setiap fungsi  
- Menjalankan Multiprocessing harus berada dalam blok `if __name__ == "__main__":` karena area global pada program akan diproses lagi. Terutama pada sistem operasi windows.  
- `run_asyncio()` akan menjalankan kode dalam satu program, hanya saja alur program dapat berpindah-pindah menggunkan `await asyncio.sleep(0)`.  
- `run_multi_threading()` akan menjalankan program dalam satu CPU, hanya saja dalam thread yang berbeda. Walaupun tidak benar-benar berjalan secara bersamaan namun bisa meningkatkan kecepatan penyelesaian program, dan dapat saling mengakses resource antar program.  Akses resource antar program bisa secara langsung maupun menggunakan parameter yang sudah disediakan yaitu `result: dict` dan `q: queue.Queue`.  
- `run_multi_processing()` akan menjalankan program dengan beberapa CPU. Program akan dibuatkan environment sendiri yang terpisah dari program induk. Keuntungannya adalah program dapat benar-benar berjalan bersamaan, namun tidak dapat saling mengakses resource secara langsung. Akses resource menggunakan parameter yang sudah disediakan yaitu `result: dict` dan `q: queue.Queue`.  
  
```python  
class ExampleRunParallel(RunParallel):  
    z = "ini"  
  
    def __init__(self) -> None:  
        self.pop = random.randint(0, 100)  
  
    def _set_property_here(self, v):  
        self.prop = v  
  
    def a(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["a"] = "a"  
        q.put("from a 1")  
        q.put("from a 2")  
  
    def b(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["b"] = "b"  
        result["q_get"] = q.get()  
  
    def c(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["c"] = "c"  
        result["q_get"] = q.get()  
  
    async def d(self):  
        print("hello")  
        await asyncio.sleep(0)  
        print("hello")  
  
        result = {}  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["d"] = "d"  
        return result  
  
    async def e(self):  
        print("world")  
        await asyncio.sleep(0)  
        print("world")  
  
        result = {}  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["e"] = "e"  
        return result  
  
if __name__ == "__main__":  
    print(ExampleRunParallel().run_asyncio())  
    print(ExampleRunParallel().run_multi_threading())  
    print(ExampleRunParallel().run_multi_processing())  
```

Output:
```py
```

## __calculate__quantity__

`__calculate__quantity__`

## generator

`generator`

Class ini menyediakan beberapa fungsi yang bisa mengembalikan generator.  
Digunakan untuk mengoptimalkan program.  
  
Class ini dibuat karena python generator yang disimpan dalam variabel  
hanya dapat diakses satu kali.

## html_dl

`html_dl`

Class ini digunakan untuk serialize dan unserialize html

## html_ol

`html_ol`

Class ini digunakan untuk serialize dan unserialize html

## html_table

`html_table`

Class ini digunakan untuk serialize dan unserialize html

## html_ul

`html_ul`

Class ini digunakan untuk serialize dan unserialize html
