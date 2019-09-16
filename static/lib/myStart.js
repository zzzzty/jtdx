$.fn.createMyStar = function(onimage,offimage){
    //alert($(this).attr("id"));
    var ths_id = $(this).attr("id");//当前元素的id
    $(this).append('<div class="target-star"></div>');//此元素添加控件
    $(this).find('.target-star').raty({//在当前元素下 找到刚刚添加的元素
        //cancel:false,
        score:6,
        number:10,
        scoreName:"score_"+ths_id,
        starOn:onimage,
        starOff:offimage,
        half:false,
        showHalf:false,
        hints:["1分","2分","3分","4分","5分","6分","7分","8分","9分","10分"],
        click:function(score){
            $("#showit").val(score);
            //document.getElementById("showit").innerHTML = score+"分";
            document.getElementById("p_"+ths_id).innerHTML = score+"分";
            }
    });
    // alert(onimage);
};



//在rateteacher.html 中使用

// <!-- <div class="evaluate">
// <div id="starts"></div>
// <div id="title"></div>
// </div> -->
        // $(function(){
        //     $("#starts").raty({
        //         number:10,
        //         path:"",
        //         starOn:"{% static 'lib/images/star-on.png' %}",
        //         starOff:"{% static 'lib/images/star-off.png' %}",
        //         target:"#title",
        //         //noRatedMsg:'no rate',
        //         targetScore:undefined,
        //         scoreName:"test",
        //         score:5,
        //         // targetText:'分数',
        //         // targetForma:'8',
        //         hints:["1分","2分","3分","4分","5分"],
        //         click:function(score,evt){
        //             $("#grade").val(score);
        //         }
        //     });
        // });