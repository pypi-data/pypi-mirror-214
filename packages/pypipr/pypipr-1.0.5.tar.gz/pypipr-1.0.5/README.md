
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
<generator object generator.batchmaker at 0x6f4e04bd00>
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
<generator object generator.chunck_array at 0x6f4e113e40>
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
2023-06-17 19:42:38.320047+07:00
2023-06-17 12:42:38.321742+00:00
2023-06-17 05:42:38.326459-07:00
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
(<function ExampleGetClassMethod.a at 0x6f4deca840>, <function ExampleGetClassMethod.b at 0x6f4deca7a0>, <function ExampleGetClassMethod.c at 0x6f4deca980>, <function ExampleGetClassMethod.d at 0x6f4decaa20>)
```

## get_filemtime

`get_filemtime`

Mengambil informasi last modification time file dalam nano seconds  

```python  
print(get_filemtime(__file__))  
```

Output:
```py
1686946602367473992
```

## get_filesize

`get_filesize`

Mengambil informasi file size dalam bytes  

```python  
print(get_filesize(__file__))  
```

Output:
```py
43832
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
weq, asd, qweqw, dfs
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
[<Element a at 0x6f4dfaaa80>, <Element a at 0x6f4dfab340>, <Element a at 0x6f4dd67110>, <Element a at 0x6f4dd671b0>, <Element a at 0x6f4dd67200>, <Element a at 0x6f4dd67250>, <Element a at 0x6f4dd672a0>, <Element a at 0x6f4dd672f0>, <Element a at 0x6f4dd67340>, <Element a at 0x6f4dd67390>, <Element a at 0x6f4dd673e0>, <Element a at 0x6f4dd67430>, <Element a at 0x6f4dd67480>, <Element a at 0x6f4dd674d0>, <Element a at 0x6f4dd67520>, <Element a at 0x6f4dd67570>, <Element a at 0x6f4dd675c0>, <Element a at 0x6f4dd67610>]
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
<generator object generator.irange at 0x6f50d0cbf0>
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
<generator object generator.iscandir at 0x6f4e112040>
(PosixPath('.git'), PosixPath('.vscode'), PosixPath('pypipr'), PosixPath('dist'))
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
            __hash__ : 4220706935049599506
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
            _flavour : <pathlib._PosixFlavour object at 0x6f4fa99cd0>
               _hash : 4220706935049599506
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
             iterdir : <generator object Path.iterdir at 0x6f4decf060>
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
True
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
<Timer(Thread-2, started 478028631296)>
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
<generator object generator.sets_ordered at 0x6f4df0e810>
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
 [['Harga Emas Hari Ini - Sabtu, 17 Juni 2023'],
  ['Spot Emas USD↑1.957,84 (+3,32) / oz',
   'Kurs IDR15.140,00 / USD',
   'Emas IDR↑953.003 (+1.616) / gr'],
  ['LM Antam (Jual)↑1.063.000 (+2.000) / gr',
   'LM Antam (Beli)↑945.000 (+3.000) / gr']],
 [['Harga Emas Hari Ini'],
  ['Gram', 'Gedung Antam Jakarta', 'Pegadaian'],
  ['per Gram (Rp)', 'per Batangan (Rp)', 'per Gram (Rp)', 'per Batangan (Rp)'],
  ['1000',
   '1.004 (+2)',
   '1.003.600 (+2.000)',
   '1.026.640 (+9.225)',
   '1.026.640.000 (+9.225.000)'],
  ['500',
   '2.007 (+4)',
   '1.003.640 (+2.000)',
   '1.026.682 (+9.226)',
   '513.341.000 (+4.613.000)'],
  ['250',
   '4.016 (+8)',
   '1.004.060 (+2.000)',
   '1.027.112 (+9.224)',
   '256.778.000 (+2.306.000)'],
  ['100',
   '10.051 (+20)',
   '1.005.120 (+2.000)',
   '1.028.200 (+9.220)',
   '102.820.000 (+922.000)'],
  ['50',
   '20.118 (+40)',
   '1.005.900 (+2.000)',
   '1.029.000 (+9.220)',
   '51.450.000 (+461.000)'],
  ['25',
   '40.299 (+80)',
   '1.007.480 (+2.000)',
   '1.030.640 (+9.240)',
   '25.766.000 (+231.000)'],
  ['10',
   '101.250 (+200)',
   '1.012.500 (+2.000)',
   '1.035.800 (+9.200)',
   '10.358.000 (+92.000)'],
  ['5',
   '203.600 (+400)',
   '1.018.000 (+2.000)',
   '1.041.400 (+9.200)',
   '5.207.000 (+46.000)'],
  ['3',
   '341.556 (+667)',
   '1.024.667 (+2.000)',
   '1.048.333 (+9.000)',
   '3.145.000 (+27.000)'],
  ['2',
   '516.500 (+1.000)',
   '1.033.000 (+2.000)',
   '1.057.000 (+9.000)',
   '2.114.000 (+18.000)'],
  ['1',
   '1.063.000 (+2.000)',
   '1.063.000 (+2.000)',
   '1.088.000 (+9.000)',
   '1.088.000 (+9.000)'],
  ['0.5',
   '2.326.000 (+4.000)',
   '1.163.000 (+2.000)',
   '1.192.000 (+10.000)',
   '596.000 (+5.000)'],
  ['Update harga LM Antam :17 Juni 2023, pukul 08:23Harga pembelian kembali '
   ':Rp. 945.000/gram (+3.000)',
   'Update harga LM Pegadaian :17 Juni 2023']],
 [['Spot Harga Emas Hari Ini (Market Close)'],
  ['Satuan', 'USD', 'Kurs\xa0Dollar', 'IDR'],
  ['Ounce\xa0(oz)', '1.957,84 (+3,32)', '15.140,00', '29.641.698'],
  ['Gram\xa0(gr)', '62,95', '15.140,00', '953.003 (+1.616)'],
  ['Kilogram\xa0(kg)', '62.946,02', '15.140,00', '953.002.708'],
  ['Update harga emas :17 Juni 2023, pukul 19:42Update kurs :13 Febuari 2023, '
   'pukul 09:10']],
 [['Gram', 'UBS Gold 99.99%'],
  ['Jual', 'Beli'],
  ['/ Batang', '/ Gram', '/ Batang', '/ Gram'],
  ['100', '95.685.000', '956.850', '94.300.000', '943.000'],
  ['50', '47.895.000', '957.900', '47.150.000', '943.000'],
  ['25', '24.050.000', '962.000', '23.575.000', '943.000'],
  ['10', '9.670.000', '967.000', '9.430.000', '943.000'],
  ['5', '4.887.000', '977.400', '4.715.000', '943.000'],
  ['1', '1.010.000', '1.010.000', '943.000', '943.000'],
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
  ['oz', '1.954,52', '+3,32+0,17%', '29.591.433', '+50.265+0,17%'],
  ['gr', '62,84', '+0,11+0,17%', '951.387', '+1.616+0,17%'],
  ['30 Hari', 'Kurs', '', '', '15.140', '%'],
  ['oz', '1.955,32', '+2,52+0,13%', '29.603.545', '+38.153+0,13%'],
  ['gr', '62,86', '+0,08+0,13%', '951.776', '+1.227+0,13%'],
  ['2 Bulan', 'Kurs', '', '', '15.140', '%'],
  ['oz', '2.005,47', '-47,63-2,38%', '30.362.816', '-721.118-2,38%'],
  ['gr', '64,48', '-1,53-2,38', '976.187', '-23.184-2,38%'],
  ['6 Bulan', 'Kurs', '', '', '15.617', '-477-3,05%'],
  ['oz', '1.788,31', '+169,53+9,48%', '27.928.037', '+1.713.660+6,14%'],
  ['gr', '57,50', '+5,45+9,48%', '897.907', '+55.095+6,14%'],
  ['1 Tahun', 'Kurs', '', '', '14.741', '+399+2,71%'],
  ['oz', '1.838,69', '+119,15+6,48%', '27.104.148', '+2.537.550+9,36%'],
  ['gr', '59,12', '+3,83+6,48%', '871.419', '+81.584+9,36%'],
  ['2 Tahun', 'Kurs', '', '', '14.257', '+883+6,19%'],
  ['oz', '1.772,06', '+185,78+10,48%', '25.264.277', '+4.377.420+17,33%'],
  ['gr', '56,97', '+5,97+10,48%', '812.265', '+140.737+17,33%'],
  ['3 Tahun', 'Kurs', '', '', '14.234', '+906+6,37%'],
  ['oz', '1.726,92', '+230,92+13,37%', '24.580.979', '+5.060.718+20,59%'],
  ['gr', '55,52', '+7,42+13,37%', '790.297', '+162.706+20,59%'],
  ['5 Tahun', 'Kurs', '', '', '13.902', '+1.238+8,91%'],
  ['oz', '1.278,27', '+679,57+53,16%', '17.770.510', '+11.871.188+66,80%'],
  ['gr', '41,10', '+21,85+53,16%', '571.335', '+381.668+66,80%']])
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram'],
 [[''],
  ['Emas 24 KaratHarga Emas 1 Gram', ''],
  ['USD', '62,95↑', '+0,11+0,18%'],
  ['KURS', '14.961,45↓', '-0,40-0,00%'],
  ['IDR', '941.763,70↑', '+1.571,86+0,17%'],
  ['Sabtu, 17 Juni 2023 19:42']],
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
  ['USD', '62,84', '62,84 - 62,95', '62,90'],
  ['KURS', '14.961,85', '14.961,45 - 14.961,85', '14.961,65'],
  ['IDR', '940.191,84', '940.191,84 - 941.763,70', '940.977,77'],
  [''],
  ['', 'Awal Tahun', 'Pergerakkan YTD', '+/- YTD'],
  ['USD', '58,64', '58,23 - 65,97', '+4,31 (7,35%)'],
  ['KURS', '15.538,50', '14.669,40 - 15.629,15', '-577,05(-3,71%)'],
  ['IDR', '911.153,72', '888.842,84 - 982.694,10', '+30.609,98 (3,36%)'],
  [''],
  ['', 'Tahun Lalu / 52 Minggu', 'Pergerakkan 52 Minggu', '+/- 52 Minggu'],
  ['USD', '59,55', '52,31 - 65,97', '+3,40 (5,71%)'],
  ['KURS', '14.819,05', '14.653,00 - 15.785,40', '+142,40 (0,96%)'],
  ['IDR', '882.497,28', '795.009,21 - 982.694,10', '+59.266,42 (6,72%)']])
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
{'a': <generator object ExampleComparePerformance.a.<locals>.<genexpr> at 0x6f4df0df20>,
 'b': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
 'c': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 'd': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
{'a': 158, 'b': 128, 'c': 100, 'd': 139}
{'a': 160, 'b': 152, 'c': 100, 'd': 148}
{'a': 137, 'b': 142, 'c': 100, 'd': 130}
{'a': 113, 'b': 122, 'c': 100, 'd': 128}
{'a': 133, 'b': 141, 'c': 100, 'd': 137}
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
