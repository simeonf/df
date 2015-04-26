fluidvids.init({
	selector: ['iframe'],
	players: ['www.youtube.com', 'player.vimeo.com']
});

$(document).ready(function() {
	$('.tooltip').tooltipster({
		offsetY: -3
	});
});