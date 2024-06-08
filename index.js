database = $.ajax({
    url: "database.json",//json文件位置，文件名
    type: "GET",//请求方式为get
    dataType: "json", //返回数据格式为json
    async: false,
    success: function (data) {//请求成功完成后要执行的方法 
    }
});
picsData = Object.values(database.responseJSON).reverse();

//Global vars:
var dataLength = picsData.length;
var loopLength = 3; //Set loop length.
var initItemsLength = 9; //set initial items length.
var itemDelay = 300;

//Create elements:
function getItem(param) {
    //Find data:
    var imgName = picsData[param].thumb_name;
    //Create image:
    var image = new Image();
    image.className = 'img-item';
    image.src = 'imgs/' + imgName + '.webp';
    //Create title:
    var title = document.createElement('span');
    title.className = "thumb-title";
    titleText = document.createTextNode(picsData[param].thumb_name);
    title.appendChild(titleText);
    //Create container:
    var item = document.createElement('div');
    item.className = 'item';
    item.appendChild(title);
    item.appendChild(image);
    return item;
}

//Append initial items:
function appendItemInit() {
    for (i = 0; i < initItemsLength; i++) {
        (function (i) {
            setTimeout(function () {
                if (initItemsLength < dataLength) {
                    //Get item:
                    var elems = getItem(i);
                    //Create jQuery object:
                    var $elems = $(elems);
                    //Append item:
                    $(".grid").append($elems);
                    // console.log(picsData[i].id);
                }
                else {
                    $('.append-button').hide();
                    $(".status").fadeIn();
                };
            }, itemDelay * i);
        }(i)); //Add delay between appended items.
    };
};
appendItemInit();

//Append new items:
function appendItem() {
    for (i = 0; i < loopLength; i++) {
        (function (i) {
            setTimeout(function () {
                if (initItemsLength < dataLength) {
                    //Get item:
                    var elems = getItem(initItemsLength);
                    //Create jQuery object:
                    var $elems = $(elems);
                    //Append item:
                    $(".grid").append($elems);
                    // console.log(picsData[initItemsLength].id);
                    //Modify items counter:
                    initItemsLength += 1;
                }
                else {
                    $('.append-button').hide();
                    $(".status").fadeIn();
                };
            }, itemDelay * i);
        }(i)); //Add delay between appended items.
    };
};

//Infinite Scroll (trigger):
$(window).scroll(function () {
    if (Math.ceil($(window).scrollTop() + window.innerHeight) == $(document).height()) {
        appendItem();
    }
});
