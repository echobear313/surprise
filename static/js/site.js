$.ajax({
    url:"/get_result",
    type:'get',
    data:{},
    timeout:20000,
    // 请求发送之前（发送请求前可修改XMLHttpRequest对象的函数，如添加自定义HTTP头。）。
    beforeSend:function(XMLHttpRequest){
        $("#warning").html("<h2>正在处理，请稍后···</h2>");
    },
    // 请求成功后的回调函数
    success:function(data,textStatus){
        $("#doing").html(String(data));
    },
    // 请求完成后的回调函数 (请求成功或失败之后均调用)
    complete:function(XMLHttpRequest,textStatus){
        // $("#doing").empty();
    },
    // 请求失败时调用此函数。
    error:function(XMLHttpRequest,textStatus,errorThrown){
        $("#doing").html("<h2>请求失败，请稍后再试！</h2>");
    }
});