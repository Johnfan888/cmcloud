// host，interface下拉菜单二级联动
$(document).ready(function(){
$("#one").change(function(){
$("#one option").each(function(i,o){
if($(this).attr("selected"))
{
$(".two").hide();
$(".two").eq(i).show();
}
});
});
$("#one").change();
});

// value，data下拉菜单二级联动
$(document).ready(function(){
$("#one2").change(function(){
$("#one2 option").each(function(i,o){
if($(this).attr("selected"))
{
$(".two2").hide();
$(".two2").eq(i).show();
}
});
});
$("#one2").change();
});


// unit文本
// 当选择什么的时候显示unitinput
$(function() {
    $('#one2').change(function() {
        if (this.value == '0') {
                    $('#unitinput').show();
                } else {
                    $('#unitinput').hide();
        }
    });
});


$(function() {
    $('#two22').change(function() {
        if (this.value == 'Boolean'){
                    $('#unitinput').hide();
                } else {
                    $('#unitinput').show();
        }
    });
});


//隐藏interface

// $(document).ready(function(){
// $("one").change(function() {   //为Select添加事件，当选择其中一项时触发
//  var checkValue = $("#one").val();  //获取Select选择的Value
//     // var itemgroups = document.getElementById('itemgroups');
//  //   清除
// $(".itemgroups").empty();
// $(".itemgroups").val(checkValue);
// $("select[id='itemgroups'] option[value=checkValue]").remove();
// // var option = $("<option>").val(checkValue);
// // $(".itemgroups").append(option);
//
//                             });
// });
// {#从数据库取值需要加上safe不然乱码报错invalid property id#}
