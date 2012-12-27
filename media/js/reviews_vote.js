$(document).ready(function(){
        $('ul.vote a').each(function(){
           $(this).click(function(){                             
                var type = $(this).attr('rel');
                var obj_id = $(this).parent().parent().attr('id');
                vote(type, obj_id);
           });
        });

        $(".dropdown dt a").click(function() {
            $(".dropdown dd ul").toggle(300);
        });
                    
        $(".dropdown dd ul li a").click(function() {
            var text = $(this).html();
            $(".dropdown dt a span").html(text);
            $(".dropdown dd ul").hide();
        });
                
    });

function vote(type, obj_id) {
    $('#'+obj_id+' span.q-vote').text('Loading...');
    $.ajax({
        url: '/review/vote-review',
        type: 'POST',
        dataType: "json",
        data: {
            id: obj_id,
            type: type
        },
        success: function(data){
            var max = data.length;
            var is_voted= $('#'+obj_id + ' .' + type + ' a').attr('class');
            if($.trim(is_voted) != '')
            {
                $('#'+obj_id + ' a').attr('class', '');
            }else{
                $('#'+obj_id + ' a').attr('class', '');
                $('#'+obj_id + ' .' + type + ' a').addClass('voted');                
            }
            for(var i=0;i<max;i++){
                if(parseInt(data[i].value) != 0){
                    $('#'+obj_id + ' .' + data[i].name + ' span.label').text('('+data[i].value+')');
                }
                else{
                    $('#'+obj_id + ' .' +  data[i].name + ' span.label').text('');
                }
            }

            
            $('#'+obj_id+' span.q-vote').text('Was this review helpful?');
        }
    });
}
 function showReviewLog(id){
        $('#reviewlog-'+id).show();
        $('#btn-log-'+id).hide();
    }
function closeReviewLog(id){
    $('#reviewlog-'+id).hide();
    $('#btn-log-'+id).show();
}
function saveLog(id){
    var review_id = $('#review-' +id).val();
    var comment = $('#review-comment-'+id).val();

    if($.trim(comment) != ""){        
        $.ajax({
        url: '/review/update',
        type: 'POST',
        dataType: "json",
        data: {
            review_id: review_id,
            comment: comment
        },
        success: function(data){
            var content = '<div class="borderBottom"></div><div><p>Updated Date: '+data[0].created_date+'</p><p>&lsquo;'+data[0].comment+'&rsquo;</p></div>';
            $('#viewlog-'+id).append(content);
           $('#reviewlog-'+id).hide();
            $('#btn-log-'+id).show();
        }
        });
    }
    else{
        alert("Please add your comment.");
    }
    
}