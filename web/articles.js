var articles = [{
        name: "t-shirt",
        icon: "flaticon-shirt-2"
    },
    {
        name: "jacket",
        icon: "flaticon-cardigan"
    },
    {
        name: "jeans",
        icon: "flaticon-jeans-1"
    },
    {
        name: "shorts",
        icon: "flaticon-swimsuit-1"
    },
]
Array.prototype.chunk = function(groupsize) {
    var sets = []
    var chunks = this.length / groupsize
    for (var i = 0, j = 0; i < chunks; i++, j += groupsize)
        sets[i] = this.slice(j, j + groupsize)
    return sets
}