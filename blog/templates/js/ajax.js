$(document).ready(function(){
    $('button[name=plus]').click(function(){
        var id = {{ post.pk }};
        cUrl = '/post/plus/'+id
        $.ajax({
            url: cUrl,
            dataType: 'json',
            success: function(data){
                if(data.rate){
                    $('#rate').html(data.rate);
                }
            }
        });
    });
    $('button[name=minus]').click(function(){
        var id = {{ post.pk }};
        cUrl = '/post/minus/'+id
        $.ajax({
            url: cUrl,
            dataType: 'json',
            success: function(data){
                if(data.rate){
                    $('#rate').html(data.rate);
                }
            }
        });
    });
    $('button[name=send]').click(function(){
        var text = $('textarea[name=text]').val();
        if(text){
            $('textarea[name=text]').val('');
            alert(text);
            $.ajax({
                url: ''
            });
        }
    });
});