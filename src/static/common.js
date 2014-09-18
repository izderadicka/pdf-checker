$(function () {
function showHelp(evt) {
		var checkName = $(this).attr('data-check-name'),
		d=$('#dialog');
		$.get('/help/'+encodeURIComponent(checkName),
				function (data) {
			$('.dialog-content', d).html(data.help || 'No help available');
			d.show();
		});
		evt.stopPropagation();
		evt.preventDefault();
	}
	
	$('#content').on('click', '.check-help', showHelp);
	
	$('#dialog .close-btn').click(function(evt) {
		$('#dialog').hide();
	})
	
});