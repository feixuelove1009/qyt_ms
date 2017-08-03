/**
 * Created by Administrator on 2017/8/2.
 */
$(document).ready(function () {
    $('#submit').click(function () {
        var name = $('#login input[type="text"]').val();
        var pwd = $('#login input[type="password"]').val();
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
                    $("span.login-message").text("登录成功！返回先前页面...").css({"color":"darkgreen","font-size":"14px"});
                    window.setTimeout("window.location.href='/test/'",1000);
                }else{
                    $("span.login-message").text(data.message).css({"color":"#ea5d45","font-size":"14px"});
                    window.setTimeout('$("span.login-message").text("").removeAttr("style");',2000);
                }
            }
        });

     });   
    
});


