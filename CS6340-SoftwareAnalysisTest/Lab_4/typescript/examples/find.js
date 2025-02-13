var arr = ["apple", "orange", "cherry", "banana", "pear"];
/*
@returns index of elem in arr
*/
function find(elem, arr) {
    for (var i = 0; i < arr.length; i++) {
        if (elem === arr[i]) {
            return i;
        }
    }
}
console.log(find("cherry", arr));
console.log(find("peach", arr));
