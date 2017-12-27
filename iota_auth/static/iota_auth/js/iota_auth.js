$(document).ready(function(){

	function generate_seed(len, charSet) {
	    charSet = charSet || 'ABCDEFGHIJKLMNOPQRSTUVWXYZ9';
	    var randomSeed = '';
	    for (var i = 0; i < len; i++) {
	        var randomPoz = Math.floor(Math.random() * charSet.length);
	        randomSeed += charSet.substring(randomPoz,randomPoz+1);
	    }
	    return randomSeed;
	}
	
	$('#generate_seed_button').click(function(){
		var seed = generate_seed(81)
		$('#seed_generated').html(seed)
	})
})