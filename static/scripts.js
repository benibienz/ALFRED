$(document).ready(function(){

    $('#dumpData').click(function(env){
        $.get("{{ url_for('gui.dump_data', env=env) }}");
    });

    $('.Action').click(function(){
        var env = $(this).attr('data-env');
		$(this).text('working');
        $.post($SCRIPT_ROOT + env + '/ajaxact', {'val': 1});
	});

});