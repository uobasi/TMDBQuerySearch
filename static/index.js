$(document).ready(function(){
    $('form').on('submit', function(event){
        $.ajax({
            data : {
                query: $('#movieQuery').val()
            },
            type:'POST',
        })
        event.preventDefault();
    });
});