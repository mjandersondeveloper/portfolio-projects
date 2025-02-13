var prism = {
    length: 5,
    width: 10,
    height: 3
};
var cone = {
    baseArea: 45,
    height: 3
};
function printVolume(obj) {
    console.log(obj.length * obj.width * obj.height);
}
printVolume(prism);
printVolume(cone);
