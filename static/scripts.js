function updateImage(key) {
    var img_url = $IMAGES + '/sat.jpg';
    if (key == 'DEBRIS') { img_url = $IMAGES + '/debris.jpg'; }
    else if (key == 'UNKNOWN') { img_url = $IMAGES + '/unknown.png'; }
    $('img').attr('src', img_url);
}

$(document).ready(function(){

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
                // update image
                updateImage(data['state'][1])
            }
            );
	});

    $('#reset').click(function(env){
        $.get("{{ url_for('gui.main') }}");
    });
});