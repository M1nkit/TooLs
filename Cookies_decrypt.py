import re
import sys
from struct import unpack
import io
from time import strftime, gmtime

# PUT YOUR Cookies.binarycookies FILE PATH HERE
FilePath = 'C:/Users/xxx/Desktop/Cookies.binarycookies'

try:
    binaryFile = open(FilePath, 'rb')
except IOError as e:
    print('File Not Found :' + FilePath)
    sys.exit(0)

fileHeader = binaryFile.read(4)
if 'cook' not in str(fileHeader):
    print("Not a Cookies.binarycookie file")
    sys.exit(0)

pageNumber = unpack('>i', binaryFile.read(4))[0]

pageSizes = []
for i in range(pageNumber):
    pageSizes.append(unpack('>i', binaryFile.read(4))[0])

pages = []
for pageSize in pageSizes:
    pages.append(binaryFile.read(pageSize))

preCookieText = ''
for page in pages:
    page = io.BytesIO(page)
    page.read(4)
    cookiesNumber = unpack('<i', page.read(4))[0]
    cookieOffsets = []
    for cookiesNumberIndex in range(cookiesNumber):
        cookieOffsets.append(unpack('<i', page.read(4))[0])

    page.read(4)
    cookie = ''
    for offset in cookieOffsets:
        page.seek(offset)
        cookiesize = unpack('<i', page.read(4))[0]
        cookie = io.BytesIO(page.read(cookiesize))

        cookie.read(4)

        flags = unpack('<i', cookie.read(4))[0]
        cookieFlags = ''
        if flags == 0:
            cookieFlags = ''
        elif flags == 1:
            cookieFlags = 'Secure'
        elif flags == 4:
            cookieFlags = 'HttpOnly'
        elif flags == 5:
            cookieFlags = 'Secure; HttpOnly'
        else:
            cookieFlags = 'Unknown'

        cookie.read(4)

        urlOffset = unpack('<i', cookie.read(4))[0]
        nameOffset = unpack('<i', cookie.read(4))[0]
        pathOffset = unpack('<i', cookie.read(4))[0]
        valueOffset = unpack('<i', cookie.read(4))[0]

        endOfCookie = cookie.read(8)
        expiryDateEpoch = unpack('<d', cookie.read(8))[0] + 978307200
        expiryDate = strftime("%a, %d %b %Y ", gmtime(expiryDateEpoch))[:-1]

        createDateEpoch = unpack('<d', cookie.read(8))[0] + 978307200
        createDate = strftime("%a, %d %b %Y ", gmtime(createDateEpoch))[:-1]

        cookie.seek(urlOffset - 4)
        url = ''
        u = cookie.read(1)
        while unpack('<b', u)[0] != 0:
            url = url + str(u)
            u = cookie.read(1)

        cookie.seek(nameOffset - 4)
        name = ''
        n = cookie.read(1)
        while unpack('<b', n)[0] != 0:
            name = name + str(n)
            n = cookie.read(1)

        cookie.seek(pathOffset - 4)
        path = ''
        pa = cookie.read(1)
        while unpack('<b', pa)[0] != 0:
            path = path + str(pa)
            pa = cookie.read(1)

        cookie.seek(valueOffset - 4)
        value = ''
        va = cookie.read(1)
        while unpack('<b', va)[0] != 0:
            value = value + str(va)
            va = cookie.read(1)
        cookieHere = 'Cookie: ' + name + '=' + value + '; domain=' + url + '; path=' + path + '; ' + 'expires=' + expiryDate + '; ' + cookieFlags
        preCookieText = cookieHere + '__LINE_9533_BREAK__' + preCookieText

preCookieText = re.sub(r"b'(.*?)'", '\g<1>', preCookieText)
preCookieText = re.sub('__LINE_9533_BREAK__', '\n', preCookieText)
with open('Cookies.binarycookies.txt', 'w+') as CookieText:
    CookieText.write(preCookieText)
CookieText.close()
