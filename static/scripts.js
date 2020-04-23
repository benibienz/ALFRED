$(document).ready(function(){

    $('#dumpData').click(function(env){
        $.get("{{ url_for('gui.dump_data', env=env) }}");
    });

    $('.action').click(function(){
        $.post(
            $SCRIPT_ROOT + '/act',  // endpoint
            {'action': $(this).attr('id'), 'env': $ENV},  // POST action
            function(data, status){  // callback
                // update state
                $.each(data['state'], function(k, s) {
                    $('#state' + k).text(s);
                })
                // update action colors
                $.each(data['probs'], function(k, p) {
                    $('#action' + k).css('background-color','rgb(0,' + 200 * p + ',0)');
                })
            }
            );

	});



});