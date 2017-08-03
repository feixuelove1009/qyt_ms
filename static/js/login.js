/**
 * Created by Administrator on 2017/8/2.
 */
$(document).ready(function () {
    $("#submit").click(function () {
        var name = $('input[type="text"]').val();
        var pwd = $('input[type="password"]').val();
        $.ajax({
            url:"/login/",
            type:"POST",
            dataType:'json',
            data:{
                "name":name,
                "pwd":pwd
            },
            success:function (data) {
                if(data.status){
                    window.location.href="/test/";
                }else{
                    alert(data.message);
                }
            }
        });

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

