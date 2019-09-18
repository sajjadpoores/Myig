var modal1 = document.getElementById("all1");
var modal2 = document.getElementById("all2");
var modal3 = document.getElementById("all3");
var modal4 = document.getElementById("all4");
var modal5 = document.getElementById("all5");
var modal6 = document.getElementById("all6");
var modal7 = document.getElementById("all7");
var noscrl1 = document.getElementById("adding1");
var noscrl2 = document.getElementById("adding2");
var noscrl3 = document.getElementById("adding3");
var noscrl4 = document.getElementById("adding4");
var noscrl5 = document.getElementById("adding5");
var noscrl6 = document.getElementById("adding6");
var noscrl7 = document.getElementById("adding7");

window.onclick = (function (event) {
    if (event.target == modal1) {
        modal1.style.display = 'none';
        enable_scroll();
    } else if (event.target.id == noscrl1.id) {
        disable_scroll();
    }
    else if (event.target == modal2) {
        modal2.style.display = 'none';
        enable_scroll();
    } else if (event.target.id == noscrl2.id) {
        disable_scroll();
    }
    else if (event.target == modal3) {
        modal3.style.display = 'none';
        enable_scroll();
    } else if (event.target.id == noscrl3.id) {
        disable_scroll();
    }
    else if (event.target == modal4) {
        modal4.style.display = 'none';
        enable_scroll();
    } else if (event.target.id == noscrl4.id) {
        disable_scroll();
    }
    else if (event.target == modal5) {
        modal5.style.display = 'none';
        enable_scroll();
    } else if (event.target.id == noscrl5.id) {
        disable_scroll();
    }
    else if (event.target == modal6) {
        modal6.style.display = 'none';
        enable_scroll();
    } else if (event.target.id == noscrl6.id) {
        disable_scroll();
    }
    else if (event.target == modal7) {
        modal7.style.display = 'none';
        enable_scroll();
    } else if (event.target.id == noscrl7.id) {
        disable_scroll();
    }
});


var keys = [32, 33, 34, 35, 36, 37, 38, 39, 40];

function preventDefault(e) {
    e = e || window.event;
    if (e.preventDefault)
        e.preventDefault();
    e.returnValue = false;
}

function keydown(e) {
    for (var i = keys.length; i--;) {
        if (e.keyCode === keys[i]) {
            preventDefault(e);
            return;
        }
    }
}

function wheel(e) {
    preventDefault(e);
}

function disable_scroll() {
    var winx = window.scrollX;
    var winy = window.scrollY;
    window.onscroll = function () {
        window.scrollTo(winx, winy);
    };
}

function enable_scroll() {
    window.onscroll = function () {};
}

function disable_scroll_mobile() {
    document.addEventListener('touchmove', preventDefault, false);
}

function enable_scroll_mobile() {
    document.removeEventListener('touchmove', preventDefault, false);
}

function offscrl1() {
    enable_scroll();
    window.onscroll = function () {};
    modal1.style.display = 'none';
}
function offscrl2() {
    enable_scroll();
    window.onscroll = function () {};
    modal2.style.display = 'none';
}
function offscrl3() {
    enable_scroll();
    window.onscroll = function () {};
    modal3.style.display = 'none';
}
function offscrl4() {
    enable_scroll();
    window.onscroll = function () {};
    modal4.style.display = 'none';
}
function offscrl5() {
    enable_scroll();
    window.onscroll = function () {};
    modal5.style.display = 'none';
}

function offscrl6() {
    enable_scroll();
    window.onscroll = function () {};
    modal6.style.display = 'none';
}

function offscrl7() {
    enable_scroll();
    window.onscroll = function () {};
    modal7.style.display = 'none';
}
var myTextArea = $('#commentArea');

function addEmoji(emoji) {
    myTextArea.val(myTextArea.val() + emoji);
    document.getElementById('commentArea').focus();
}
