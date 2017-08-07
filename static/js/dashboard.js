/**
 * Created by Administrator on 2017/8/2.
 */

$(document).ready(function () {
    $(".nav-sidebar li a").click(function () {
        var nav_name = $("nav ul.navbar-nav li.active").children().first().attr("name");
        var rock_name = $(this).text();
        var next_url = "/" + nav_name + "/?rock=" + rock_name;
        $(this).parent().siblings().removeClass("active");
        $(this).parent().addClass("active");
        window.location.href=next_url;
    });
});


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

// 用于ajax时的csrf问题
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});