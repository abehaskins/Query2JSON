$(function () {
	$('.output').hide()
	$('input[name=response]').keypress(function (e) {
		if (e.which == 13) {
			$.get('/new/', {url: $('input[name=url]').val(), response: $(this).val()? $(this).val():" "}, function (d) {
				$('#url').text(d.url);
				$('.output').slideDown();
			}, 'JSON')
		}
	})
})