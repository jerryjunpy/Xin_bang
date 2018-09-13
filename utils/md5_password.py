# coding: utf-8
import hashlib
import random

def get_md5(parm):

    hl = hashlib.md5()
    hl.update(parm.encode(encoding='utf-8'))
    sign = hl.hexdigest()
    return sign

def get_data(link, data):

    li = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    nonce = ''.join(li[random.randint(0, 15)] for i in range(9))
    # nonce = "450543312"

    if data:
        string = "&".join(f"{k}={v}" for k, v in sorted(data.items()))
        string = link + string
    else:
        string = link

    string += ("&nonce=" + nonce)
    xyz = get_md5(string)
    return nonce, xyz

if __name__ == '__main__':
    nonce = "450543312"
    string = "/xdnphb/common/account/get?AppKey=joker"
    string += ("&nonce=" + nonce)
    print(string)
    print(get_md5(string))
