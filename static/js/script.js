var topic_name = "";
var task_type = ''; 
var num_right = 0;
var num_done = 0;
var mistake = false;
var task_id = 0;

function getTask() {
    $('#wrapper #options input').removeClass().addClass('btn btn-lg btn-default');
    $.ajax({
        url: task_type,
        data: {taskid: task_id},
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
    {
        task_type = '/semantic_task';
        path_back = '/semantics';
    }
    else {
        task_type = '/grammar_task';
        path_back = '/grammar';
    }

    $('#wrapper').hide();
    wrapper_margin_top = ($(window).height() - $("#wrapper").height())/2;
    cat_margin_top = ($(window).height() - $("#subcat").height())/2;
    $("#wrapper").css('marginTop', wrapper_margin_top);
    $("#subcat").css('marginTop', cat_margin_top);
    $('#generate').click(getTask);
    mistake = false;
    $('#wrapper #options input').click(function() {
        $('#wrapper #options input').removeClass().addClass('btn btn-lg btn-default');
        if ($(this).attr('correct') == '1') {
            $(this).removeClass().addClass('btn btn-lg btn-success');
            if (mistake == false)
            {
                num_right = num_right + 1;
            }
            num_done = num_done + 1;
            mistake = false;
            if (num_done < 3) {
                setTimeout('getTask()', 1500);
            }
            else {
                alert("Вы выполнили верно " + num_right + " из " + num_done + " заданий!");
                num_done = 0;
                var last_result = num_right.toString();
                num_right = 0;
                // $(location).attr('href', '/index');
                document.location.href = path_back + "?right=" + last_result + "&taskid=" + task_id.toString();
            }
        }
        else
        {
            $(this).removeClass().addClass('btn btn-lg btn-danger');
            mistake = true;
        }
    });
    $("#categories input").click(function() {
        topic_name = $(this).attr('topic');
        task_id = $(this).attr('taskid');
        $('#categories').hide();
        num_done = 0;
        num_right = 0;
        getTask();
        $('#wrapper').show();
    });
});