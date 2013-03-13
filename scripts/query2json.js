$(function () {
	$('.output').hide()
	$('input').keypress(function (e) {
		if (e.which == 13) {
			$.get('/new/', {url: $(this).val(), response: "cake cake cake"}, function (d) {
				$('#url').text(d.url);
				$('.output').slideDown();
			}, 'JSON')
		}
	})
})