sed -i "75s|.*|typedef _Complex float __cfloat128 __attribute__ ((__mode__ (__TC__)));|" /usr/include/x86_64-linux-gnu/bits/floatn.h
sed -i "87s|.*|typedef __float128 _Float128;|" /usr/include/x86_64-linux-gnu/bits/floatn.h
