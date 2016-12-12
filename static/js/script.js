var topic_name = "";
var task_type = ''; 
function getTask() {
    $('#wrapper #options input').removeClass().addClass('btn btn-lg btn-default');
    $.ajax({
        url: task_type,
        data: {topic: topic_name},
        type: 'POST',
        success: function(response) {
            $("#sentence").text(response.task)
            correct_num = Math.floor(Math.random() * 4)
            $("#options input").attr('correct', '0')
            $("#options input:eq(" + correct_num + ")").attr({'value': response.options[0], 'correct': '1'});
            j = 1;
            for (i = 0; i < 4 && j < response.options.length; ++i) {
                if (i == correct_num)
                    continue;
                $("#options input:eq(" + i + ")").attr('value', response.options[j++]);
            }
        }
    });
}
$(function() {
    if (window.location.href.includes('semantics'))
        task_type = '/semantic_task';
    else 
        task_type = '/grammar_task';

    $('#wrapper').hide();
    wrapper_margin_top = ($(window).height() - $("#wrapper").height())/2;
    cat_margin_top = ($(window).height() - $("#subcat").height())/2;
    $("#wrapper").css('marginTop', wrapper_margin_top);
    $("#subcat").css('marginTop', cat_margin_top);
    $('#generate').click(getTask);
    $('#wrapper #options input').click(function() {
        $('#wrapper #options input').removeClass().addClass('btn btn-lg btn-default');
        if ($(this).attr('correct') == '1') {
            $(this).removeClass().addClass('btn btn-lg btn-success');
            setTimeout('getTask()', 1500);
        }
        else
            $(this).removeClass().addClass('btn btn-lg btn-danger');
    });
    $("#categories input").click(function() {
        topic_name = $(this).attr('topic');
        $('#categories').hide();
        getTask();
        $('#wrapper').show();
    });
});