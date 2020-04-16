$(document).ready(function(){

    $('#dumpData').click(function(env){
        $.get("{{ url_for('gui.dump_data', env=env) }}");
    });

    $('.action').click(function(){
        $.post(
            $SCRIPT_ROOT + '/act',  // endpoint
            {'action': $(this).attr('id'), 'env': $ENV},  // form to post
            function(data, status){
                // update state
                $.each(data['state'], function(k, s) {
                    $('#state' + k).text(s[1]);
                })
                // update action colors
                $.each(data['probs'], function(k, p) {
                    $('#action' + k).css('background-color','rgb(0,' + 200 * p + ',0)');
                })
            }
            );

	});



});