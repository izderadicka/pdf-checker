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
	};
	
	function showAbout(evt) {
		
		d=$('#dialog');
		$.get('/static/about.html',
				function (data) {
			$('.dialog-content', d).html(data);
			d.show();
		});
		evt.stopPropagation();
		evt.preventDefault();
	};
	
	$('#name-version').click(showAbout);
	$('#content').on('click', '.check-help', showHelp);
	
	$('#dialog .close-btn').click(function(evt) {
		$('#dialog').hide();
	})
	
});