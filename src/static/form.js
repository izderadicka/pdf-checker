$(function() {
var $h=$('.group-header'),
form_action = $('form').attr('action');

$h.click(function(evt) {
	if ($h.hasClass('collapsed')) {
		$h.removeClass('collapsed').addClass('expanded');
		$('.group-body').show();
	} else {
		$h.removeClass('expanded').addClass('collapsed');
		$('.group-body').hide();
	}
});
$('input[type="submit"]').click(function(evt) {
	if (!$('input[name="file"]').val() || ! $('select[name="cat"]').val()) {
		alert("File and it's category are required!");
		evt.preventDefault();
	} 
	else  if (! $('.cb_cell input[type="checkbox"]:checked').length ) {
		alert("No check is selected!");
		evt.preventDefault();
	}
	var f =$('form');
	f.attr('action',form_action+'?LOB='+ $('select[name="cat"]').val());
});
var $cat=$('select[name="cat"]');

var clearChecks = function () {
	
}
$cat.change(function (evt) {
	var newCat = $cat.val();
	$('.cb_cell input[type="checkbox"]').prop('checked', false).change();
	if (newCat) {
		var checks = [];
		for (var i=0;i< checkCategories.length; i++) {
			var name = checkCategories[i][0],
			cats = checkCategories[i][1];
			if (cats.indexOf(newCat)>=0) checks.push(name);
		}
		for (i=0; i<checks.length;i++) {
			$('.cb_cell input[type="checkbox"][value="'+checks[i]+'"]').prop('checked', true).change();
		}
	}
});

});